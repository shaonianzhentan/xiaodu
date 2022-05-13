import os, json, aiohttp

def load_json(file_path):
    # 不存在则返回空字典
    if os.path.exists(file_path) == False:
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

async def download(url, file_path):
    headers = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
    connector = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        async with session.get(url) as response:
            file = await response.read()
            with open(file_path, 'wb') as f:
                f.write(file)

class Manifest():

    def __init__(self, domain):
        self.domain = domain
        self.update()

    @property
    def remote_url(self):
        return 'https://gitee.com/shaonianzhentan/xiaodu/raw/main/custom_components/xiaodu/manifest.json'

    def update(self):
        data = load_json(os.path.abspath(f'./custom_components/{self.domain}/manifest.json'))
        self.name = data.get('name')
        self.version = data.get('version')
        self.documentation = data.get('documentation')

manifest = Manifest('xiaodu')