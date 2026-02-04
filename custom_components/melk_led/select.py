"""Select platform for MELK LED Strip - Microphone EQ mode."""
from __future__ import annotations
import logging
from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers import device_registry

from .const import DOMAIN, MIC_MODES, MIC_MODE_LABELS
from .elkbledom import BLEDOMInstance

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up MELK LED select entities."""
    instance: BLEDOMInstance = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MELKLEDMicrophoneEQMode(instance, entry.data["name"], entry.entry_id),
    ])


class MELKLEDMicrophoneEQMode(SelectEntity):
    """Microphone EQ mode selector."""

    _attr_icon = "mdi:equalizer"

    def __init__(self, instance: BLEDOMInstance, name: str, entry_id: str) -> None:
        self._instance = instance
        self._attr_name = f"{name} Microphone EQ Mode"
        self._entry_id = entry_id
        self._attr_unique_id = f"{self._instance.address}_mic_eq_mode"
        
        # Prepare options list with pretty labels
        self._attr_options = [MIC_MODE_LABELS[mode.name] for mode in MIC_MODES]
        self._attr_current_option = MIC_MODE_LABELS["energic"]  # Default
        
        # Maps for conversion
        self._label_to_mode = {MIC_MODE_LABELS[mode.name]: mode.value for mode in MIC_MODES}
        self._mode_to_label = {mode.value: MIC_MODE_LABELS[mode.name] for mode in MIC_MODES}

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._instance.address)},
            name=self._attr_name.replace(" Microphone EQ Mode", ""),
            manufacturer="MELK",
            model="LED Strip Controller",
            connections={(device_registry.CONNECTION_NETWORK_MAC, self._instance.address)},
        )

    async def async_select_option(self, option: str) -> None:
        """Select EQ mode."""
        mode_value = self._label_to_mode.get(option)
        if mode_value is not None:
            await self._instance.set_microphone_eq_mode(mode_value)
            self._attr_current_option = option
            self.async_write_ha_state()
