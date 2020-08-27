import requests


requests.packages.urllib3.disable_warnings()

class DNAC():
    def __init__(self, host, username, password):
        super().__init__()
        self.host = host
        self.username = username
        self.password = password
        self.base_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.token = self.auth()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Auth-Token': self.token
        }

    def auth(self):
        path = f'{self.host}/dna/system/api/v1/auth/token'
        resp = requests.post(path, auth=(self.username, self.password), headers=self.base_headers, verify=False)
        resp.raise_for_status()
        resp_json = resp.json()
        return resp_json.get('Token')

    def get_site_health(self):
        path = f'{self.host}/dna/intent/api/v1/site-health'
        resp = requests.get(path, headers=self.headers, verify=False)
        resp.raise_for_status()
        return resp.json()

    def get_wireless_site_health(self):
        site_health = self.get_site_health()
        wireless_health = []
        for site in site_health.get('response'):
            wifi = {k:v for k,v in site.items() if 'wireless' in k or 'siteName' in k}
            wireless_health.append(wifi)
        return wireless_health