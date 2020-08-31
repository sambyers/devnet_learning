from config import Config
from rest import RestClient
from resources import ServerProfile
from resources import NtpPolicy


class Intersight():
    def __init__(self):
        self.config = Config()
        self.rest_client = RestClient(
            self.config.base_url,
            self.config.api_key_id,
            self.config.secret_key_file
            )
        self.serverprofile = ServerProfile(self.rest_client)
        self.ntppolicy = NtpPolicy(self.rest_client)