from src.base.B24 import B24
from src.base.pSQLmodels import ArticleModel
from src.base.mongodb import FileModel
from src.model.File import File

import json
import datetime

from fastapi import APIRouter, Body

article_router = APIRouter(prefix="/article", tags=["Статьи"])

def make_date_valid(date):
    if date is not None:
        try:
            return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        except:
            return datetime.datetime.strptime(date, '%d.%m.%Y')
    else:
        return None



class Article:
    def __init__(self, id=0, section_id=0):
        self.id = id
        self.section_id = section_id

    def find(self, inf_id, art_id, property):
        return B24().find(inf_id, art_id, property)

    def get_inf(self):
        return B24().getInfoBlock(self.section_id)

    def make_valid_article(self, data):
        '''
        ! Добавить статью и стандартизировать данные
        '''

        self.id = int(data['ID'])

        if "PREVIEW_TEXT" in data:
            preview = data['PREVIEW_TEXT']
            #data.pop('PREVIEW_TEXT')
        elif "PROPERTY_1009" in data:
            preview = list(data['PROPERTY_1009'].values())[0]
            #data.pop('PROPERTY_1009')
        elif "PROPERTY_341" in data:
            preview = list(data['PROPERTY_341'].values())[0]
            #data.pop('PROPERTY_341')
        elif "PROPERTY_290" in data:
            preview = list(data['PROPERTY_290'].values())[0]
            #data.pop('PROPERTY_290')
        else:
            preview = None



        content_type = None
        if "CONTENT_TEXT" in data:
            content = data['CONTENT_TEXT']
            #data.pop('CONTENT_TEXT')
        elif "TEXT" in data:
            content = data['TEXT']
            #data.pop('TEXT')
        elif "DETAIL_TEXT" in data:
            content = data['DETAIL_TEXT']
            #data.pop('DETAIL_TEXT')
        else:
            keys = ["PROPERTY_1239", "PROPERTY_457", "PROPERTY_477", "PROPERTY_340", "PROPERTY_291"]
            content = None
            for key in keys:
                if key in data:
                    if "TEXT" in data[key]:
                        content = list(data[key]["TEXT"].values())[0]
                        if "TYPE" in data[key]:
                            content_type = list(data[key]["TYPE"].values())[0]

                    elif "TEXT" in list(data[key].values())[0]:
                        content = list(data[key].values())[0]["TEXT"]
                        if "TYPE" in list(data[key].values())[0]:
                            content_type = list(data[key].values())[0]["TYPE"]



        if "ACTIVE_FROM" in data:
            date_publiction = data['ACTIVE_FROM']
            if data["ACTIVE_FROM"] == None:
                data["active"] = False
            #data.pop('ACTIVE_FROM')
        else:
            date_publiction = None

        if "DATE_CREATE" in data:
            date_creation = data['DATE_CREATE']
            #data.pop('DATE_CREATE')
        elif "PROPERTY_665" in data:
            date_creation = list(data['PROPERTY_665'].values())[0]
        elif "PROPERTY_666" in data:
            date_creation = list(data['PROPERTY_666'].values())[0]
        else:
            date_creation = None

        # записываем файлы в БД
        self.search_files(data["IBLOCK_ID"], self.id, data)
        # article_data["indirect_data"]["files"]

        # определяем превью

        #тут, по необходимости, можно форматировать data (заменить числовой ключ на значение или что-то вроде того)

        indirect_data = json.dumps(data)

        article_data = {
            "id" : self.id,
            "section_id" : self.section_id,
            "name" : data['NAME'],
            "preview_text" : preview,
            "content_text" : content,
            "date_publiction" : make_date_valid(date_publiction),
            "date_creation" : make_date_valid(date_creation),
            "indirect_data" : indirect_data
        }

        if "active" in data:
            article_data['active'] = data['active']

        if content_type is not None:
            article_data['content_type'] = content_type

        return article_data

    def search_files(self, inf_id, art_id, data):
        files_propertys = [
            "PREVIEW_PICTURE",
            "DETAIL_PICTURE",
            "PROPERTY_372",
            "PROPERTY_373",
            "PROPERTY_337",
            "PROPERTY_338",
            "PROPERTY_342",
            "PROPERTY_343",
            "PROPERTY_1023",
            "PROPERTY_1020",
            "PROPERTY_476",
            "PROPERTY_670",
            "PROPERTY_669",
            "PROPERTY_463",
            "PROPERTY_498",
            "PROPERTY_289",
            "PROPERTY_399",
            "PROPERTY_400",
            "PROPERTY_407",
            "PROPERTY_409"
        ]

        # находим файлы статьи
        files = []
        # preview_image_url = ""
        for file_property in files_propertys:
            
            if file_property in data:
                try:
                    # выцепить id файла
                    # "PREVIEW_PICTURE" не обрабатывается, тип - строка
                    # "DETAIL_PICTURE" тоже не обработается если строка
                    if type(data[file_property]) == type(dict()):
                        for file_id in data[file_property].values():
                            if type(file_id) == type(str()):
                                files.append(file_id)
                            elif type(file_id) == type(list()):
                                for f_id in file_id:
                                    files.append(f_id)
                    elif type(data[file_property]) == type(list()):
                        for dct in data[file_property]:
                            for file_id in dct.values():
                                if type(file_id) == type(str()):
                                    files.append(file_id)
                                elif type(file_id) == type(list()):
                                    for f_id in file_id:
                                        files.append(f_id)
                    else:
                        print("Некорректные данные в поле ", file_property)
                        
                except:
                    pass
                    # print("Ошибка обработки в инфоблоке", sec_inf[i], "в поле", file_propertyin)

        if files == []:
            return []
        else:
            files_data = []
            files_to_add = File().need_update_file(art_id, files)
            if files_to_add != []:
                
                for f_id in files:
                    try:
                        file_data = File(id=f_id).upload_inf_art(inf_id, art_id)
                        print(f'{f_id}файл добавлен в монго', art_id, inf_id)
                        files_data.append(file_data)
                    except:
                        pass
            else:
                print(f'добавлять/обновалять не нужно {art_id} - статья, {inf_id} - инфоблок')

                return files_data


    def add(self, article_data):
        return ArticleModel().add_article(self.make_valid_article(article_data))



    def uplod(self):
        '''
        ! Не повредить имеющиеся записи и структуру
        ! Выгрузка файлов из инфоблоков
        '''

        '''
        ! Сопоставить section_id из Интранета и IBLOCK_ID из B24
        '''

        '''однозначно'''
        sec_inf = {
            13 : "149", # Наши люди
            16 : "122", # Видеоитервью
            32 : "132", # Новости организационного развития
            53 : "62", # Афиша
            54 : "55", # Предложения партнеров
            55 : "56" # Благотворительные проекты
        }


        #проходимся по инфоблокам
        for i in sec_inf:

            # запрос в B24
            self.section_id = sec_inf[i]
            infs = self.get_inf()

            #инфоблок не пустой
            if infs != []:
                for inf in infs:
                    artDB = ArticleModel(id = inf["ID"], section_id = i)
                    self.section_id = i

                    if artDB.need_add():
                        print("Добавил стаью", inf["ID"])
                        self.add(inf)
                    elif artDB.update(self.make_valid_article(inf)):
                        #проверить апдейт файлов
                        pass



        '''с параметрами'''
        #один section_id - несколько IBLOCK_ID
        sec_inf = {
            15 : ["75", "77"], #Блоги
            18 : ["81", "82"], #Памятка
            41 : ["98", "78", "84"] #Гид по предприятиям
        }

        #Блоги
        #пройти по инфоблоку заголовков
        self.section_id = "75"
        sec_inf_title = self.get_inf()
        for title_inf in sec_inf_title:
            title_id = title_inf["ID"]
            title_data = title_inf

            # пройти по инфоблоку статей блогов
            self.section_id = "77"
            sec_inf_data = self.get_inf()
            for data_inf in sec_inf_data:
                data_title_id = list(data_inf["PROPERTY_1008"].values())[0]
                #если эта статья принадлежит иинфоблоку
                if data_title_id == title_id:
                    data = dict()

                    #добавить все данные заголовка
                    for key in title_data:
                        data[key] = title_data[key]
                    #добавить все данные статьи
                    for key in data_inf:
                        data[key] = data_inf[key]

                    data["ID"] = data_inf["ID"]
                    data["section_id"] = 15 #Блоги
                    self.section_id = 15
                    data["TITLE"] = title_inf["NAME"]

                    #загрузить данные в таблицу
                    artDB = ArticleModel(id=data["ID"], section_id=self.section_id)
                    if artDB.need_add():
                        self.add(data)
                    elif artDB.update(self.make_valid_article(data)):
                        pass

        #Памятка
        # пройти по инфоблоку заголовков
        self.section_id = "82"
        sec_inf_title = self.get_inf()
        for title_inf in sec_inf_title:
            title_id = title_inf["ID"]
            title_data = title_inf

            # пройти по инфоблоку статей блогов
            self.section_id = "81"
            sec_inf_data = self.get_inf()
            for data_inf in sec_inf_data:
                if "PROPERTY_480" in data_inf:
                    data_title_id = list(data_inf["PROPERTY_480"].values())[0]
                else:
                    print("##################", data_inf["ID"])

                # если эта статья принадлежит инфоблоку
                if data_title_id == title_id:
                    data = dict()

                    # добавить все данные заголовка
                    for key in title_data:
                        data[key] = title_data[key]
                    # добавить все данные статьи
                    for key in data_inf:
                        data[key] = data_inf[key]

                    data["ID"] = data_inf["ID"]
                    data["section_id"] = 18  # Памятка
                    self.section_id = 18
                    data["TITLE"] = title_inf["NAME"]

                    # загрузить данные в таблицу
                    artDB = ArticleModel(id=data["ID"], section_id=self.section_id)
                    if artDB.need_add():
                        self.add(data)
                    elif artDB.update(self.make_valid_article(data)):
                        pass

        #Гид по предприятиям
        # пройти по инфоблоку заголовков
        self.section_id = "78"
        sec_inf_title = self.get_inf()
        for title_inf in sec_inf_title:
            title_id = title_inf["ID"]
            title_data = title_inf

            # пройти по инфоблоку статей блогов
            self.section_id = "98"
            sec_inf_data = self.get_inf()
            for data_inf in sec_inf_data:
                #if "PROPERTY_671" in data_inf:
                data_title_id = list(data_inf["PROPERTY_671"].values())[0]
                # если эта статья принадлежит иинфоблоку

                if data_title_id == title_id:
                    data = dict()

                    # добавить все данные заголовка
                    for key in title_data:
                        data[key] = title_data[key]
                    # добавить все данные статьи
                    for key in data_inf:
                        data[key] = data_inf[key]

                    data["ID"] = data_inf["ID"]
                    data["section_id"] = 41 # Гид по предприятиям
                    self.section_id = 41
                    data["TITLE"] = title_inf["NAME"]

                    # загрузить данные в таблицу
                    artDB = ArticleModel(id=data["ID"], section_id=self.section_id)
                    if artDB.need_add():
                        self.add(data)
                    elif artDB.update(self.make_valid_article(data)):
                        pass



        #несколько section_id - один IBLOCK_ID
        sec_inf = {
            31 : "50", #Актуальные новости
            51 : "50"  #Корпоративные события
        }

        # пройти по инфоблоку
        self.section_id = "50"
        art_inf = self.get_inf()
        for art in art_inf:
            art_id = art["ID"]
            if "PROPERTY_1066" in art:
                pre_section_id = list(art["PROPERTY_1066"].values())[0]

                if pre_section_id == "661":
                    if "PROPERTY_5044" in art and list(art["PROPERTY_5044"].values())[0] == "1":
                        art["section_id"] = 33  # Видеорепортажи
                        self.section_id = 33
                    else:
                        art["section_id"] = 31 # Актуальные новости
                        self.section_id = 31
                elif pre_section_id == "663":
                    art["section_id"] = 51  # Корпоративные события
                    self.section_id = 51

                artDB = ArticleModel(id=art["ID"], section_id=self.section_id)
                if artDB.need_add():
                    self.add(art)
                elif artDB.update(self.make_valid_article(art)):
                    pass
            else:
                # че делать с уже не актуальными новостями?
                
                self.section_id = 6
                artDB = ArticleModel(id=art["ID"], section_id=self.section_id)
                if artDB.need_add():
                    self.add(art)
                    print("Статья", art["NAME"], art["ID"], "уже не актуальна")
                elif artDB.update(self.make_valid_article(art)):
                    
                    # сюда надо что-то дописать
                    pass
                
                



        #несколько section_id - несколько IBLOCK_ID
        sec_inf = {
            42 : ["68", "69"], #Официальные события
            52 : ["68", "69"]  #Корпоративная жизнь в фото
        }

        # Фотогалерея
        self.section_id = "68"
        art_inf = self.get_inf()
        for art in art_inf:
            art_id = art["ID"]

            if "PROPERTY_403" in art:
                pre_section_id = list(art["PROPERTY_403"].values())[0]

                if pre_section_id == "322":
                    art["section_id"] = 42 # Официальные события
                    self.section_id = 42
                elif pre_section_id == "323":
                    art["section_id"] = 52  # Корпоративная жизнь в фото
                    self.section_id = 42

                artDB = ArticleModel(id=art["ID"], section_id=self.section_id)
                if artDB.need_add():
                    self.add(art)
                elif artDB.update(self.make_valid_article(art)):
                    pass

            else:
                self.section_id = 6
                artDB = ArticleModel(id=art["ID"], section_id=self.section_id)
                if artDB.need_add():
                    self.add(art)
                    # че делапть с уже не актуальными новостями?
                    print("Запись в фотогалерею", art["NAME"], art["ID"], "уже не актуальна")
                elif artDB.update(self.make_valid_article(art)):
                    pass


        # Видеогалерея
        self.section_id = "69"
        art_inf = self.get_inf()
        for art in art_inf:
            art_id = art["ID"]

            if "PROPERTY_405" in art:
                pre_section_id = list(art["PROPERTY_405"].values())[0]

                if pre_section_id == "327":
                    art["section_id"] = 42 # Официальные события
                    self.section_id = 42
                elif pre_section_id == "328":
                    art["section_id"] = 52  # Корпоративная жизнь в фото
                    self.section_id = 52

                artDB = ArticleModel(id=art["ID"], section_id=self.section_id)
                if artDB.need_add():
                    self.add(art)
                elif artDB.update(self.make_valid_article(art)):
                    pass

            else:
                # че делать с уже не актуальными новостями?
                self.section_id = 6
                artDB = ArticleModel(id=art["ID"], section_id=self.section_id)
                if artDB.need_add():
                    art["active"] = False
                    self.add(art)
                    print("Запись в фотогалерею", art["NAME"], art["ID"], "уже не актуальна")
                elif artDB.update(self.make_valid_article(art)):
                    pass



        '''самобытные блоки'''
        # полная статика
            # 11 Наша компания -> Наша компания
            # 12 История компании -> История компании
            # 110 Техника безопасности -> Техника безопасности
            # 33 Корпоративная газета ЭМК -> газеты
            # 41 Гид по предприятиям -> 3D тур

        #переделки
            # 17 Учебный центр
            # 19 Дни рождения
            # 21 Подбор оборудования
            # 22 Поздравительная открытка
            # 23 ChatGPT
            # 24 Разрешительная документация и сертиффикаты
            # 25 Референсы и опыт поставок
            # Новые сотрудники
            # Личный кабинет
            # Есть Идея

        #новые разделы
            # конфигуратор НПО Регулятор
            # DeepSeek
            # VCard
            # система личной эффективности
            # магазин мерча
            # QR-код на САЗ
            # Юбилей САЗ

        return {"status" : True}



    def search_by_id(self):
        return ArticleModel(id = self.id).find_by_id()

    def search_by_section_id(self):
        return ArticleModel(section_id = self.section_id).find_by_section_id()


#Получить данные инфоблока из Б24
@article_router.get("/infoblock/{ID}")
def test(ID):
    return Article(section_id=ID).get_inf()

#загрузить статьи из иноблоков Битрикса
@article_router.put("")
def upload_articles():
    return Article().uplod()

#найти статью по id
@article_router.get("/find_by_ID/{ID}")
def get_article(ID):
    return Article(id = ID).search_by_id()

#найти статьи раздела
@article_router.get("/find_by/{section_id}")
def get_articles(section_id):
    return Article(section_id = section_id).search_by_section_id()

#найти статьи раздела
@article_router.post("/search")
def search_articles(data = Body()):
    pass
