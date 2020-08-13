'''Good old fashioned web scraping to generate json of IPs and URLs used by Webex for consumtion by a network appliance.'''
import re
import urllib.request
import json

# To do
# Add Webex teams clients

def webex_meetings_clients(ips: list, urls: list) -> dict:
    output = {
            "service": "WebEx Meetings Clients",
            "ips": ips,
            "urls": urls,
            "tcpPorts": "80, 443, 53",
            "udpPorts": "53, 9000"
        }
    return output

def webex_teams_clients(ips: list, urls: list) -> dict:
    output = {
            "service": "WebEx Teams Clients",
            "ips": ips,
            "urls": urls,
            "tcpPorts": "443, 5004",
            "udpPorts": "5004"
        }
    return output

def find_ips(html: str) -> list:
    ip_pattern = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}"
    ip_results = set(re.findall(ip_pattern, html))
    return list(ip_results)

def find_urls(html: str) -> list:
    url_pattern = "\*+\.[a-z0-9]+\.[a-z]+"
    url_results = set(re.findall(url_pattern, html))
    return list(url_results)

def outfile(file_input: list) -> None:
    with open('output.json', 'w') as f:
        f.write(json.dumps(file_input, indent=4))

def main():
    wbxurl = "https://help.webex.com/en-us/WBX264/How-Do-I-Allow-Webex-Meetings-Traffic-on-My-Network"
    response = urllib.request.urlopen(wbxurl)
    resaponse_str = str(response.read())
    ips = find_ips(resaponse_str)
    urls = find_urls(resaponse_str)
    meetings = webex_meetings_clients(ips, urls)
    # teams = webex_teams_clients(ips, urls)
    outfile([meetings])


if __name__ == "__main__":
    main()