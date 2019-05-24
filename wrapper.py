import requests

class BaseApi(object):
    def __init__(self, BASE_URL):
        self.BASE_URL = BASE_URL

    def list(self, resource):
        pass

    def get(self, resource, id):
        pass

    def post(self, resource, **kwargs):
        pass
