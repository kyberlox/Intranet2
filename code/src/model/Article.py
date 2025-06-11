from src.base.B24 import B24
from src.base.pSQLmodels import ArticleModel
from src.base.SearchModel import ArticleSearchModel
from src.base.mongodb import FileModel
from src.model.File import File
from src.model.User import User
from src.model.Section import Section
from src.services.LogsMaker import LogsMaker
from src.base.pSQLmodels import LikesModel
from src.base.pSQLmodels import ViewsModel

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
        
        #убрать ключи из PROPERTY:
        for key in data.keys():
            if key.startswith("PROPERTY_") and type(data[key]) == type(dict()):
                grya = []
                for key_key in data[key].keys():
                    if type(data[key][key_key]) == type(list()):
                        for scr_scr in data[key][key_key]:
                            grya.append(scr_scr)
                    else:
                        grya.append(data[key][key_key])
                data[key] = grya

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
            #"PROPERTY_376",

            "PROPERTY_337",
            "PROPERTY_338",

            "PROPERTY_342",
            "PROPERTY_343",

            "PROPERTY_1023",
            "PROPERTY_1020",

            "PROPERTY_476",

            "PROPERTY_670", #!!! сслыка на ютуб !!!
            "PROPERTY_669",

            "PROPERTY_463",

            "PROPERTY_498",

            "PROPERTY_289",
            # "PROPERTY_296",

            "PROPERTY_399",
            "PROPERTY_400",
            #"PROPERTY_402",

            "PROPERTY_407",
            "PROPERTY_409", #!!! сслыка на ютуб !!!

            #вложения
            "PROPERTY_478",
            "PROPERTY_491"

        ]

        preview_file = [
            "PREVIEW_PICTURE",
            "PROPERTY_372",
            "PROPERTY_337",
            "PROPERTY_342",
            "PROPERTY_1023"
        ]
        
        # находим файлы статьи
        files = []
        preview_images = []
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

                                    if file_property in preview_file:
                                        preview_images.append(f_id)
                    elif type(data[file_property]) == type(list()):
                        for dct in data[file_property]:
                            for file_id in dct.values():
                                if type(file_id) == type(str()):
                                    files.append(file_id)
                                elif type(file_id) == type(list()):
                                    for f_id in file_id:
                                        files.append(f_id)

                                        if file_property in preview_file:
                                            preview_images.append(f_id)

                    elif type(data[file_property]) == type(str()):
                        files.append( data[file_property] )

                        if file_property in preview_file:
                            preview_images.append(data[file_property])
                    else:
                        print("Некорректные данные в поле ", file_property, f"Данные: {type(data[file_property])}", f"Ищи в {inf_id}, {art_id}")
                        
                except:
                    pass
                    # print("Ошибка обработки в инфоблоке", sec_inf[i], "в поле", file_property)

        if files == []:
            return []
        else:
            files_data = []
            files_to_add = File().need_update_file(art_id, files)

            if files_to_add != []:
                for f_id in files:
                    is_preview = f_id in preview_images
                    file_data = File(b24_id=f_id).upload_inf_art(art_id, is_preview)
                    #sprint(f'{f_id} файл добавлен в монго', art_id, inf_id)
                    files_data.append(file_data)

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

        # создание индексов в Mongo
        FileModel().create_indexes()

        # кастомный прогрессбар
        logg = LogsMaker()

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
        for i in logg.progress(sec_inf, "Загрузка данных инфоблоков 149, 122, 132, 62, 55, 56 "):

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
        for title_inf in logg.progress(sec_inf_title, "Загрузка данных инфоблоков 75, 77 "):
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
        for title_inf in logg.progress(sec_inf_title, "Загрузка данных инфоблоков 82, 81 "):
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
        for title_inf in logg.progress(sec_inf_title, "Загрузка данных инфоблоков 78, 98 "):
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
        for art in logg.progress(art_inf, "Загрузка данных разделов \"Актуальные новости\", \"Корпоративные события\" и \"Видеорепортажи\" "):
            if art["ID"] == '13486':
                print(art, ' новость')
            else:
                pass
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
        for art in logg.progress(art_inf, "Загрузка данных разделов \"Официальные события\" и \"Корпоративная жизнь в фото\" "):
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
        
        # вакансии (приведи друга)
        self.section_id = "67"
        art_inf = self.get_inf()
        for art in art_inf:
            self.section_id = 5 # потом изменить
            artDB = ArticleModel(id=art["ID"], section_id=self.section_id)
            if artDB.need_add():
                self.add(art)
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
            # YandexGPT5 + Yandex ART
            # система личной эффективности
            # магазин мерча
            # QR-код на САЗ
            # Юбилей САЗ

        return {"status" : True}

    def search_by_id(self):
        return ArticleModel(id = self.id).find_by_id()

    def get_preview(self, id):
        res = FileModel(id).find_all_by_art_id()
        mongo_list = []
        preview_inf = []
        one_preview_inf = []
        for result in res:
            mongo_list.append(result)
        if len(mongo_list) > 1:

            for info in mongo_list:
                one_preview_inf.append(info['b24_id'])
                one_preview_inf.append(info['file_url'])
                preview_inf.append(one_preview_inf)

            # сортируем по b24_id если фоток много и берем с наименьшим b24_id
            sorted_list = sorted(preview_inf, key=lambda x: x[0], reverse=True)

            preview_inf = sorted_list[0][1]
            return preview_inf
        elif len(mongo_list) == 0:
            return None
        else:
            return mongo_list[0]['file_url']

    def search_by_section_id(self):
        if self.section_id == "0":
            main_page = [1, 19, 32, 4, 111, 31, 16, 33, 9, 10, 51] #section id
            page_view = []

            for page in main_page: # проходимся по каждой секции
                sec = self.main_page(page)
                page_view.append(sec) 
            page_view[-3]['content'] = [page_view[-2], page_view[-1]]
            del page_view[-2:]

            return page_view
        
        elif self.section_id == "19":
            users_bday_info = []
            date_bday = datetime.datetime.now().strftime("%d.%m")
            users = User().get_birthday_celebrants(date_bday)
            return users

        else:
            active_articles = []
            result = ArticleModel(section_id = self.section_id).find_by_section_id()
            for res in result:
                if self.section_id == "16" and ("PROPERTY_1025" not in res['indirect_data'] or res['indirect_data']['PROPERTY_1025'] is None):
                    continue
                elif res['active']:
                    active_articles.append(res)
                else:
                    pass
            if self.section_id == "111":
                sorted_active_aticles = sorted(active_articles, key=lambda x: x['name'], reverse=False)
            else:
                sorted_active_aticles = sorted(active_articles, key=lambda x: x['id'], reverse=True)
            return sorted_active_aticles
    
    def main_page(self, section_id):
        #Новые сотрудники
        if section_id == 1:       
            new_workers = {
                'id': 1,
                'type': 'singleBlock',
                'title': 'Новые сотрудники',
                'images': [{
                    "id": 1,
                    "image": None,
                    "href": "/"
                }],
                'href': 'newWorkers',
            } # словарь-заглушка для будущей секции "новые сотрудники"
            return new_workers

        #С днем рождения!
        elif section_id == 19:
            images_for_bday = []
            date_bday = datetime.datetime.now().strftime("%d.%m")
            users = User().get_birthday_celebrants(date_bday)
            for user in users:
                user.pop('position')
                user.pop('department')
                user.pop('user_fio')
                images_for_bday.append(user)

            birthday = {
                'id': section_id,
                'type': 'singleBlock',
                'title': 'С днем рождения!',
                'images': images_for_bday,
                'href': 'birthdays',
            } # словарь-заглушка для будущей секции "С днем рождения!"
            return birthday

        #
        elif section_id == 32:
            date_list = [] # список для сортировки по дате
            articles_in_section = ArticleModel(section_id=section_id).find_by_section_id()
            for values in articles_in_section:
                if values["active"] is False:
                        pass
                else:
                    date_value = [] # список для хранения необходимых данных
                    date_value.append(values["id"])
                    date_value.append(values["name"])
                    date_value.append(values["preview_text"])
                    date_value.append(values["date_creation"])
                    date_list.append(date_value) # получили список с необходимыми данными
            # сортируем по дате
            sorted_data = sorted(date_list, key=lambda x: x[0], reverse=True)
            news_id = sorted_data[0][0]
            print(news_id, 'article')
            image_URL = self.get_preview(news_id)
            second_page = {
                'id': section_id, 
                'type': 'singleBlock', 
                'title': 'Организационное развитие', 
                "href": "corpnews", 
                'images': [{'id': news_id, 'image': image_URL}]
                }
            return second_page
        
        #
        elif section_id == 4:
            idea_block = {
                'id': 4,
                'type': 'singleBlock',
                'title': 'Предложить идею',
                'images': [{
                    "id": 1,
                    "image": None,
                    "href": "/"
                }],
                'modifiers': ['outline'],
                'href': 'ideasPage'
            }# словарь-заглушка для будущей секции "Предложить идею"
            return idea_block

        #
        elif section_id == 111:
            emk_competition = {
                'id': section_id,
                'type': 'singleBlock',
                'title': 'Конкурсы ЭМК',
                'images': [{
                    "id": 1,
                    "image": None,
                    "href": "vacancies"
                }],
                '// href': '/'
            } # словарь-заглушка для будущей секции "Конкурсы ЭМК"
            return emk_competition

        elif section_id == 31:
            date_list = [] # список для сортировки по дате
            articles_in_section = ArticleModel(section_id=section_id).find_by_section_id()
            for values in articles_in_section:
                if values["active"] is False:
                        pass
                else:
                    date_value = [] # список для хранения необходимых данных
                    date_value.append(values["id"])
                    date_value.append(values["name"])
                    date_value.append(values["preview_text"])
                    date_value.append(values["date_creation"])
                    date_list.append(date_value) # получили список с необходимыми данными
            # сортируем по дате
            sorted_data = sorted(date_list, key=lambda x: x[0], reverse=True)

            second_page = {
                'id': section_id,
                'type': 'fullRowBlock',
                'title': 'Бизнес-новости',
                'href': 'actualnews',
                'images': []
            }

            business_news = []
            
            image_url = ''
            for i, row in enumerate(sorted_data):
                if i < 5:
                    news = {}
                    preview_pict = Article().get_preview(row[0])

                    if preview_pict is None:
                        image_url = None
                    else:
                        image_url = preview_pict
                    
                    news['id'] = row[0]
                    news['title'] = row[1]
                    # news['description'] = row[2]
                    news['image'] = image_url
                    # сюда реакции
                    news['reactions'] = {
                        'views': 12,
                        'likes': { 'count': 13, 'likedByMe': 1 },
                    }
                    business_news.append(news)
            second_page['images'] = business_news
            return second_page

        elif section_id == 16:
            date_list = [] # список для сортировки по дате
            articles_in_section = ArticleModel(section_id=section_id).find_by_section_id()
            for values in articles_in_section:
                if values["active"] is False:
                        pass
                else:
                    if "PROPERTY_1025" not in values['indirect_data'] or values['indirect_data']['PROPERTY_1025'] is None:
                        pass
                    else:
                        date_value = [] # список для хранения необходимых данных
                        date_value.append(values["id"])
                        date_value.append(values["name"])
                        date_value.append(values["preview_text"])
                        date_value.append(values["date_creation"])
                        date_list.append(date_value) # получили список с необходимыми данными
            # сортируем по дате
            sorted_data = sorted(date_list, key=lambda x: x[0], reverse=True)

            second_page = {
                'id': section_id,
                'type': 'fullRowBlock',
                'title': 'Интервью',
                'href': 'interview',
                'images': []
            }

            interview_news = []
            
            image_url = ''
            for i, row in enumerate(sorted_data):
                if i < 5:
                    news = {}
                    preview_pict = Article().get_preview(row[0])

                    if preview_pict is None:
                        image_url = None
                    else:
                        image_url = preview_pict
                    
                    news['id'] = row[0]
                    news['title'] = row[1]
                    news['description'] = row[2]
                    news['image'] = image_url
                    news['href'] = 'videoInterview'
                    # сюда реакции
                    news['reactions'] = {
                        'views': 12,
                        'likes': { 'count': 13, 'likedByMe': 1 },
                    }
                    interview_news.append(news)
            second_page['images'] = interview_news
            return second_page

        elif section_id == 33:
            date_list = [] # список для сортировки по дате
            articles_in_section = ArticleModel(section_id=section_id).find_by_section_id()
            for values in articles_in_section:
                if values["active"] is False:
                        pass
                else:
                    date_value = [] # список для хранения необходимых данных
                    date_value.append(values["id"])
                    date_value.append(values["name"])
                    date_value.append(values["preview_text"])
                    date_value.append(values["date_creation"])
                    date_list.append(date_value) # получили список с необходимыми данными
            # сортируем по дате
            sorted_data = sorted(date_list, key=lambda x: x[0], reverse=True)

            second_page = {
                'id': section_id,
                'type': 'fullRowBlock',
                'title': 'Видеорепортажи',
                'href': 'videonews',
                'images': []
            }

            video_news = []
            
            image_url = ''
            for i, row in enumerate(sorted_data):
                if i < 5:
                    news = {}
                    preview_pict = Article().get_preview(row[0])

                    if preview_pict is None:
                        image_url = None
                    else:
                        image_url = preview_pict
                    
                    news['id'] = row[0]
                    news['title'] = row[1]
                    news['description'] = row[2]
                    news['image'] = image_url
                    # сюда реакции
                    news['reactions'] = {
                        'views': 12,
                        'likes': { 'count': 13, 'likedByMe': 1 },
                    }
                    video_news.append(news)
            second_page['images'] = video_news
            return second_page

        elif section_id == 9:
            second_page = {
                "id": 9,
                "type": "mixedRowBlock",
                "content": []
            }
            return second_page

        elif section_id == 10:
            afisha = {
                'type': "singleBlock",
                'title': "Афиша",
                'href': 'eventAnnounces',
                'images': [
                    {
                        'id': 1,
                        'image': None,
                        'href': "home"
                    },
                    {
                        'id': 2,
                        'image': None,
                        'href': "home"
                    }
                ]
            } # словарь-заглушка для будущей секции "Афиша"
            return afisha
        
        elif section_id == 51:
            date_list = [] # список для сортировки по дате
            articles_in_section = ArticleModel(section_id=section_id).find_by_section_id()
            for values in articles_in_section:
                if values["active"] is False:
                        pass
                else:
                    date_value = [] # список для хранения необходимых данных
                    date_value.append(values["id"])
                    date_value.append(values["name"])
                    date_value.append(values["preview_text"])
                    date_value.append(values["date_creation"])
                    date_list.append(date_value) # получили список с необходимыми данными
            # сортируем по дате
            sorted_data = sorted(date_list, key=lambda x: x[0], reverse=True)

            corpevents = {
                'id': section_id,
                'type': "fullRowBlock",
                'title': "Корпоративные события",
                'href': "corpevents",
                'images': []
            }
            image_url = ''
            corpevents_news = []
            for i, row in enumerate(sorted_data):
                if i < 5:
                    news = {}
                    preview_pict = Article().get_preview(row[0])

                    if preview_pict is None:
                        image_url = None
                    else:
                        image_url = preview_pict
                    
                    news['id'] = row[0]
                    news['title'] = row[1]
                    news['description'] = row[2]
                    news['image'] = image_url
                    # сюда реакции
                    news['reactions'] = {
                        'views': 12,
                        'likes': { 'count': 13, 'likedByMe': 1 },
                    }
                    corpevents_news.append(news)

            corpevents['images'] = corpevents_news
            return corpevents

    # лайки
    def get_all_likes(self):
        return LikesModel(art_id=self.id).get_likes_count()

    def get_article_likers(self):
        return LikesModel(art_id=self.id).get_article_likers()
    
    def get_popular_articles(self, limit):
        return LikesModel().get_popular_articles(limit=limit)

    def get_recent_popular_articles(self, days, limit):
        return LikesModel().get_recent_popular_articles(days=days, limit=limit)
    
    # просмотры
    def get_viewers(self):
        return ViewsModel(art_id=self.id).get_viewers()


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

#найти статьи раздела по названию
@article_router.post("/search/title/{title}")
def search_articles_by_title(title): # data = Body()
    return ArticleSearchModel().search_by_title(title)

#найти статьи раздела по заголовку
@article_router.post("/search/preview/{preview}")
def search_articles_by_preview(preview): # data = Body()
    return ArticleSearchModel().search_by_preview(preview)

#найти статьи раздела по тексту
@article_router.post("/search/text/{text}")
def search_articles_by_text(text): # data = Body()
    return ArticleSearchModel().search_by_text(text)

#загрузить дату в эластик
@article_router.put("/elastic_data")
def upload_articles_to_es():
    return ArticleSearchModel().dump()

#найти статьи раздела
@article_router.post("/search")
def search_articles(data = Body()):
    pass

#лайки и просмотры
@article_router.get("/get_all_likes/{ID}")
def get_all_likes(ID: int):
    return Article(id = ID).get_all_likes()

@article_router.get("/get_article_likers/{ID}")
def get_article_likers(ID: int):
    return Article(id = ID).get_article_likers()

@article_router.get("/get_popular_articles/{limit}")
def get_popular_articles(limit: int):
    return Article().get_popular_articles(limit)

@article_router.get("/get_recent_popular_articles/{days}/{limit}")
def get_recent_popular_articles(days: int, limit: int):
    return Article().get_recent_popular_articles(days=days, limit=limit)

@article_router.get("/get_viewers/{ID}")
def get_viewers(ID: int):
    return Article(id = ID).get_viewers()
