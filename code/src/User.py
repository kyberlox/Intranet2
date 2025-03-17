from src.pSQLmodels import UserModel
from src.B24 import B24

import requests
import json



class User:
    def __init__(self, uuid=""):
        self.uuid = uuid
        #self.UserSQL = UserSQL()



    '''
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

        return (keys, result)
    '''



    def fetch_users_data(self):
        b24 = B24()
        data = b24.getUsers()
        UserSQL = UserModel()

        #отправить записи
        for usr_data in data:
            if usr_data['ID'] == '2375':
                UserSQL.upsert_user(usr_data)

        return {"status" : True}

    def search_by_id(self, id):
        return UserModel(id).find_by_id(id)


    '''
    def variant_users(self, key):
        return B24().variant_key_user(key)
    '''

    '''
    def get_dep_usrs(self):
        b24 = B24()
        users_data = b24.getUsers()
        dep_data = sorted(b24.getDeps(), key=lambda d: int(d['ID']))

        result = [["ID", "Название подраздедения", "ФИО руководителя", "ФИО сотрудника"]]
        for dep in dep_data:
            dep_ID = int(dep['ID'])
            if 'UF_HEAD' in dep and dep['UF_HEAD'] != '0':
                for usr in users_data:
                    if usr['ID'] == dep['UF_HEAD'] and ('LAST_NAME' in usr and 'NAME' in usr and 'SECOND_NAME' in usr):
                        dep_head = f"{usr['LAST_NAME']} {usr['NAME']} {usr['SECOND_NAME']}"
                        print(dep_ID, dep_head)

            for usr in users_data:
                if usr["ACTIVE"] and dep_ID in usr['UF_DEPARTMENT'] and ('LAST_NAME' in usr and 'NAME' in usr and 'SECOND_NAME' in usr):

                    result.append([dep_ID, dep['NAME'], dep_head, f"{usr['LAST_NAME']} {usr['NAME']} {usr['SECOND_NAME']}"])

        return result
    '''

    def get_dep_usrs(self):
        b24 = B24()
        users_data = sorted(b24.getUsers(), key=lambda d: int(d['ID']))
        #dep_data = b24.getDeps()
        result = [["id", "ФИО", "Должность", "Подразделение (по иерархии)"]]
        for usr in users_data:
            if usr["ACTIVE"] and ('WORK_POSITION' in usr and usr['WORK_POSITION'] != "") and ('UF_USR_1705744824758' in usr and usr['UF_USR_1705744824758'] != [] and usr['UF_USR_1705744824758'] != False) and ('LAST_NAME' in usr and 'NAME' in usr and 'SECOND_NAME' in usr):
                line = [usr['ID'], f"{usr['LAST_NAME']} {usr['NAME']} {usr['SECOND_NAME']}", usr['WORK_POSITION']]
                for dep in usr['UF_USR_1705744824758']:
                    line.append(dep)

                result.append(line)
        return result









