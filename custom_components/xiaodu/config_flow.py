from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant.data_entry_flow import FlowResult

import homeassistant.helpers.config_validation as cv
from homeassistant.core import callback
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry

from .const import DOMAIN

class SimpleConfigFlow(ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
    
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            errors = {}
            DATA_SCHEMA = vol.Schema({})
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

        return self.async_create_entry(title=DOMAIN, data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(entry: ConfigEntry):
        return OptionsFlowHandler(entry)


class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is None:
            options = self.config_entry.options
            errors = {}
            DATA_SCHEMA = vol.Schema({
                vol.Optional("apiKey", default=options.get('apiKey', '')): str,
                vol.Optional("debug", default=options.get('debug', False)): bool,
            })
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
        # 选项更新
        return self.async_create_entry(title='', data=user_input)