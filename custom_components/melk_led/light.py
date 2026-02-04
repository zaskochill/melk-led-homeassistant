"""MELK LED Strip light platform with correct commands from Magic Lantern APK."""
from __future__ import annotations
import logging
from homeassistant.components.light import (
    ColorMode,
    LightEntity,
    LightEntityFeature,
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR,
    ATTR_EFFECT,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers import device_registry

from .const import (
    DOMAIN,
    ALL_EFFECTS_MAP,
    ALL_EFFECT_LABELS,
    SCENES_MAP,
)
from .elkbledom import BLEDOMInstance

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up MELK LED light from config entry."""
    instance: BLEDOMInstance = hass.data[DOMAIN][entry.entry_id]
    light_entity = MELKLEDLight(instance, entry.data["name"], entry.entry_id)
    
    # Сохраняем ссылку на light entity в instance для доступа из switch
    instance._light_entity = light_entity
    
    async_add_entities([light_entity])


class MELKLEDLight(RestoreEntity, LightEntity):
    """MELK LED Strip RGB light with correct protocol commands."""

    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB
    _attr_supported_features = LightEntityFeature.EFFECT
    # Указываем, что состояние предполагаемое (assumed)
    # потому что Bluetooth устройство не может отправлять состояние обратно
    _attr_assumed_state = True

    def __init__(self, instance: BLEDOMInstance, name: str, entry_id: str) -> None:
        self._instance = instance
        self._attr_name = name
        self._entry_id = entry_id
        self._attr_unique_id = f"{self._instance.address}_light"

        # Текущий эффект (ключ из const)
        self._current_effect_key: str = "none"
        
        # Последний эффект перед микрофоном (для восстановления)
        self._last_effect_before_mic: str = "none"
        
        # Флаг, что состояние восстановлено
        self._restored = False

        # Подготовим красивые списки для UI (эффекты + сцены)
        pretty = []
        for key in ["none"] + [k for k in ALL_EFFECTS_MAP.keys() if k != "none"]:
            pretty.append(ALL_EFFECT_LABELS.get(key, key))

        self._pretty_effect_list = pretty
        self._key2pretty = {k: ALL_EFFECT_LABELS.get(k, k) for k in ALL_EFFECTS_MAP.keys()}
        self._pretty2key = {v: k for k, v in self._key2pretty.items()}
    
    async def async_added_to_hass(self) -> None:
        """Restore state when entity is added to hass."""
        await super().async_added_to_hass()
        
        # Восстанавливаем последнее состояние
        last_state = await self.async_get_last_state()
        if last_state:
            _LOGGER.info("Restoring last state: %s", last_state.state)
            
            # Восстанавливаем состояние ON/OFF
            self._instance._is_on = last_state.state == "on"
            
            # Восстанавливаем эффект
            if last_state.attributes.get(ATTR_EFFECT):
                effect_label = last_state.attributes[ATTR_EFFECT]
                self._current_effect_key = self._pretty2key.get(effect_label, "none")
                _LOGGER.info("Restored effect: %s", effect_label)
            
            self._restored = True
            _LOGGER.info("State restored: is_on=%s, effect=%s", 
                        self._instance._is_on, self._current_effect_key)
        else:
            _LOGGER.info("No previous state found, using defaults")

    @property
    def is_on(self):
        return self._instance.is_on

    @property
    def brightness(self):
        return self._instance.brightness

    @property
    def rgb_color(self):
        return self._instance.rgb_color

    @property
    def color_mode(self):
        return ColorMode.RGB

    @property
    def effect(self) -> str | None:
        return self._key2pretty.get(self._current_effect_key, "none")

    @property
    def effect_list(self) -> list[str] | None:
        return self._pretty_effect_list

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._instance.address)},
            name=self._attr_name,
            manufacturer="MELK",
            model="LED Strip Controller",
            connections={(device_registry.CONNECTION_NETWORK_MAC, self._instance.address)},
        )
    
    def save_state_before_microphone(self) -> None:
        """Save current effect before enabling microphone."""
        self._last_effect_before_mic = self._current_effect_key
        _LOGGER.info("Saved effect before microphone: %s", self._last_effect_before_mic)
    
    async def restore_state_after_microphone(self) -> None:
        """Restore effect after disabling microphone."""
        if self._last_effect_before_mic and self._last_effect_before_mic != "none":
            _LOGGER.info("Restoring effect after microphone: %s", self._last_effect_before_mic)
            
            # Восстанавливаем эффект
            if self._last_effect_before_mic.startswith("scene_"):
                scene_name = self._last_effect_before_mic[6:]
                if scene_name in SCENES_MAP:
                    scene_id = SCENES_MAP[scene_name]
                    await self._instance.set_scene(scene_id)
                    self._current_effect_key = self._last_effect_before_mic
                    _LOGGER.info("Restored scene: %s (id=%d)", self._last_effect_before_mic, scene_id)
            elif self._last_effect_before_mic in ALL_EFFECTS_MAP:
                effect_id = ALL_EFFECTS_MAP[self._last_effect_before_mic]
                await self._instance.set_effect(effect_id)
                self._current_effect_key = self._last_effect_before_mic
                _LOGGER.info("Restored effect: %s (0x%02X)", self._last_effect_before_mic, effect_id)
        else:
            # Нет эффекта - восстанавливаем статичный цвет
            _LOGGER.info("Restoring static color after microphone")
            await self._instance.set_color(self._instance.rgb_color)
            self._current_effect_key = "none"
        
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Turn on the light with correct commands."""
        _LOGGER.debug("Turn ON with kwargs: %s", kwargs)
        
        # Если включаем без параметров - восстанавливаем последний режим
        if not kwargs:
            _LOGGER.info("Turning on without params - restoring last state")
            await self._instance.turn_on()
            
            # Восстанавливаем последний эффект или цвет
            if self._current_effect_key and self._current_effect_key != "none":
                _LOGGER.info("Restoring last effect: %s", self._current_effect_key)
                
                # Проверяем, это сцена или обычный эффект
                if self._current_effect_key.startswith("scene_"):
                    scene_name = self._current_effect_key[6:]
                    if scene_name in SCENES_MAP:
                        scene_id = SCENES_MAP[scene_name]
                        await self._instance.set_scene(scene_id)
                        _LOGGER.info("Restored scene: %s (id=%d)", self._current_effect_key, scene_id)
                elif self._current_effect_key in ALL_EFFECTS_MAP:
                    effect_id = ALL_EFFECTS_MAP[self._current_effect_key]
                    await self._instance.set_effect(effect_id)
                    _LOGGER.info("Restored effect: %s (0x%02X)", self._current_effect_key, effect_id)
            else:
                # Нет эффекта - восстанавливаем статичный цвет
                _LOGGER.info("Restoring static color")
                await self._instance.set_color(self._instance.rgb_color)
            
            self.async_write_ha_state()
            return
        
        # Если меняем эффект или цвет - выключаем микрофон
        if ATTR_EFFECT in kwargs or ATTR_RGB_COLOR in kwargs:
            # Получаем entity_id света из registry
            if not hasattr(self, 'entity_id') or not self.entity_id:
                _LOGGER.warning("Light entity_id not available yet")
            else:
                # Формируем entity_id микрофона
                switch_entity_id = self.entity_id.replace("light.", "switch.") + "_microphone_mode"
                _LOGGER.debug("Attempting to disable microphone: %s", switch_entity_id)
                
                if self.hass.states.get(switch_entity_id):
                    _LOGGER.info("Auto-disabling microphone: %s", switch_entity_id)
                    await self.hass.services.async_call(
                        "switch", "turn_off",
                        {"entity_id": switch_entity_id},
                        blocking=False
                    )
                else:
                    _LOGGER.warning("Microphone switch not found: %s (available entities: %s)", 
                                  switch_entity_id, 
                                  [e for e in self.hass.states.async_entity_ids() if 'microphone' in e])
        
        await self._instance.turn_on()

        if ATTR_BRIGHTNESS in kwargs:
            await self._instance.set_brightness(kwargs[ATTR_BRIGHTNESS])

        if ATTR_RGB_COLOR in kwargs:
            await self._instance.set_color(kwargs[ATTR_RGB_COLOR])
            self._current_effect_key = "none"

        if ATTR_EFFECT in kwargs:
            # Пользователь присылает красивое имя
            pretty_name = kwargs[ATTR_EFFECT]
            effect_key = self._pretty2key.get(pretty_name, pretty_name)
            
            # Проверяем, это сцена или обычный эффект
            if effect_key.startswith("scene_"):
                # Это сцена - используем другую команду
                scene_name = effect_key[6:]  # Убираем префикс "scene_"
                if scene_name in SCENES_MAP:
                    scene_id = SCENES_MAP[scene_name]
                    await self._instance.set_scene(scene_id)
                    self._current_effect_key = effect_key
                    _LOGGER.debug("Applied scene: key=%s id=%d", effect_key, scene_id)
            elif effect_key in ALL_EFFECTS_MAP:
                # Обычный эффект
                effect_id = ALL_EFFECTS_MAP[effect_key]
                await self._instance.set_effect(effect_id)
                self._current_effect_key = effect_key
                _LOGGER.debug("Applied effect: key=%s id=0x%02X", effect_key, effect_id)

        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the light."""
        _LOGGER.info("Turning off light - saving current state")
        
        # НЕ сбрасываем эффект - сохраняем для следующего включения
        # self._current_effect_key остаётся как есть
        
        # Выключаем микрофон если он был включен
        if hasattr(self, 'entity_id') and self.entity_id:
            switch_entity_id = self.entity_id.replace("light.", "switch.") + "_microphone_mode"
            if self.hass.states.get(switch_entity_id):
                mic_state = self.hass.states.get(switch_entity_id)
                if mic_state and mic_state.state == "on":
                    _LOGGER.info("Auto-disabling microphone on light turn off: %s", switch_entity_id)
                    await self.hass.services.async_call(
                        "switch", "turn_off",
                        {"entity_id": switch_entity_id},
                        blocking=False
                    )
        
        await self._instance.turn_off()
        self.async_write_ha_state()
