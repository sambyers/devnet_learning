import requests
from intersight_auth import IntersightAuth


class RestClient(object):
    def __init__(self, base_url, api_key_id, secret_key_file):
        self.base_url = base_url
        self.api_key_id = api_key_id
        self.secret_key_file = secret_key_file
        self.auth = IntersightAuth(
            secret_key_filename = self.secret_key_file,
            api_key_id = self.api_key_id
        )

    def get(self, url):
        url = self.base_url + url
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def delete(self, url):
        url = self.base_url + url
        response = requests.delete(url, auth=self.auth)
        response.raise_for_status()
        return response.status_code
