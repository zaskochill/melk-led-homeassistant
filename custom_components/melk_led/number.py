"""Number platform for MELK LED Strip - Microphone sensitivity and Effect speed."""
from __future__ import annotations
import logging
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers import device_registry

from .const import DOMAIN
from .elkbledom import BLEDOMInstance

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up MELK LED number entities."""
    instance: BLEDOMInstance = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MELKLEDMicrophoneSensitivity(instance, entry.data["name"], entry.entry_id),
        MELKLEDEffectSpeed(instance, entry.data["name"], entry.entry_id),
        MELKLEDEffectBrightness(instance, entry.data["name"], entry.entry_id),
    ])


class MELKLEDMicrophoneSensitivity(NumberEntity):
    """Microphone sensitivity control (0-100%)."""

    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:microphone"

    def __init__(self, instance: BLEDOMInstance, name: str, entry_id: str) -> None:
        self._instance = instance
        self._attr_name = f"{name} Microphone Sensitivity"
        self._entry_id = entry_id
        self._attr_unique_id = f"{self._instance.address}_mic_sensitivity"
        self._attr_native_value = 50  # Default

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._instance.address)},
            name=self._attr_name.replace(" Microphone Sensitivity", ""),
            manufacturer="MELK",
            model="LED Strip Controller",
            connections={(device_registry.CONNECTION_NETWORK_MAC, self._instance.address)},
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set microphone sensitivity (0-100)."""
        sensitivity = int(value)
        await self._instance.set_microphone_sensitivity(sensitivity)
        self._attr_native_value = sensitivity
        self.async_write_ha_state()


class MELKLEDEffectSpeed(NumberEntity):
    """Effect speed control (0-100)."""

    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:speedometer"

    def __init__(self, instance: BLEDOMInstance, name: str, entry_id: str) -> None:
        self._instance = instance
        self._attr_name = f"{name} Effect Speed"
        self._entry_id = entry_id
        self._attr_unique_id = f"{self._instance.address}_effect_speed"
        self._attr_native_value = 50  # Default

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._instance.address)},
            name=self._attr_name.replace(" Effect Speed", ""),
            manufacturer="MELK",
            model="LED Strip Controller",
            connections={(device_registry.CONNECTION_NETWORK_MAC, self._instance.address)},
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set effect speed (0-100)."""
        speed = int(value)
        await self._instance.set_effect_speed(speed)
        self._attr_native_value = speed
        self.async_write_ha_state()


class MELKLEDEffectBrightness(NumberEntity):
    """Effect brightness control (0-100) - separate from RGB brightness."""

    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:brightness-6"

    def __init__(self, instance: BLEDOMInstance, name: str, entry_id: str) -> None:
        self._instance = instance
        self._attr_name = f"{name} Effect Brightness"
        self._entry_id = entry_id
        self._attr_unique_id = f"{self._instance.address}_effect_brightness"
        self._attr_native_value = 100  # Default

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._instance.address)},
            name=self._attr_name.replace(" Effect Brightness", ""),
            manufacturer="MELK",
            model="LED Strip Controller",
            connections={(device_registry.CONNECTION_NETWORK_MAC, self._instance.address)},
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set effect brightness (0-100) without switching to RGB mode."""
        brightness = int(value)
        await self._instance.set_effect_brightness(brightness)
        self._attr_native_value = brightness
        self.async_write_ha_state()
