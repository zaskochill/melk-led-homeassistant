"""MELK LED Strip integration for Home Assistant."""
from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event
from homeassistant.const import CONF_MAC, EVENT_HOMEASSISTANT_STOP, Platform

from .const import DOMAIN, CONF_RESET, CONF_DELAY
from .elkbledom import BLEDOMInstance

LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.LIGHT,
    Platform.NUMBER,
    Platform.SWITCH,
    Platform.SELECT,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MELK LED Strip from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Получаем параметры
    reset = entry.options.get(CONF_RESET, entry.data.get(CONF_RESET, False))
    delay = entry.options.get(CONF_DELAY, entry.data.get(CONF_DELAY, 120))
    mac = entry.data.get(CONF_MAC) or entry.options.get(CONF_MAC)

    if not mac:
        LOGGER.error("MELK LED: MAC address missing in entry %s", entry.entry_id)
        return False

    LOGGER.info("Initializing MELK LED: MAC=%s | reset=%s | delay=%s", mac, reset, delay)

    # Создаем экземпляр устройства
    instance = BLEDOMInstance(mac, reset, delay, hass)
    hass.data[DOMAIN][entry.entry_id] = instance

    # Регистрируем платформы
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Обработчик обновления параметров
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    # Гарантированное отключение при остановке HA
    async def _async_stop(event: Event) -> None:
        LOGGER.debug("Stopping MELK LED (%s) due to HA shutdown", mac)
        await instance.stop()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _async_stop)
    )

    LOGGER.info("MELK LED integration successfully loaded for %s", mac)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    LOGGER.info("Unloading MELK LED: %s", entry.entry_id)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        instance: BLEDOMInstance = hass.data[DOMAIN].pop(entry.entry_id, None)
        if instance:
            await instance.stop()
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    LOGGER.debug("Reloading MELK LED after options change")
    await hass.config_entries.async_reload(entry.entry_id)
