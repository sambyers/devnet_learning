import requests
from time import sleep

class FDMClient():
    def __init__(self, ip=None, port='443', username=None, password=None, log=None):
        super().__init__()
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        assert log
        self.log = log
        self.token = None
        self.base_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.base_url = '/api/fdm/v5'
        self.auth_headers = None
        self._policy_id = None

    def request(self, url, method='get', headers=None, body=None, params=None):
        if not headers:
            headers = self.base_headers
        requrl = f'https://{self.ip}:{self.port}{self.base_url}{url}'
        reqmethod = getattr(requests, method)
        self.log.debug(f'Sending request to {requrl}')
        resp = reqmethod(requrl, verify=False, headers=headers, json=body, params=params)
        resp.raise_for_status()
        if resp.status_code == 204:
            return None
        resp_json = resp.json()
        paging = resp_json.get('paging')
        if paging:
            if paging.get('next'):
                count = resp_json['paging']['count']
                params = {'limit': count}
                self.log.debug('Requesting additional pages of data from FDM.')
                resp = reqmethod(requrl, verify=False, headers=headers, json=body, params=params)
                resp_json = resp.json()
        return resp_json
    
    def login(self):
        if self.token:
            self.log.debug('Already logged in.')
            return None
        path = '/fdm/token'
        body = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }
        self.log.debug('Logging into the FDM host.')
        resp = self.request(path, method='post', body=body)
        self.log.debug('Login successful.')
        self.token = resp.get('access_token')
        self.auth_headers = self.get_auth_headers()
        return resp
    
    def logout(self):
        if self.token is None:
            self.log.debug('Not logged in.')
            return None
        path = '/fdm/token'
        body = {
            'grant_type': 'revoke_token',
            'access_token': self.token,
            'token_to_revoke': self.token
        }
        self.log.debug('Logging out of the FDM host.')
        resp = self.request(path, method='post', body=body)
        self.log.debug('Logout successful.')
        self.token = None
        self.auth_headers = None
        return resp

    def get_auth_headers(self):
        auth_headers = self.base_headers
        auth_headers['Authorization'] = f'Bearer {self.token}'
        return auth_headers
    
    @property
    def policy_id(self):
        if self._policy_id is None:
            path = '/policy/accesspolicies'
            self.log.debug('Getting access policy from FDM.')
            resp = self.request(path, headers=self.auth_headers)
            policy_id = resp['items'][0]['id']
            self.log.debug(f'Retrieving Policy ID: {policy_id}')
            self._policy_id = policy_id
        return self._policy_id

    def get_access_rule_by_name(self, name):
        self.log.debug('Searching for access rule.')
        path = f'/policy/accesspolicies/{self.policy_id}/accessrules'
        self.log.debug('Requesting access rules from FDM.')
        resp = self.request(path, headers=self.auth_headers)
        self.log.debug('Access rule by name request was successful.')
        access_rules = resp.get('items')
        
        rule_data = None
        for access_rule in access_rules:
            if name == access_rule.get('name'):
                rule_data = access_rule
                break
        if rule_data is None:
            Exception('Unsable to find requested access rule.')
        return rule_data
    
    def get_url_categories(self):
        path = '/object/urlcategories'
        self.log.debug('Requesting url categories from FDM.')
        resp = self.request(path, headers=self.auth_headers)
        self.log.debug(f'Retrieved url categories from FDM.')
        return resp.get('items')
    
    def put_access_rule(self, access_rule):
        parent_id = self.policy_id
        obj_id = access_rule.get('id')
        path = f'/policy/accesspolicies/{parent_id}/accessrules/{obj_id}'
        self.log.debug('Updating url categories to FDM.')
        resp = self.request(path, method='put', body=access_rule)
        self.log.debug('Updating url categories to FDM was successful.')
        return resp
    
    def deploy(self, timeout=180, wait=10):
        path = '/operational/deploy'
        self.log.debug('Deploying the FDM configuration.')
        resp = self.request(path, method='post')
        if not resp.get('state') == 'QUEUED':
            raise Exception('Deployment to FDM has failed.')
        deploy_id = resp.get('id')
        while timeout > 0:
            sleep(wait)
            timeout -= wait
            self.log.debug('Checking status on deployment.')
            deploy_status = self.get_deploy_by_id(deploy_id)
            state = deploy_status.get('state')
            if state == 'DEPLOYED':
                self.log.debug('Deploy to FDM was successful.')
                break
            elif state == 'DEPLOY_FAILED' or state == 'DEPLOY_TIMEOUT':
                self.log.debug('Deploy to FDM failed.')
                break
        return resp

    def get_deploy_by_id(self, id):
        path = f'/operational/deploy/{id}'
        return self.request(path, headers=self.auth_headers)
