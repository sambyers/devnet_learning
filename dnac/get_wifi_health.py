from dnac import DNAC
import json

with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)
wifi_health = dnac.get_wireless_site_health()
print(json.dumps(wifi_health, indent=4))