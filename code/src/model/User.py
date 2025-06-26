from src.base.pSQLmodels import UserModel
from src.base.SearchModel import UserSearchModel
from src.model.File import File
from src.base.B24 import B24
from src.services.LogsMaker import LogsMaker

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
        # кастомный прогрессбар
        logg = LogsMaker()

        #отправить записи
        for usr_data in logg.progress(data, "Обработка информации о пользователях "):
            #!!!!!!!!!!!!!!!!!!!!!!убрать по окончанию тестового периода!!!!!!!!!!!!!
            cool_users = ['2366', '2375', '4133', '157', '174', '1375', '4370', '4375', '4367', '575', '4320', '2515', '682', '806', '376', '911', '552', '796', '367', '659', '579', '828', '4399', '4393', '4411', '292', '3218', '2081']
            pochet = ['421', '682', '806', '376', '911', '552', '796', '810', '603', '148', '161', '832', '692', '590', '67', '533', '610', '345', '745', '372', 
            '591', '712', '72', '1399', '684', '1801', '1176', '556', '609', '580', '798', '812', '680', '930', '598', '318', '343', '82', '1566', '1141', '2111', 
            '1566', '120', '1442', '58', '85', '86', '2366', '2375', '1712', '704', '707', '1440', '1023', '604', '610', '355', '363', '361', '347', '1413', '743', 
            '805', '1430', '1062', '1541', '2540', '1282', '589', '593', '534', '2547', '1384', '1087', '1323', '63', '1660', '975', '96', '2452', '2713', '2707', 
            '1560', '681', '711', '340', '702', '612', '353', '605', '2484', '2497', '2857', '810', '794', '261', '552', '1568', '2521', '2508', '2527', '2536', 
            '1567', '2510', '2545', '1080', '627', '1131', '592', '809', '570', '724', '514', '757', '153', '376', '2112', '1037', '1705']
            cool_users += pochet
            if usr_data['ID'] in cool_users:
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                UserSQL.upsert_user(usr_data)
        
        status = self.set_users_photo()

        return {"status" : status}

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

    def user_inf_by_uuid(self):
        return UserModel(self.uuid).find_by_uuid()


    def set_users_photo(self):
        b24 = B24()
        data = b24.getUsers()
        # кастомный прогрессбар
        logg = LogsMaker()

        for usr_data in logg.progress(data, "Загрузка фотографий пользователей "):
            #найдем фото пользователя, если у пользователя есть аватарка
            # print()
            cool_users = ['2366', '2375', '4133', '157', '174', '1375', '4370', '4375', '4367', '575', '4320', '2515', '682', '806', '911', '796', '367', '659', '579', '828', '4399', '4393', '4411', '292', '3218', '2081']
            pochet = ['421', '682', '806', '376', '911', '552', '796', '810', '603', '148', '161', '832', '692', '590', '67', '533', '610', '345', '745', '372', 
            '591', '712', '72', '1399', '684', '1801', '1176', '556', '609', '580', '798', '812', '680', '930', '598', '318', '343', '82', '1566', '1141', '2111', 
            '1566', '120', '1442', '58', '85', '86', '2366', '2375', '1712', '704', '707', '1440', '1023', '604', '610', '355', '363', '361', '347', '1413', '743', 
            '805', '1430', '1062', '1541', '2540', '1282', '589', '593', '534', '2547', '1384', '1087', '1323', '63', '1660', '975', '96', '2452', '2713', '2707', 
            '1560', '681', '711', '340', '702', '612', '353', '605', '2484', '2497', '2857', '810', '794', '261', '552', '1568', '2521', '2508', '2527', '2536', 
            '1567', '2510', '2545', '1080', '627', '1131', '592', '809', '570', '724', '514', '757', '153', '376', '2112', '1037', '1705']
            cool_users += pochet
            if "ID" in usr_data:
                if usr_data['ID'] in cool_users:
                    uuid = usr_data['ID']
                    #есть ли у пользователя есть фото в битре? есть ли пользователь в БД? 
                    if 'PERSONAL_PHOTO' in usr_data and 'id' in UserModel(uuid).find_by_id().keys():

                        b24_url = usr_data['PERSONAL_PHOTO']
                        #print(b24_url)
                        #проверим url первоисточника текущей аватарки
                        psql_user = UserModel(uuid).find_by_id()
                        if psql_user['photo_file_id'] is None or psql_user['photo_file_b24_url'] != b24_url:

                            #cтарую фотку - в архив
                            if psql_user['photo_file_b24_url'] is not None and psql_user['photo_file_b24_url'] != b24_url:
                                old_file_id = psql_user['photo_file_id']
                                File(id = old_file_id).delete_user_img()
                            
                            #если есть несоответствие - скачать новую
                            file_data = File().add_user_img(b24_url, uuid)

                            #обновить данные в pSQL
                            UserModel(uuid).set_user_photo(file_data['id'])
                            
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
    
    # лайки
    def add_like(self, art_id):
        return LikesModel(user_id=self.id, art_id=art_id).add_like()

    def remove_like(self, art_id):
        return LikesModel(user_id=self.id, art_id=art_id).remove_like()

    def has_liked(self, art_id):
        return LikesModel(user_id=self.id, art_id=art_id).has_liked()

    def get_user_likes(self):
        return LikesModel(user_id=self.id).get_user_likes()
    
    # просмотры
    def add_view(self, art_id):
        return ViewsModel(user_id=self.id, art_id=art_id).add_view()

    def get_viewed_articles(self):
        return ViewsModel(user_id=self.id).get_viewed_articles()
    
    # день рождения
    def get_birthday_celebrants(self, date):
        return UserModel().find_all_celebrants(date)
    
    # новые сотрудники
    def get_new_workers(self):
        return UserModel().new_workers()

'''
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
'''



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
@users_router.post("/search/{username}")
def search_user(username: str): # jsn=Body()
    return UserSearchModel().search_by_name(username)

#загрузить дату в ES
@users_router.put("/elastic_data")
def upload_users_to_es():
    return UserSearchModel().dump()

@users_router.get("/test_update_photo")
def test_update_photo():
    return User().set_users_photo()



@users_router.post("/search")
def search_user(jsn=Body()):
    #будет работать через elasticsearch
    return UserSearchModel().search_model(jsn)

@users_router.get("/test_update_photo")
def test_update_photo():
    return User().set_users_photo()

# лайки и просмотры
@users_router.put("/add_like")
def add_like(user_id: int, art_id: int):
    return User(user_id=user_id).add_like(art_id)

@users_router.delete("/remove_like")
def remove_like(user_id: int, art_id: int):
    return User(user_id=user_id).remove_like(art_id)

@users_router.post("/has_liked")
def has_liked(user_id: int, art_id: int):
    return User(user_id=user_id).has_liked(art_id)

@users_router.get("/get_user_likes")
def get_user_likes(user_id: int):
    return User(user_id=user_id).get_user_likes()

@users_router.put("/add_view")
def add_view(user_id: int, art_id: int):
    return User(user_id=user_id).add_view(art_id)

@users_router.get("/get_viewed_articles")
def get_viewed_articles(user_id: int):
    return User(user_id=user_id).get_viewed_articles()

@users_router.post("/search_indirect")
def search_indirect(key_word):
    #будет работать через elasticsearch
    return UserSearchModel().search_indirect(key_word)

# запрос для получения списка пользователей у кого в эту дату ДР
@users_router.get("/get_birthday_celebrants/{day_month}")
def birthday_celebrants(day_month: str):
    return User().get_birthday_celebrants(day_month)