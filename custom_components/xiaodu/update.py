import requests, os, _thread
from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityDescription,
    UpdateEntityFeature
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .manifest import manifest, download

NAME = manifest.name
DOMAIN = manifest.domain

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    ent = EntityUpdate(hass, entry.entry_id)
    await ent.async_update()
    async_add_entities([ ent ])

class EntityUpdate(UpdateEntity):

    _attr_supported_features = UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS
    _attr_name = DOMAIN
    _attr_title = NAME

    def __init__(self, hass, unique_id):
        self.hass = hass
        self._attr_unique_id = unique_id
        self._attr_release_url = manifest.documentation
        self._attr_in_progress = False
        
    @property
    def in_progress(self) -> bool:
        return self._in_progress

    @property
    def installed_version(self):
        return manifest.version

    async def async_install(self, version: str, backup: bool):
        self._attr_in_progress = True
        sh_file = self.hass.config.path(f'{self._attr_name}.sh')
        # download file of bash script
        url = 'https://gitee.com/shaonianzhentan/updater/raw/main/bash/install.sh'
        await download(url, sh_file)
        # execute bash script
        bash = f'sh {sh_file} main https://gitee.com/shaonianzhentan/xiaodu xiaodu xiaodu'

        _thread.start_new_thread(self.exec_script, (bash, ))

    def exec_script(self, bash):
        os.system(bash)        
        manifest.update()
        self._attr_title = f'{self._attr_name} 重启生效'
        self._in_progress = False
        # print(f'install {self._attr_name}')
        self.hass.services.call('homeassistant', 'update_entity', { 'entity_id': self.entity_id})

    async def async_update(self):
        res = await self.hass.async_add_executor_job(requests.get, (manifest.remote_url))
        data = res.json()
        self._attr_latest_version = data.get('version')