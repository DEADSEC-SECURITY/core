"""The SMA Manager integration."""

from sma_manager_api.SMA import SMA

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform, CONF_PORT, CONF_NAME, CONF_HOST

from .const import CONF_REFRESH_INTERVAL, DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry) -> bool:
    """Set up an SMA Manager config entry."""

    data = config.data
    sma = SMA(
        data[CONF_NAME], data[CONF_HOST], data[CONF_PORT], data[CONF_REFRESH_INTERVAL]
    )

    if not sma.available:
        raise ConfigEntryNotReady(
            f"Timeout while connecting socket at {data[CONF_HOST]}"
        )

    hass.data.setdefault(DOMAIN, {})[config.entry_id] = sma

    # Configure platforms
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config, platform)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, config: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(config, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(config.entry_id)

    return unload_ok
