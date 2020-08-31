import os


class Singleton(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it
    def init(self, *args, **kwds):
        pass

class Config(Singleton):
    def __init__(self):
        self.base_url = "https://intersight.com"
        self.api_key_id = os.environ.get('INTERSIGHT_KEY_ID')
        self.secret_key_file = os.environ.get('INTERSIGHT_SECRET_KEY_FILE')
