from src.base.pSQLmodels import UserModel
from src.model.File import File
from src.base.B24 import B24

import requests
import json

from fastapi import APIRouter, Body, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="./front_jinja")

users_router = APIRouter(prefix="/users", tags=["Пользователь"])


class User:
    def __init__(self, id=0, uuid=""):
        self.id = id
        self.uuid = uuid
        #self.UserSQL = UserSQL()

    def fetch_users_data(self):
        b24 = B24()
        data = b24.getUsers()
        UserSQL = UserModel()

        #отправить записи
        for usr_data in data:
            #if usr_data['ID'] == '2375':
            UserSQL.upsert_user(usr_data)
        
        self.set_users_photo()

        return {"status" : True}

    def search_by_id(self):
        return UserModel(self.id).find_by_id()

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

    def get_uf_depart(self):
        return UserModel().find_uf_depart()

    

    def set_users_photo(self):
        b24 = B24()
        data = b24.getUsers()

        for usr_data in data:
            #найдем фото пользователя, если у пользователя есть аватарка
            if "ID" in data:
                uuid = data['ID']
                if 'PERSONAL_PHOTO' in usr_data:
                    b24_ulr = data['PERSONAL_PHOTO']
                    #проверим url первоисточника текущей аватарки
                    
                    psql_user = UserModel(self.id).find_by_id()
                    if psql_user['photo_file_b24_url'] is None or psql_user['photo_file_b24_url'] != b24_ulr:
                        #cтарую фотку - в архив
                        if psql_user['photo_file_b24_url'] is not None and psql_user['photo_file_b24_url'] != b24_ulr:
                            old_file_id = psql_user['photo_file_id']
                            File(id = ObjectId(old_file_id)).delete_user_img()
                        
                        #если есть несоответствие - скачать новую
                        file_data = File().add_user_img(b24_url, uuid)

                        #обновить данные в pSQL
                        UserModel(self.id).set_user_photo(file_data['id'], file_data['URL'])
                        
            #вывести отчет по изменениях
            return True



   
    def variant_users(self, key):
        return B24().variant_key_user(key)

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
    

    # def get(self, method="user.get", params={}):
    #     req = f"https://portal.emk.ru/rest/2158/qunp7dwdrwwhsh1w/{method}"
    #     if params != {}:
    #         req += "?"
    #         for parem_key in params.keys():
    #             req += f"&{parem_key}={params[parem_key]}"
    #     response = requests.get(req)
    #     return response.json()
    
    # def get_all(self, method, params={}):
    #     response = self.get(method)
    #     current = 50
    #     result = response["result"]
    #     keys = []
    #     while current < int(response["total"]):
    #         params["start"] = current
    #         response = self.get(method, params)
    #         curr_result = response["result"]
    #         for curr_keys in curr_result:
    #             for k in curr_keys:
    #                 if k not in keys:
    #                     keys.append(k)
    #                     #print(k)
    #         result = result + curr_result
    #         current += 50

    #     return (keys, result)




#Пользоваетелей можно обновить
@users_router.put("/update")
def update_user():
    usr = User()
    return usr.fetch_users_data()

# фронт
@users_router.get("/view")
def view_user(request: Request):
    return templates.TemplateResponse(name="user.html", context={"request": request})

#Пользователя можно выгрузить
@users_router.get("/find_by/{id}")
def find_by_user(id):
    return User(id).search_by_id()

#Пользователя можно найти
@users_router.post("/search")
def search_user(jsn=Body()):
    #будет работать через elasticsearch
    pass


