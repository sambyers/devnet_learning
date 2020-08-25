import requests
import re
import json
from configuration import headers, hosts
import json


requests.packages.urllib3.disable_warnings()

def get_interface(url, username, password, headers, intfname):
    url = url + f'/data/ietf-interfaces:interfaces/interface={intfname}'
    resp = requests.get(url, auth=(username, password), headers=headers, verify=False)
    resp.raise_for_status()
    return resp.json()

def get_interface_native(url, username, password, headers, intfname):
    url = url + f'/data/native/interface/Loopback={intfname}'
    resp = requests.get(url, auth=(username, password), headers=headers, verify=False)
    resp.raise_for_status()
    return resp.json()

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

        print(f'\n-> Running Get Interface for {hostname}')
        print('\n-> Standard model')
        show = get_interface(base_url, username, password, headers, interface_name)
        print(json.dumps(show, indent=4))

        interface_number = re.findall('\d+', interface_name)
        show_native = get_interface_native(base_url, username, password, headers, interface_number[0])
        print('\n-> Native model')
        print(json.dumps(show_native, indent=4))
