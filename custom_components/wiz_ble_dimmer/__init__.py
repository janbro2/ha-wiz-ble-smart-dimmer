"""Unofficial Home Assistant integration for the 2026 WiZ BLE Smart Dimmer.

Emits ``wiz_dimmer_button`` events; does not directly control any devices.
"""

import logging
from time import monotonic

from homeassistant.components import bluetooth
from homeassistant.components.bluetooth.models import BluetoothCallbackReplay
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .const import CONF_MAC, DOMAIN, EVENT_NAME, MANUFACTURER_ID
from .decoder import decode_button

_LOGGER = logging.getLogger(__name__)
_DEBOUNCE_SECONDS = 0.35


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Subscribe to advertisement data for one configured dimmer."""
    address = entry.data[CONF_MAC].upper()
    last_code: str | None = None
    last_fired_at = 0.0

    @callback
    def on_advertisement(
        service_info: bluetooth.BluetoothServiceInfoBleak,
        change: bluetooth.BluetoothChange,
    ) -> None:
        nonlocal last_code, last_fired_at

        if service_info.address.upper() != address:
            return
        data = service_info.manufacturer_data.get(MANUFACTURER_ID)
        if not data:
            return

        decoded = decode_button(data, address)
        if decoded is None:
            _LOGGER.debug("Unrecognized WiZ BLE manufacturer payload")
            return

        action, code = decoded
        now = monotonic()
        if code == last_code and now - last_fired_at < _DEBOUNCE_SECONDS:
            return
        last_code, last_fired_at = code, now

        hass.bus.async_fire(
            EVENT_NAME,
            {
                "address": address,
                "action": action,
                "code": code,
                "rssi": service_info.rssi,
            },
        )
        _LOGGER.debug("WiZ dimmer button %s (%s) received", action, code)

    entry.async_on_unload(
        bluetooth.async_register_callback(
            hass,
            on_advertisement,
            {
                "address": address,
                "manufacturer_id": MANUFACTURER_ID,
                "connectable": False,
            },
            bluetooth.BluetoothScanningMode.PASSIVE,
            replay=BluetoothCallbackReplay.DISABLED,
        )
    )
    _LOGGER.info("WiZ BLE Smart Dimmer listening for configured remote")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Home Assistant removes the Bluetooth callback registered on this entry."""
    return True
