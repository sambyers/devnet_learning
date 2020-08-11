''' Example with the UCS API'''
import http.client
import argparse
import xml.etree.ElementTree


class UCS:
    def __init__(self, host, username, password):
        # Store argument values and instantiate the HTTPConnection class
        self.host = host
        self.username = username
        self.password = password
        self.cookie = None
        self.conn = http.client.HTTPConnection(self.host)

    def api_request(self, body):
        # Initiate the request
        self.conn.request('POST', '/nuova', body)
        
        # Read the response
        api_response = self.conn.getresponse()
        
        # Store the status and data
        status = api_response.status
        data = api_response.read()

        return (status, data)

    def login(self):
        body = f'<aaaLogin inName="{self.username}" inPassword="{self.password}" />'

        response = self.api_request(body)
        if response[0] == 200:
            response_xml = xml.etree.ElementTree.fromstring(response[1])
            self.cookie = response_xml.attrib['outCookie']
            return self.cookie

    def logout(self):
        body = f'<aaaLogout inCookie="{self.cookie}" />'
        
        self.api_request(body)

    def get_service_profile_templates(self):
        body = f'<configResolveClasses cookie="{self.cookie}"><inIds><classId value="lsServer"/></inIds></configResolveClasses>'

        response = self.api_request(body)
        response_xml = xml.etree.ElementTree.fromstring(response[1])
            
        templates = {}
        out_configs = response_xml.find('outConfigs')
        for server in out_configs:
            if server.attrib['type'] == 'initial-template':
                templates[server.attrib['name']] = server.attrib['dn']

        return templates

    def create_service_profile(self, name, template):
        body = (
            f'<configConfMo dn="" cookie="{self.cookie}"><inConfig>'
            f'    <lsServer dn="org-root/ls-{name}"'
            f'                     name="{name}"'
            f'                     srcTemplName="{template}"/>'
            f'  </inConfig></configConfMo>'
        )
        response = self.api_request(body)
        return response

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--ucsm', required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--template', required=True)
    parser.add_argument('--prefix', required=True)
    parser.add_argument('--count', type=int, default=1)
    args = parser.parse_args()

    ucs = UCS(args.ucsm, args.user, args.password)
    ucs.login()
    if args.template in ucs.get_service_profile_templates():
        for i in range(args.count):
            name = f'{args.prefix}{str(i)}'
            response = ucs.create_service_profile(name, args.template)
            if response[0] == 200 and 'errorCode' not in str(response[1]):
                print(f'The service profile {name} created successfully.')
    ucs.logout()