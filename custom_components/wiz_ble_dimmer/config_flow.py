"""User-configurable setup for an unofficial 2026 WiZ Bluetooth dimmer."""

import re
import voluptuous as vol

from homeassistant import config_entries

from .const import CONF_MAC, DOMAIN

_MAC_RE = re.compile(r"(?:[0-9A-F]{2}:){5}[0-9A-F]{2}")


class WizBleDimmerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Add one Bluetooth remote by its actual address."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            address = user_input[CONF_MAC].strip().upper()
            if not _MAC_RE.fullmatch(address):
                errors[CONF_MAC] = "invalid_mac"
            else:
                await self.async_set_unique_id(address)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"WiZ Bluetooth Dimmer ({address[-8:]})",
                    data={CONF_MAC: address},
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_MAC): str}),
            errors=errors,
        )
