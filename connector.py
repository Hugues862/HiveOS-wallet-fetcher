from requests import request, exceptions
from time import sleep

class Hive(object):

    def __init__(self, token):
        self.token = token

    def api_query(self, method, command, payload=None, params=None):

        if payload is None:
            payload = {}
        if params is None:
            params = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }

        while True:
            try:
                s = request(method, 'https://api2.hiveos.farm/api/v2' + command, data=payload, params=params,
                            headers=headers, timeout=10)
            except exceptions.ConnectionError:
                print('Oops.')
                sleep(15)
                continue
            except exceptions.Timeout:
                print('Oops.')
                sleep(15)
                continue
            except exceptions.TooManyRedirects:
                print('Oops.')
                sleep(1800)
                continue
            else:
                api = s.json()
                break

        return api

    def get_farms(self):
        return self.api_query('GET', '/farms')

    def get_workers(self, farm_id):
        return self.api_query('GET', '/farms/'+farm_id+'/workers')

    def get_wallets(self, farm_id):
        return self.api_query('GET', '/farms/'+farm_id+'/wallets')
        
    def edit_farm(self, farm_id, params):
        return self.api_query('PATCH', '/farms/' + farm_id, params)
