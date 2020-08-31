

class ServerProfile(object):
    def __init__(self, rest_client):
        self.rest_client = rest_client
        self.path = '/api/v1/server/Profiles'

    def get(self):
        return self.rest_client.get(self.path)

    def get_byid(self, id):
        return self.rest_client.get(self.path+f'/{id}')
