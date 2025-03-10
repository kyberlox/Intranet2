#from src.pSQLmodels import User as UserSQL
#from src.pSQLmodels import update_table_structure

import requests
import json

class User:
    def __init__(self, uuid=""):
        self.uuid = uuid
        #self.UserSQL = UserSQL()

    def get(self, method="user.get", params={}):
        req = f"https://portal.emk.ru/rest/2158/qunp7dwdrwwhsh1w/{method}"
        if params != {}:
            req += "?"
            for parem_key in params.keys():
                req += f"&{parem_key}={params[parem_key]}"
        response = requests.get(req)
        return response.json()

    def get_all(self, method, params={}):
        response = self.get(method)
        current = 50
        result = response["result"]
        keys = []
        while current < int(response["total"]):
            params["start"] = current
            response = self.get(method, params)
            curr_result = response["result"]
            for curr_keys in curr_result:
                for k in curr_keys:
                    if k not in keys:
                        keys.append(k)
                        #print(k)
            result = result + curr_result
            current += 50

        return [keys, result]

    def fetch_users_data(self):
        #отправить ключи на 
        return self.get_all("user.get")
