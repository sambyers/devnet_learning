import requests
from config import headers, hosts
import json


requests.packages.urllib3.disable_warnings()

def delete_interface(url, username, password, headers, intfname):
    url = url + f'/data/ietf-interfaces:interfaces/interface={intfname}'
    resp = requests.delete(url, auth=(username, password), headers=headers, verify=False)
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
        interface_name = device_config['ietf-interfaces:interface']['name']

        print(f'\n-> Running Delete Interface for {hostname}')
        delete = delete_interface(base_url, username, password, headers, interface_name)
        print('\n-> Interface deleted. ' + str(delete))
