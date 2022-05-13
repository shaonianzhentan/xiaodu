import json, logging, time
from homeassistant.components.http import HomeAssistantView

from .const import DOMAIN, XIAODU_API
from .xiaodu import discoveryDevice, controlDevice, queryDevice

_LOGGER = logging.getLogger(__name__)

class XiaoduView(HomeAssistantView):

    url = XIAODU_API
    name = XIAODU_API[1:].replace('/', ':')
    requires_auth = False

    async def post(self, request):
        hass = request.app["hass"]
        data = await request.json()
        options = hass.data[DOMAIN]
        if options.get('debug', False) == True:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '接收信息',
                'message': json.dumps(data)
            })
        header = data['header']
        payload = data['payload']
        name = header['name']
        accessToken = payload['accessToken']
        # 正常授权验证
        token = await hass.auth.async_validate_access_token(accessToken)
        # 进行自定义服务验证
        if token is None:
            apiKey = options.get('apiKey', '')
            # 判断是否定义apiKey
            if apiKey != '' and accessToken == f'apiKey{apiKey}':
                token = accessToken
        # 走正常流程
        result = {}
        if token is not None:
            namespace = header['namespace']
            if namespace == 'DuerOS.ConnectedHome.Discovery':
                # 发现设备
                result = await discoveryDevice(hass)
                name = 'DiscoverAppliancesResponse'
            elif namespace == 'DuerOS.ConnectedHome.Control':
                # 控制设备
                result = await controlDevice(hass, name, payload)
                if result is None:
                    name = 'UnsupportedOperationError'
                else:
                    name = name.replace('Request', 'Confirmation')
            elif namespace == 'DuerOS.ConnectedHome.Query':
                # 查询设备
                result = queryDevice(hass, name, payload)
                name = name.replace('Request', 'Response')
        else:
            name = 'InvalidAccessTokenError'

        header['name'] = name
        # 如果包含Uid则返回用户ID
        if 'openUid' in payload:
            result['openUid'] = payload['openUid']
        response = {'header': header, 'payload': result}
        
        if options.get('debug', False) == True:
            await hass.services.async_call('persistent_notification', 'create', {
                'title': '发送信息',
                'message': json.dumps(response)
            })
        return self.json(response)