import requests
from config import headers, hosts
import json


requests.packages.urllib3.disable_warnings()

def add_interface(url, username, password, headers, body):
    url = url + '/data/ietf-interfaces:interfaces'
    resp = requests.post(url, auth=(username, password), headers=headers, json=body, verify=False)
    resp.raise_for_status()
    return resp.status_code

if __name__ == '__main__':
    for host in hosts:
        hostname = host.get("host")
        with open(f'{hostname}/interface.json', 'r') as f:
            device_config = json.loads(f.read())

        username = host.get('username')
        password = host.get('password')
        restconf_port = host.get("restconf_port")
        base_url = f'https://{hostname}:{restconf_port}/restconf'

        print(f'\n-> Running Set Interface for host {hostname}')
        create = add_interface(base_url, username, password, headers, device_config)
        print('\n-> Created interface. ' + str(create))
