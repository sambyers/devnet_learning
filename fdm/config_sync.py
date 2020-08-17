import argparse
import logging
from fdm import FDMClient
import yaml
import json
import urllib3


urllib3.disable_warnings()

class ConfigSync():
    def __init__(self, configfile=None, log=None):
        super().__init__()
        self.configfile = configfile
        self.log = log
        self.configdict = self.load_config()
        self.fdmclient = self.init_fdm_client()
        self.access_rule_config = None

    def load_config(self):
        with open(self.configfile) as f:
            configdict = yaml.full_load(f.read())
        return configdict
    
    def init_fdm_client(self):
        fdm = FDMClient(**self.configdict.get('host'), log=self.log)
        fdm.login()
        return fdm
    
    def get_config(self):
        rule_name = self.configdict['config']['url_filtering']['rule_name']
        self.log.debug(f'Requesting access rule {rule_name}.')
        config = self.fdmclient.get_access_rule_by_name(rule_name)
        return config

    def get_url_category(self, name):
        url_category = None
        for category in self.url_categories:
            if category.get('name') == name:
                url_category = {
                    'urlCategory': {
                        'id': category.get('id'),
                        'type': category.get('type'),
                        'name': category.get('name')
                    },
                    'type': 'urlcategorymatcher'
                }
                break
        return url_category
    
    def sync(self):
        self.log.info('Starting the configuration synchronization.')
        self.log.info('Requesting URL categories from FDM.')
        self.url_categories = self.fdmclient.get_url_categories()
        self.access_rule_config = self.get_config()
        self.access_rule_config['urlFilter']['urlCategories'] = []
        for url_category in self.configdict['config']['url_filtering']['url_categories']:
            cat = self.get_url_category(url_category)
            self.access_rule_config['urlFilter']['urlCategories'].append(cat)
        self.log.info('Synchronizing URL categories to FDM.')
        self.fdmclient.put_access_rule(self.access_rule_config)
    
    def deploy(self):
        self.log.info('Deploying configuration to FDM.')
        self.fdmclient.deploy()
        self.log.info('Deploy complete. Logging out.')
        self.fdmclient.logout()


def parse_args():
    a = argparse.ArgumentParser()
    a.add_argument('--config', default='fdm.cfg')
    a.add_argument('--debug', action='store_true')
    return a.parse_args()

def init_logger(log_level=logging.INFO):
    log = logging.getLogger(__file__)
    log.setLevel(log_level)
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    log.addHandler(console)
    return log

if __name__ == '__main__':
    args = parse_args()
    if args.debug:
        log = init_logger(logging.DEBUG)
    else:
        log = init_logger()
    cs = ConfigSync(configfile='fdm.cfg', log=log)
    cs.sync()
    cs.deploy()
