"""BLE communication for MELK LED Strip with correct protocol commands."""
import asyncio
import logging
import json
import os
from typing import Tuple, TypeVar, Callable, cast, Any
from bleak.backends.service import BleakGATTServiceCollection

try:
    from bleak.exc import BleakDBusError
except Exception:
    try:
        from bleak.exc import BleakError as BleakDBusError
    except Exception:
        class BleakDBusError(Exception):
            pass

from bleak_retry_connector import (
    BleakClientWithServiceCache,
    BleakNotFoundError,
    BLEAK_RETRY_EXCEPTIONS as BLEAK_EXCEPTIONS,
    establish_connection,
)
from homeassistant.components.bluetooth import async_ble_device_from_address
from homeassistant.exceptions import ConfigEntryNotReady

LOGGER = logging.getLogger(__name__)

# =========================================================
# Правильные команды из Magic Lantern APK v6.9.6
# =========================================================
# Формат команды: 7E [CMD] [SUBCMD] [PARAM1] [PARAM2] [PARAM3] [PARAM4] [PARAM5] EF

# Включение/выключение
TURN_ON_CMD = [0x7E, 0x04, 0x04, 0x01, 0xFF, 0xFF, 0xFF, 0x00, 0xEF]
TURN_OFF_CMD = [0x7E, 0x04, 0x04, 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0xEF]

# UUID для записи команд
WRITE_CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

# Настройки повторных попыток
DEFAULT_ATTEMPTS = 3
BLEAK_BACKOFF_TIME = 0.25
STATE_FILE = "/config/.storage/melk_led_state.json"
RETRY_BACKOFF_EXCEPTIONS = (BleakDBusError,)

WrapFuncType = TypeVar("WrapFuncType", bound=Callable[..., Any])


# =========================================================
# Декоратор безопасных повторных попыток BLE
# =========================================================
def retry_bluetooth_connection_error(func: WrapFuncType) -> WrapFuncType:
    """Retry decorator for BLE operations."""
    async def _async_wrap_retry(self: "BLEDOMInstance", *args, **kwargs):
        for attempt in range(DEFAULT_ATTEMPTS):
            try:
                return await func(self, *args, **kwargs)
            except BleakNotFoundError:
                raise
            except RETRY_BACKOFF_EXCEPTIONS as err:
                if attempt == DEFAULT_ATTEMPTS - 1:
                    LOGGER.error("%s: BLE retry exhausted: %s", self.name, err)
                    raise
                await asyncio.sleep(BLEAK_BACKOFF_TIME)
            except BLEAK_EXCEPTIONS as err:
                if attempt == DEFAULT_ATTEMPTS - 1:
                    LOGGER.error("%s: BLE exception: %s", self.name, err)
                    raise
    return cast(WrapFuncType, _async_wrap_retry)


# =========================================================
# Класс экземпляра устройства
# =========================================================
class BLEDOMInstance:
    """MELK LED Strip BLE device instance."""

    def __init__(self, address, reset: bool, delay: int, hass) -> None:
        self.address = address
        self._reset = reset
        self._delay = delay
        self._hass = hass

        self._device = async_ble_device_from_address(hass, address)
        if not self._device:
            raise ConfigEntryNotReady(f"Bluetooth device {address} not found.")

        self._client: BleakClientWithServiceCache | None = None
        self._connect_lock = asyncio.Lock()
        self._cached_services: BleakGATTServiceCollection | None = None
        self._write_uuid = None

        # Начальные значения
        self._is_on = False
        self._rgb_color: Tuple[int, int, int] = (255, 255, 255)
        self._brightness: int = 255
        self._effect_speed: int = 50
        self._last_effect: int | None = None

        asyncio.create_task(self._async_init_state())
        asyncio.create_task(self._delayed_connect())
        asyncio.create_task(self._heartbeat())

    # =========================================================
    # JSON-состояние
    # =========================================================
    def _load_state_sync(self):
        """Load state from JSON file."""
        try:
            os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get(self.address, {})
        except Exception as e:
            LOGGER.warning("Failed to load state for %s: %s", self.address, e)
        return {}

    async def _async_load_state(self):
        """Load state asynchronously."""
        return await self._hass.async_add_executor_job(self._load_state_sync)

    def _save_state_sync(self, payload: dict | None = None):
        """Save state to JSON file."""
        try:
            os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
            data: dict = {}
            if os.path.exists(STATE_FILE):
                try:
                    with open(STATE_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

            if payload is None:
                payload = {
                    "is_on": self._is_on,
                    "rgb": self._rgb_color,
                    "brightness": self._brightness,
                }

            data[self.address] = payload
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            LOGGER.error("Failed to save state for %s: %s", self.address, e)

    async def _async_save_state(self, payload: dict | None = None):
        """Save state asynchronously."""
        await self._hass.async_add_executor_job(self._save_state_sync, payload)

    async def _async_init_state(self):
        """Initialize state from saved data."""
        state = await self._async_load_state()
        self._is_on = state.get("is_on", False)
        self._rgb_color = tuple(state.get("rgb", (255, 255, 255)))  # type: ignore[arg-type]
        self._brightness = int(state.get("brightness", 255))
        LOGGER.info("%s: Loaded state from JSON: is_on=%s, rgb=%s, brightness=%s", 
                   self.name, self._is_on, self._rgb_color, self._brightness)

    # =========================================================
    # Свойства
    # =========================================================
    @property
    def name(self):
        return self._device.name if self._device else self.address

    @property
    def is_on(self) -> bool:
        return getattr(self, "_is_on", False)

    @property
    def brightness(self) -> int:
        return getattr(self, "_brightness", 255)

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        return getattr(self, "_rgb_color", (255, 255, 255))

    # =========================================================
    # Подключение BLE
    # =========================================================
    async def _delayed_connect(self):
        """Delayed initial connection."""
        await asyncio.sleep(3)
        await self._ensure_connected()

    async def _ensure_connected(self):
        """Ensure BLE connection is established."""
        if self._client and self._client.is_connected:
            return
        async with self._connect_lock:
            try:
                client = await establish_connection(
                    BleakClientWithServiceCache,
                    self._device,
                    self._device.name,
                    self._disconnected,
                    cached_services=self._cached_services,
                )
                self._client = client
                self._cached_services = client.services
                
                # Найти характеристику для записи
                c = client.services.get_characteristic(WRITE_CHARACTERISTIC_UUID)
                if c:
                    self._write_uuid = c
                    LOGGER.info("%s connected", self._device.name)
                else:
                    LOGGER.error("%s: write characteristic not found", self._device.name)
            except Exception as e:
                LOGGER.error("%s: connection failed: %s", self._device.name, e)
                await asyncio.sleep(5)
                asyncio.create_task(self._ensure_connected())

    def _disconnected(self, _client):
        """Handle disconnection."""
        asyncio.create_task(self._ensure_connected())

    async def _heartbeat(self):
        """Maintain connection with periodic checks."""
        while True:
            if not self._client or not self._client.is_connected:
                await self._ensure_connected()
            await asyncio.sleep(30)

    # =========================================================
    # BLE-команды (правильные из Magic Lantern APK)
    # =========================================================
    @retry_bluetooth_connection_error
    async def _write(self, data: list[int]):
        """Write command to BLE device."""
        await self._ensure_connected()
        await self._client.write_gatt_char(self._write_uuid, bytearray(data), False)
        # Добавляем задержку между командами для стабильности
        await asyncio.sleep(0.15)

    @retry_bluetooth_connection_error
    async def turn_on(self):
        """Turn on the light - команда: 7E 04 04 01 FF FF FF 00 EF"""
        await self._write(TURN_ON_CMD)
        self._is_on = True
        await self._async_save_state()

    @retry_bluetooth_connection_error
    async def turn_off(self):
        """Turn off the light - команда: 7E 04 04 00 FF FF FF 00 EF"""
        await self._write(TURN_OFF_CMD)
        self._is_on = False
        await self._async_save_state()

    @retry_bluetooth_connection_error
    async def set_brightness(self, value: int):
        """
        Set brightness (0-255).
        Команда: 7E 04 01 [BRIGHTNESS] FF FF FF 00 EF
        где BRIGHTNESS = 0-100 (процент)
        """
        self._brightness = max(1, min(int(value), 255))
        percent = round(self._brightness * 100 / 255)
        
        # Отправляем команду яркости
        await self._write([0x7E, 0x04, 0x01, percent, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])
        await asyncio.sleep(0.1)
        
        # Затем устанавливаем цвет
        r, g, b = self._rgb_color
        await self._write([0x7E, 0x07, 0x05, 0x03, r, g, b, 0x10, 0xEF])
        
        await self._async_save_state()

    @retry_bluetooth_connection_error
    async def set_color(self, rgb: Tuple[int, int, int], brightness: int | None = None):
        """
        Set RGB color.
        Команда: 7E 07 05 03 [R] [G] [B] 10 EF
        """
        if brightness is not None:
            self._brightness = max(1, min(int(brightness), 255))
        
        r, g, b = (max(0, min(255, c)) for c in rgb)
        self._rgb_color = (int(r), int(g), int(b))

        # Правильная команда RGB из APK
        await self._write([0x7E, 0x07, 0x05, 0x03, r, g, b, 0x10, 0xEF])

        self._is_on = True
        await self._async_save_state()

    @retry_bluetooth_connection_error
    async def set_effect(self, value: int):
        """
        Set effect.
        Команда: 7E 05 03 [EFFECT_ID] 06 FF FF 00 EF
        """
        try:
            await self._ensure_connected()
            if value in (0x00, None):
                await self.set_color(self._rgb_color, self._brightness)
                self._last_effect = None
                return
            
            # Правильная команда эффекта из APK
            await self._write([0x7E, 0x05, 0x03, value, 0x06, 0xFF, 0xFF, 0x00, 0xEF])
            self._last_effect = value
            LOGGER.debug("%s: set effect 0x%02X", self.name, value)
        except Exception as e:
            LOGGER.error("%s: set_effect error: %s", self.name, e)

    @retry_bluetooth_connection_error
    async def set_scene(self, scene_id: int):
        """
        Set scene (1-28).
        Команда для сцен: 7E 05 31 [SCENE_ID] 07 FF FF 01 EF
        ВАЖНО: Сцены используют ДРУГУЮ команду (0x31 вместо 0x03)!
        """
        try:
            await self._ensure_connected()
            scene_id = max(1, min(int(scene_id), 28))
            
            # Правильная команда сцены из APK
            await self._write([0x7E, 0x05, 0x31, scene_id, 0x07, 0xFF, 0xFF, 0x01, 0xEF])
            self._last_effect = scene_id
            LOGGER.debug("%s: set scene %d", self.name, scene_id)
        except Exception as e:
            LOGGER.error("%s: set_scene error: %s", self.name, e)

    @retry_bluetooth_connection_error
    async def set_effect_speed(self, speed: int):
        """
        Set effect speed (0-100).
        Команда: 7E 04 02 [SPEED] FF FF FF 00 EF
        """
        s = max(0, min(int(speed), 100))
        self._effect_speed = s
        await self._write([0x7E, 0x04, 0x02, s, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])
        LOGGER.debug("%s: set speed %d", self.name, s)

    @retry_bluetooth_connection_error
    async def set_effect_brightness(self, brightness: int):
        """
        Set effect brightness (0-100) without switching to RGB mode.
        Команда: 7E 04 01 [BRIGHTNESS] FF FF FF 00 EF
        
        ВАЖНО: Эта команда меняет яркость текущего эффекта без переключения в RGB режим!
        """
        b = max(0, min(int(brightness), 100))
        await self._write([0x7E, 0x04, 0x01, b, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])
        LOGGER.debug("%s: set effect brightness %d", self.name, b)

    @retry_bluetooth_connection_error
    async def set_microphone(self, enabled: bool):
        """
        Enable/disable microphone mode.
        Команда: 7E 04 07 [01/00] FF FF FF 00 EF
        
        ВАЖНО: При включении микрофона нужно сначала выключить эффект!
        """
        if enabled:
            # Сначала выключаем эффект (устанавливаем статичный цвет)
            await self.set_color(self._rgb_color, self._brightness)
            await asyncio.sleep(0.2)
        
        value = 0x01 if enabled else 0x00
        await self._write([0x7E, 0x04, 0x07, value, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])
        LOGGER.debug("%s: microphone %s", self.name, "enabled" if enabled else "disabled")

    @retry_bluetooth_connection_error
    async def set_microphone_sensitivity(self, sensitivity: int):
        """
        Set microphone sensitivity (0-100).
        Команда: 7E 04 06 [SENSITIVITY] FF FF FF 00 EF
        """
        s = max(0, min(int(sensitivity), 100))
        await self._write([0x7E, 0x04, 0x06, s, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])
        LOGGER.debug("%s: microphone sensitivity %d", self.name, s)

    @retry_bluetooth_connection_error
    async def set_microphone_eq_mode(self, mode: int):
        """
        Set microphone EQ mode (0x80-0x87).
        Команда: 7E 07 03 [MODE] 04 FF FF 00 EF
        где MODE = 0x80-0x87 (128-135)
        """
        m = max(0x80, min(int(mode), 0x87))
        await self._write([0x7E, 0x07, 0x03, m, 0x04, 0xFF, 0xFF, 0x00, 0xEF])
        LOGGER.debug("%s: microphone EQ mode 0x%02X", self.name, m)

    async def stop(self):
        """Stop and disconnect."""
        await self._async_save_state()
        if self._client and self._client.is_connected:
            await self._client.disconnect()
