"""Switch platform for MELK LED Strip - Microphone mode."""
from __future__ import annotations
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers import device_registry

from .const import DOMAIN
from .elkbledom import BLEDOMInstance

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up MELK LED switch entities."""
    instance: BLEDOMInstance = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MELKLEDMicrophoneSwitch(instance, entry.data["name"], entry.entry_id),
    ])


class MELKLEDMicrophoneSwitch(RestoreEntity, SwitchEntity):
    """Microphone mode switch."""

    _attr_icon = "mdi:microphone"
    # Указываем, что состояние предполагаемое
    _attr_assumed_state = True

    def __init__(self, instance: BLEDOMInstance, name: str, entry_id: str) -> None:
        self._instance = instance
        self._attr_name = f"{name} Microphone Mode"
        self._entry_id = entry_id
        self._attr_unique_id = f"{self._instance.address}_microphone"
        self._attr_is_on = False
        self._hass = None
        # Entity IDs будут заполнены в async_added_to_hass
        self._eq_entity_id = None
        self._sensitivity_entity_id = None

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._hass = self.hass
        
        # Восстанавливаем последнее состояние
        last_state = await self.async_get_last_state()
        if last_state:
            self._attr_is_on = last_state.state == "on"
            _LOGGER.info("Restored microphone state: %s", self._attr_is_on)
            
            # Но если свет выключен - микрофон тоже должен быть выключен
            if not self._instance.is_on and self._attr_is_on:
                _LOGGER.info("Light is off - forcing microphone to off")
                self._attr_is_on = False

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._instance.address)},
            name=self._attr_name.replace(" Microphone Mode", ""),
            manufacturer="MELK",
            model="LED Strip Controller",
            connections={(device_registry.CONNECTION_NETWORK_MAC, self._instance.address)},
        )

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on microphone mode."""
        _LOGGER.info("Turning ON microphone mode")
        
        # Сохраняем текущий эффект перед включением микрофона
        if hasattr(self._instance, '_light_entity'):
            self._instance._light_entity.save_state_before_microphone()
        
        # Сначала выключаем эффект - устанавливаем статичный цвет
        await self._instance.set_color(self._instance.rgb_color, self._instance.brightness)
        
        # Включаем микрофон
        await self._instance.set_microphone(True)
        
        # ДОБАВЛЕНО: Отправляем чувствительность и режим эквалайзера
        import asyncio
        await asyncio.sleep(0.1)
        
        if self._hass:
            # Находим entity_id динамически через entity registry
            if not self._sensitivity_entity_id or not self._eq_entity_id:
                from homeassistant.helpers import entity_registry, device_registry
                er = entity_registry.async_get(self._hass)
                dr = device_registry.async_get(self._hass)
                
                # Находим device по identifier
                device = dr.async_get_device(identifiers=self.device_info["identifiers"])
                if device:
                    _LOGGER.info("Found device: %s", device.id)
                    device_entities = entity_registry.async_entries_for_device(er, device.id)
                    
                    for entity in device_entities:
                        if entity.entity_id.startswith("select.") and "microphone_eq_mode" in entity.entity_id:
                            self._eq_entity_id = entity.entity_id
                            _LOGGER.info("Found EQ entity: %s", self._eq_entity_id)
                        elif entity.entity_id.startswith("number.") and "microphone_sensitivity" in entity.entity_id:
                            self._sensitivity_entity_id = entity.entity_id
                            _LOGGER.info("Found sensitivity entity: %s", self._sensitivity_entity_id)
                else:
                    _LOGGER.error("Device not found in registry")
            
            # Используем динамически найденные entity_id
            if self._sensitivity_entity_id:
                sensitivity_state = self._hass.states.get(self._sensitivity_entity_id)
            else:
                _LOGGER.warning("Sensitivity entity not found")
                sensitivity_state = None
            if sensitivity_state:
                sensitivity = int(float(sensitivity_state.state))
            else:
                sensitivity = 60  # Дефолт
            await self._instance.set_microphone_sensitivity(sensitivity)
            _LOGGER.info("Set microphone sensitivity: %d", sensitivity)
            
            await asyncio.sleep(0.1)
            
            # Режим эквалайзера - ВСЕГДА отправляем
            if self._eq_entity_id:
                eq_state = self._hass.states.get(self._eq_entity_id)
                _LOGGER.info("EQ entity: %s, state: %s", self._eq_entity_id, eq_state.state if eq_state else "None")
            else:
                _LOGGER.warning("EQ entity not found")
                eq_state = None
            
            mode_sent = False
            
            if eq_state and eq_state.state != 'unavailable':
                from .const import MIC_MODES, MIC_MODE_LABELS
                current_label = eq_state.state
                _LOGGER.info("Trying to apply EQ mode from UI: '%s'", current_label)
                
                for mode in MIC_MODES:
                    label = MIC_MODE_LABELS[mode.name]
                    if label == current_label:
                        await self._instance.set_microphone_eq_mode(mode.value)
                        _LOGGER.info("✓ Applied EQ mode: %s (0x%02X)", current_label, mode.value)
                        mode_sent = True
                        break
                
                if not mode_sent:
                    _LOGGER.warning("Failed to find mode for label: '%s'", current_label)
            
            # Если не удалось отправить из UI - отправляем дефолт
            if not mode_sent:
                await self._instance.set_microphone_eq_mode(0x80)  # Energic
                _LOGGER.info("✓ Applied EQ mode: Energic (0x80) - default")
        
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off microphone mode."""
        _LOGGER.info("Turning OFF microphone mode")
        
        # Выключаем микрофон
        await self._instance.set_microphone(False)
        
        # Восстанавливаем последний эффект или статичный цвет
        import asyncio
        await asyncio.sleep(0.15)
        
        # Восстанавливаем состояние через light entity
        if hasattr(self._instance, '_light_entity'):
            _LOGGER.info("Restoring state after microphone via light entity")
            await self._instance._light_entity.restore_state_after_microphone()
        else:
            # Fallback - просто восстанавливаем цвет
            _LOGGER.info("Light entity not found, restoring static color")
            await self._instance.set_color(self._instance.rgb_color, self._instance.brightness)
        
        _LOGGER.info("Microphone disabled, state restored")
        
        self._attr_is_on = False
        self.async_write_ha_state()
    
    async def async_update(self) -> None:
        """Update microphone state based on light state."""
        # Если свет выключен - микрофон тоже должен быть выключен
        if not self._instance.is_on and self._attr_is_on:
            _LOGGER.info("Light is off - auto-disabling microphone state")
            self._attr_is_on = False
            self.async_write_ha_state()
