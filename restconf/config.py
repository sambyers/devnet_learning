# Configuration file
import json


with open('hosts.json', 'r') as f:
    hosts = json.loads(f.read())

headers = {
    'Accept': 'application/yang-data+json',
    'Content-Type': 'application/yang-data+json'
}
