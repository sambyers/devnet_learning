from ydk.providers import NetconfServiceProvider
from ydk.services import CRUDService
from ydk.models.openconfig import openconfig_bgp
import json


def config_native(native):
    """Add config data to native object."""
    loopback = native.interface.Loopback()
    loopback.name = 0
    loopback.description = "PRIMARY ROUTER LOOPBACK"
    loopback.ip.address.primary.address = "172.16.255.1"
    loopback.ip.address.primary.mask = "255.255.255.255"
    native.interface.loopback.append(loopback)

if __name__ == "__main__":
    with open('hosts.json', 'r') as fh:
        hosts = json.loads(fh.read())
    host = hosts[0]
    provider = NetconfServiceProvider(address=host.get('host'),
                                     port=int(host.get('netconf_port')),
                                     username=host.get('username'),
                                     password=host.get('password'),
                                     protocol='ssh')
    crud = CRUDService()

    bgp = openconfig_bgp.Bgp()

    bgp.global_.config.as_ = 65001
    bgp.global_.config.router_id = '10.0.0.1'

    result = crud.create(provider, bgp)