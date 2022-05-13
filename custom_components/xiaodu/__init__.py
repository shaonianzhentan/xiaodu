import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

# 授权
from typing import Optional
import homeassistant.auth.models as models
from homeassistant.auth.const import ACCESS_TOKEN_EXPIRATION
from datetime import timedelta

from .xiaodu_view import XiaoduView
from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = cv.deprecated(DOMAIN)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data[DOMAIN] = entry.options
    
    hass.http.register_view(XiaoduView)

    # 创建刷新token
    async def async_create_refresh_token(
        self,
        user: models.User, 
        client_id: Optional[str] = None,
        client_name: Optional[str] = None,
        client_icon: Optional[str] = None,
        token_type: str = models.TOKEN_TYPE_NORMAL,
        access_token_expiration: timedelta = ACCESS_TOKEN_EXPIRATION,
        credential: models.Credentials = None,
    ) -> models.RefreshToken:
        # 如果是小度或天猫精灵，则给它们十年的授权
        if client_id is not None and ['https://open.bot.tmall.com', 'https://xiaodu.baidu.com'].count(client_id.strip('/')) > 0:
            access_token_expiration = timedelta(hours=87600)
            _LOGGER.debug('如果是小度或天猫精灵，则给它们十年的授权')
        """Create a new token for a user."""
        kwargs = {
            'user': user,
            'client_id': client_id,
            'token_type': token_type,
            'access_token_expiration': access_token_expiration
        }
        if client_name:
            kwargs['client_name'] = client_name
        if client_icon:
            kwargs['client_icon'] = client_icon

        refresh_token = models.RefreshToken(**kwargs)
        user.refresh_tokens[refresh_token.id] = refresh_token

        hass.auth._store._async_schedule_save()
        return refresh_token

    # 重写刷新token方法
    hass.auth._store.async_create_refresh_token = async_create_refresh_token

    entry.async_on_unload(entry.add_update_listener(update_listener))

        
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True

async def update_listener(hass, entry):
    """Handle options update."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)