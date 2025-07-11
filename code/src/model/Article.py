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
from src.services.Idea import Idea
from src.services.Auth import AuthService

import re
import json
import datetime
import asyncio
import types

from fastapi import APIRouter, Body, Request

article_router = APIRouter(prefix="/article", tags=["Статьи"])

def make_date_valid(date):
    if date is not None:
        try:
            return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        except:
            return datetime.datetime.strptime(date, '%d.%m.%Y')
    else:
        return None

def take_value(PROPERTY):
    if type(PROPERTY) == type(dict()):
        return list(PROPERTY.values())[0]
    elif type(PROPERTY) == type(list()):
        return PROPERTY[0]
    else:
        return None

def dict_to_indirect_data(data, property_value_dict):
    res = dict()
    for key in property_value_dict.keys():
        if key in data:
            res[property_value_dict[key]] = take_value(data[key])
    return res



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
        elif "PROPERTY_356" in data:
            preview = list(data['PROPERTY_356'].values())[0]
            #data.pop('PROPERTY_356')
        elif "PROPERTY_488" in data:
            preview = list(data['PROPERTY_488'].values())[0]
            # data.pop('PROPERTY_488')
        elif "PROPERTY_1127" in data:
            preview = list(data['PROPERTY_1127'].values())[0]
            # data.pop('PROPERTY_1127')
        elif "PROPERTY_677" in data:
            preview = list(data['PROPERTY_677'].values())[0]
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
        elif "PROPERTY_365" in data:
            content = list(data['PROPERTY_365'].values())[0]
            # data.pop('PROPERTY_365')
        else:
            keys = ["PROPERTY_1239", "PROPERTY_457", "PROPERTY_477", "PROPERTY_340", "PROPERTY_291", "PROPERTY_358", "PROPERTY_1034", "PROPERTY_348"]
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
        

        #отдельно обарботаем случай Доски почета
        if self.section_id == 14:
            #соберём совою indirect_data
            if type(data['PROPERTY_1036']) == type(list()):
                uuid = int(data['PROPERTY_1036'][0])
            else:
                uuid = int(list(data['PROPERTY_1036'].values())[0])

            if type(data['PROPERTY_1035']) == type(list()):
                year = data['PROPERTY_1035'][0]
            else:
                year = list(data['PROPERTY_1035'].values())[0]
            
            if type(data['PROPERTY_1037']) == type(list()):
                position = data['PROPERTY_1037'][0]
            else:
                position = list(data['PROPERTY_1037'].values())[0]
            
            if type(data['PROPERTY_1039']) == type(list()):
                department = data['PROPERTY_1039'][0]
            else:
                department = list(data['PROPERTY_1039'].values())[0]
            
            if "PROPERTY_1113" in data:
                if type(data['PROPERTY_1113']) == type(list()):
                    pre_award = data['PROPERTY_1113'][0]
                else:
                    pre_award = list(data['PROPERTY_1113'].values())[0]
                award = "Почетная грамота" if int(pre_award) == 888 else "Сотрудник года"
            else:
                award = "Сотрудник года"

            user = User(id=uuid).search_by_id()
            photo = user["photo_file_url"]
            indirect_data = json.dumps({
                "uuid" : uuid,
                "year" : year,
                "position" : position,
                "department" : department,
                #внедряю компрессию
                "photo_file_url" : photo.replace("user_files", "compress_image/user"),
                "award" : award,
                "location" : ""
            })

        # отдельно обработаем случай конкурсов ЭМК
        elif self.section_id == 7:
            nomination = None
            age_group = None

            if 'PROPERTY_1071' in data:
                if int(data['PROPERTY_1071'][0]) == 664:
                    nomination = 'Дети от 5 до 7 лет'
                elif int(data['PROPERTY_1071'][0]) == 1775:
                    nomination = 'Дети от 8 до 11 лет'
                elif int(data['PROPERTY_1071'][0]) == 1776:
                    nomination = 'Дети от 12 до 16 лет'
        


            if 'PROPERTY_1072' in data:
                if int(data['PROPERTY_1072'][0]) == 671:
                    age_group = 'Дети от 5 до 7 лет'
                elif int(data['PROPERTY_1072'][0]) == 672:
                    age_group = 'Дети от 8 до 11 лет'
                elif int(data['PROPERTY_1072'][0]) == 673:
                    age_group = 'Дети от 12 до 16 лет'

            

            indirect_data = json.dumps({
                "created_by" : data['CREATED_BY'],
                "author" : str(data['PROPERTY_1070'][0]),
                "nomination" : nomination,
                "age_group" : age_group,
                "representative_id" : int(data['PROPERTY_1074'][0]),
                "representative_text" : str(data['PROPERTY_1075'][0])
            })
            '''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #добавим лайки и просмотры PROPERTY_1073
            if 'PROPERTY_1073' in data:
                for user_id in data['PROPERTY_1073']:
                     # проверяем есть ли такие юзеры в бд
                        user_exist = User(int(user_id)).search_by_id()
                        if isinstance(user_exist, types.CoroutineType) or user_exist is None:
                            continue
                        else:
                            LikesModel(user_id=int(user_id), art_id=int(data['ID'])).add_or_remove_like()
            '''

        #отдельно обарботаем случай Блогов
        elif self.section_id == 15:
            #собираем из двух статей одну
            uuid = None
            photo = None
            if "PROPERTY_444" in data:
                if type(data['PROPERTY_444']) == type(list()):
                    uuid = int(data['PROPERTY_444'][0])
                else:
                    uuid = int(list(data['PROPERTY_444'].values())[0])
                    
                #отдельно вытащить превьюшки людей
                user = User(id=uuid).search_by_id()
                photo = user["photo_file_url"]
                #photo = photo.replace("user_files", "compress_image/user")
            company = None
            if "PROPERTY_1022" in data and take_value(data["PROPERTY_1022"]) == "6180":
                company = 10834#"АО «НПО «Регулятор»"
            elif  "PROPERTY_1022" in data and take_value(data["PROPERTY_1022"]) == "6178":
                company = 10815#"АО «САЗ»"

            if "PROPERTY_453" in data and take_value(data["PROPERTY_453"]) == "335":
                data["active"] = True
            else:
                data["active"] = False
            
            if "PROPERTY_446" in data and take_value(data["PROPERTY_446"]) == "333":
                data["active"] = True
            else:
                data["active"] = False
            
            link = None
            if "PROPERTY_1247" in data:
                link = take_value(data["PROPERTY_1247"])
            
            

            #отдельно обрабатываем файлы
            if "PROPERTY_1239" in data:
                content = take_value(data["PROPERTY_1239"])
            if content is not None:
                #хватаю url
                matches = re.findall(r'src="([^"]*)"', content)
                for url in matches:
                    #качаю файл новым методом
                    if url != "https://portal.emk.ru/bitrix/tools/disk/uf.php?attachedId=128481&auth%5Baplogin%5D=1&auth%5Bap%5D=j6122m0ystded5ag&action=show&ncc=1":
                        new_url = File().upload_by_URL(url=url, art_id=self.id)
                        print(url, "-->", new_url)
                        #заменяю url на новый
                        #content = re.sub(r'src="([^"]*)"', f'src="{new_url}"', content)
                        
                        content = content.replace(url, new_url)



            indirect_data = {
                "TITLE" : data["TITLE"],
                "author_uuid" : uuid,
                "company" : company, 
                "link" : link,
                "photo_file_url" : photo,
            }
            
            
            #файлы для Интранета ???сработает??? - да
            keys = [
                "PROPERTY_1023", #фото превью
                "PROPERTY_1222", #ссылка на youtube
                "PROPERTY_455",
                "PROPERTY_1020",
            ]
            for key in keys:
                if key in data:
                    indirect_data[key] = data[key]
        
        #отдельно забираю сортировку для Памятки Новому Сотруднику
        elif self.section_id == 18:
            sort = None
            if "PROPERTY_475" in data:
                sort = take_value(data["PROPERTY_475"])
            indirect_data = {"sort" : sort}

        #Референсы и опыт поставок
        elif self.section_id == 25:
            
            industryId = None
            if "PROPERTY_681" in data:
                industryId = take_value(data["PROPERTY_681"])
            
            industry = None
            values_dict = {
                None : "Прочие",
                "8308" : "Прочие",
                "8307" : "Энергетика",
                "8306" : "Химия",
                "8305" : "Нефтегаз"
            }
            industry = values_dict[industryId]

            enterpriseId = None
            if "PROPERTY_680" in data:
                enterpriseId = take_value(data["PROPERTY_680"])
            
            enterprise = None
            values_dict = {
                None : "Ошибка",
                "6185" : "ООО «Пульсатор»",
                "6184" : "ООО «Техно-Сфера»",
                "6183" : "ООО «АРМАТОМ»",
                "6182" : "АО «Тулаэлектропривод»",
                "6181" : "ООО «ТехПромАрма»",
                "6180" : "АО «НПО Регулятор»",
                "6179" : "ЗАО «Курганспецарматура»",
                "6178" : "ЗАО «Саратовский арматурный завод»"
            }
            enterprise = values_dict[enterpriseId]
            
            indirect_data = {
                "industry" : industry,
                "industryId" : industryId,
                "enterprise" : enterprise,
                "enterpriseId" : enterpriseId
            }

        #Благотворительные проекты
        elif self.section_id == 55:
            property_dict = {
                "PROPERTY_435" : "organizer",
                "PROPERTY_347" : "phone_number"
            }
            
            indirect_data = dict_to_indirect_data(data, property_dict)

        #Учебный центр (Литература)
        elif self.section_id == 175:
            property_dict = {
                "PROPERTY_489" : "subsection_id",
                "PROPERTY_488" : "author"
            }
            
            indirect_data = dict_to_indirect_data(data, property_dict)

            subsection_id = indirect_data["subsection_id"]
            values_dict = {
                None : "Нет данных",
                "339" : "Техническая литература",
                "340" : "Обучающие материалы",
                "1020" : "Диджитал и IT",
                "1021" : "Психология и развитие",
                "1761" : "Обучающие материалы: продажи B2B",
                "1762" : "Обучающие материалы: Эффективные переговоры",
                "1763" : "Обучающие материалы: Профессиональное планирование для регулярного менеджмента",
            }
            indirect_data["subsection"] = values_dict[subsection_id]

        #Учебный центр (Тренинги)
        elif self.section_id == 172:
            
            if "PROPERTY_371" in data:
                content = data["PROPERTY_371"][0]["TEXT"]
                content_type = data["PROPERTY_371"][0]["TYPE"]

            property_dict = {
                "PROPERTY_369" : "event_date",
                "PROPERTY_437" : "author",
                "PROPERTY_432" : "participants"
            }
            
            indirect_data = dict_to_indirect_data(data, property_dict)
            participants = []
            if "participants" in indirect_data:
                for user_uuid in indirect_data["participants"]:
                    user = User(id=user_uuid).search_by_id()
                    if user is not None:
                        last_name = user['last_name']
                        name = user['name']
                        second_name = user['second_name']

                        fio = f"{last_name} {name} {second_name}"
                        photo = user["photo_file_url"]
                        work_position = user["indirect_data"]["work_position"]

                        participants.append({
                            "fio" : fio,
                            "photo_file_url" : photo,
                            "work_position" : work_position
                        })



            reviews_props = data["reviews"]
            reviews = []
            if reviews_props != []:
                for feedback_props in reviews_props:
                    text = ""
                    if "PROPERTY_486" in feedback_props:
                        text = list(feedback_props["PROPERTY_486"].values())[0]["TEXT"]
                    
                    name = "",
                    if "NAME" in feedback_props:
                        name = feedback_props["NAME"]
                    
                    stars = "",
                    if "PROPERTY_501" in feedback_props:
                        stars = list(feedback_props["PROPERTY_501"].values())[0]
                        print(feedback_props["PROPERTY_501"], stars)

                    feedback = {
                        "reviewer" : name,
                        "text" : text,
                        "stars" : stars,
                    }
                    reviews.append(feedback)

            indirect_data["reviews"] = reviews
            indirect_data["participants"] = participants
        
        #Корпоративная газета ЭМК
        elif self.section_id == 34:
            img_url = File().save_by_URL(url=data["image"], art_id=self.id, is_preview=True)
            file_url = File().save_by_URL(url=data["file"], art_id=self.id)
            indirect_data = {
                "year" : data["year"],
                "photo_file_url" : img_url,
                "pdf" : file_url,
            }

        #Гид по предприятиям
        elif self.section_id == 41:
            
            reports = data["reports"]
            tours = data["tours"]

            print(reports)
            if reports != []:
                for rep in reports:
                    act = True
                    if rep["BP_PUBLISHED"] != "Y":
                        act = False
                    
                    photo_file_url = None
                    if "PROPERTY_669" in rep:
                        photo = take_value(rep["PROPERTY_669"])
                        print(photo)
                        #скачать и вытащить ссылку
                        files = [photo]
                        art_id = rep["ID"]
                        inf_id = "98"
                        is_preview = False
                        
                        file_data = File(b24_id=photo).upload_inf_art(art_id, is_preview, False, inf_id)
                        print(file_data)
                        
                        url = file_data["file_url"]
                        #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!
                        photo_file_url = f"http://intranet.emk.org.ru{url}"
                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                            
                    
                    rp = {
                        "id" : rep["ID"],
                        "name" : rep["NAME"],
                        "active" : act,
                        "date" : take_value(rep["PROPERTY_667"]),
                        "photo_file_url" : photo_file_url,
                        "link" : take_value(rep["PROPERTY_670"]) #!!!!!!!!!!!!!! сслыка на youtube
                    }
                    print(rp)

                    reports.append(rep)
            
            if tours != []:
                for tour in tours:
                    act = True
                    if tour["BP_PUBLISHED"] != "Y":
                        act = False
                    
                    photo_file_url = None
                    if "PROPERTY_498" in tour:
                        photo = take_value(tour["PROPERTY_498"])
                        #скачать и вытащить ссылку
                        art_id = tour["ID"]
                        inf_id = "84"
                        is_preview = False
                        file_data = File(b24_id=photo).upload_inf_art(art_id, is_preview, False, inf_id)
                        
                        url = file_data["file_url"]
                        #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!
                        photo_file_url = f"http://intranet.emk.org.ru{url}"
                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    
                    rp = {
                        "id" : tour["ID"],
                        "name" : tour["NAME"],
                        "active" : act,
                        "3D_files_path" : take_value(tour["PROPERTY_497"]),
                        "photo_file_url" : photo_file_url
                    }
            
            indirect_data = {
                "PROPERTY_463" : data["PROPERTY_463"],
                "reports" : reports,
                "tours" : tours
            }


        else:
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
            
            #Блоги
            "PROPERTY_1023", 
            #"PROPERTY_1222", #ссылка на youtube
            #"PROPERTY_1203", #ссылка на youtube
            "PROPERTY_455",
            "PROPERTY_1020",
            "PROPERTY_1246", #QR-код Земской
            
            #Референсы
            "PROPERTY_678",
            #"PROPERTY_679",

            "PROPERTY_476",

            #"PROPERTY_670", #!!! сслыка на ютуб !!!
            "PROPERTY_669",

            #Гид по предприятиям
            "PROPERTY_463",

            "PROPERTY_498",

            "PROPERTY_289",
            # "PROPERTY_296",

            "PROPERTY_399",

            "PROPERTY_400",
            #"PROPERTY_402",
            "PROPERTY_407",

            #"PROPERTY_409", #!!! сслыка на ютуб !!!

            "PROPERTY_476",
            "PROPERTY_1025",
            "PROPERTY_356",

            #вложения
            "PROPERTY_478",
            "PROPERTY_491",
            "PROPERTY_366",
        ]

        preview_file = [
            "PROPERTY_399",
            "PROPERTY_407",
            "PROPERTY_372",
            "PROPERTY_337",
            "PROPERTY_342",
            "PROPERTY_476",
            "PROPERTY_669",
            "PROPERTY_463",
            "PROPERTY_498",
            "PREVIEW_PICTURE",
            "PROPERTY_356",
        ]
        
        # находим файлы статьи
        files = []
        preview_images = []
        need_all_method = True
        #собираем данные о файлах
        for file_property in files_propertys:
            
            if file_property in data:
                # if art_id == 12221:
                #     print(data, art_id)

                #обрабатываются дефолтным методом битры
                if file_property in ["PROPERTY_289", "PROPERTY_400", "PROPERTY_373", "PROPERTY_678", "PROPERTY_366"]:
                    need_all_method = False
                try:
                    # выцепить id файла
                    # "PREVIEW_PICTURE" не обрабатывается, тип - строка
                    # "DETAIL_PICTURE" тоже не обработается если строка
                    if type(data[file_property]) == type(dict()):
                        for file_id in data[file_property].values():
                            if type(file_id) == type(str()):
                                files.append(file_id)
                                if file_property in preview_file:
                                        preview_images.append(file_id)
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
                                    if file_property in preview_file:
                                            preview_images.append(file_id)
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
                        LogsMaker().warning_message("Некорректные данные в поле ", file_property, f"Данные: {type(data[file_property])}", f"Ищи в {inf_id}, {art_id}")
                        # print("Некорректные данные в поле ", file_property, f"Данные: {type(data[file_property])}", f"Ищи в {inf_id}, {art_id}")
                        
                except Exception as e:
                    return LogsMaker().error_message(e)
                    # print("Ошибка обработки в инфоблоке", sec_inf[i], "в поле", file_property)
        
        if files == []:
            return []
        else:
            files_data = []
            #проеверяем, нужно ли обновить файлы?
            # if art_id == 12221:
            #     print(f'{files} проверяет на обновлениеб {preview_images} - сработали ли?')

            files_to_add = File().need_update_file(art_id, files)

            if files_to_add != []:
                for f_id in files:
                    print(f"Качаю файл {f_id} статьи {art_id} инфоблока {inf_id}, использование метода Матренина - {need_all_method}")
                    try:
                        is_preview = f_id in preview_images
                        file_data = File(b24_id=f_id).upload_inf_art(art_id, is_preview, need_all_method, inf_id)
                        #sprint(f'{f_id} файл добавлен в монго', art_id, inf_id)
                        files_data.append(file_data)
                    except:
                        LogsMaker().warning_message(f"Не получилось по хорошему скачать файл {f_id} статьи {art_id} инфоблока {inf_id}, метода Матренина по умолчанию - {need_all_method}")
                        is_preview = f_id in preview_images
                        file_data = File(b24_id=f_id).upload_inf_art(art_id, is_preview, True, inf_id)
                        # sprint(f'{f_id} файл добавлен в монго', art_id, inf_id)
                        files_data.append(file_data)


            else:
                pass
                #print(f'добавлять/обновалять не нужно {art_id} - статья, {inf_id} - инфоблок')

            return files_data

    def add(self, article_data):
        return ArticleModel().add_article(self.make_valid_article(article_data))

    def uplod(self):
        '''
        ! Не повредить имеющиеся записи и структуру
        ! Выгрузка файлов из инфоблоков
        ✔️ - готов и отлажен
        ☑️ - готов и тестируется
        ♻️ - в разработке сейчас
        ❌ - ожидает работы
        '''

        # создание индексов в Mongo
        File().index_files()

        # кастомный прогрессбар
        logg = LogsMaker()

        '''
        ! Сопоставить section_id из Интранета и IBLOCK_ID из B24
        '''

        '''однозначно'''
        sec_inf = {
            13 : "149", # Наши люди ✔️
            #14 : "123", #Доска почёта ☑️
            16 : "122", # Видеоитервью ✔️
            
            32 : "132", # Новости организационного развития ✔️
            #53 : "62", # Афиша ✔️
            #54 : "55", # Предложения партнеров ✔️
            #55 : "56", # Благотворительные проекты ✔️

            #25 : "100", #Референсы и опыт поставок ✔️
            #175 : "60" #Учебный центр (Литература) ✔️
        }
        

        #проходимся по инфоблокам
        for i in logg.progress(sec_inf, f"Загрузка данных инфоблоков {sec_inf.values} "):

            # запрос в B24
            self.section_id = sec_inf[i]
            infs = self.get_inf()

            #инфоблок не пустой
            if infs != []:
                for inf in infs:
                    artDB = ArticleModel(id = inf["ID"], section_id = i)
                    self.section_id = i
                    # if self.section_id == 16:
                    #     print('тут загуржаем', type(inf))
                    if artDB.need_add():
                        logg.warning_message(f'Добавил статью, {inf["ID"]}')
                        self.add(inf)
                    elif artDB.update(self.make_valid_article(inf)):
                        #проверить апдейт файлов
                        pass


        '''с параметрами'''
        #один section_id - несколько IBLOCK_ID
        sec_inf = {
            #15 : ["75", "77"], #Блоги ✔️
            #18 : ["81", "82"], #Памятка ✔️
            41 : ["98", "78", "84"], #Гид по предприятиям ♻️ сделать сервис
            #172 : ["61", "83"] #Учебный центр (Проведённые тренинги)  ♻️
        }

        '''
        #Учебный центр (Проведённые тренинги)
        self.section_id = "61"
        sec_inf_title = self.get_inf()
        for title_inf in logg.progress(sec_inf_title, "Загрузка данных инфоблоков 61, 83 "):
            title_id = title_inf["ID"]
            title_data = title_inf

            data = dict()

            #добавить все данные статьи
            for key in title_data:
                data[key] = title_data[key]
            
            data["ID"] = title_data["ID"]
            data["TITLE"] = title_data["NAME"]
            print(data["ID"])
            data["reviews"] = []

            # пройти по инфоблоку тренингов
            self.section_id = "83"
            sec_inf_data = self.get_inf()
            for data_inf in sec_inf_data:
                #если эта статья принадлежит иинфоблоку
                if "PROPERTY_484" in data_inf and take_value(data_inf["PROPERTY_484"]) == title_id:
                    #добавить отзывы
                    data["reviews"].append(data_inf)

            #загрузить данные в таблицу
            data["section_id"] = 172
            self.section_id = 172
            artDB = ArticleModel(id=data["ID"], section_id=self.section_id)
            if artDB.need_add():
                self.add(data)
            elif artDB.update(self.make_valid_article(data)):
                pass
        
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
                    logg.warning_message(f'##################, {data_inf["ID"]}')
                    

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
        '''
 

        

        #Гид по предприятиям
        # пройти по инфоблоку заголовков
        self.section_id = "78"
        sec_inf_title = self.get_inf()
        for title_inf in logg.progress(sec_inf_title, "Загрузка данных инфоблоков 78, 98 и 84"):
            art_id = title_inf["ID"]
            data = title_inf
            data["reports"] = []
            data["tours"] = []

            # пройти по инфоблоку репортажей
            self.section_id = "98"
            sec_inf_data = self.get_inf()
            for data_inf in sec_inf_data:
                #if "PROPERTY_671" in data_inf:
                data_title_id = list(data_inf["PROPERTY_671"].values())[0]
                # если эта статья принадлежит иинфоблоку

                if data_title_id == art_id:
                    dt = dict()

                    # добавить все данные статьи
                    for key in data_inf:
                        dt[key] = data_inf[key]

                    dt["ID"] = data_inf["ID"]
                    dt["TITLE"] = title_inf["NAME"]

                    data["reports"].append(dt)
                    
            # пройти по инфоблоку репортажей
            self.section_id = "84"
            sec_inf_data = self.get_inf()
            for data_inf in sec_inf_data:
                #if "PROPERTY_671" in data_inf:
                data_title_id = list(data_inf["PROPERTY_496"].values())[0]
                # если эта статья принадлежит иинфоблоку

                if data_title_id == art_id:
                    dt = dict()

                    for key in data_inf:
                        dt[key] = data_inf[key]

                    dt["ID"] = data_inf["ID"]
                    dt["TITLE"] = title_inf["NAME"]

                    data["tours"].append(dt)

            data["section_id"] = 41 # Гид по предприятиям
            self.section_id = 41
            # загрузить данные в таблицу
            artDB = ArticleModel(id=data["ID"], section_id=self.section_id)
            if artDB.need_add():
                self.add(data)
            elif artDB.update(self.make_valid_article(data)):
                pass

        '''
        #несколько section_id - один IBLOCK_ID
        sec_inf = {
            31 : "50", #Актуальные новости ✔️
            51 : "50"  #Корпоративные события ✔️
        }

        # пройти по инфоблоку
        self.section_id = "50"
        art_inf = self.get_inf()
        for art in logg.progress(art_inf, "Загрузка данных разделов \"Актуальные новости\", \"Корпоративные события\" и \"Видеорепортажи\" "):
            if art["ID"] == '13486':
                logg.warning_message(f'{art["ID"]} новостьь которая проникает не туда')
                # print(art, ' новость')
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
                    logg.warning_message(f'Статья - Name:{art["NAME"]}, id:{art["ID"]} уже не актуальна')
                    # print("Статья", art["NAME"], art["ID"], "уже не актуальна")
                elif artDB.update(self.make_valid_article(art)):
                    # сюда надо что-то дописать
                    pass
        '''
                


        '''
        #несколько section_id - несколько IBLOCK_ID
        sec_inf = {
            42 : ["68", "69"], #Официальные события ❌
            52 : ["68", "69"]  #Корпоративная жизнь в фото ❌
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
            self.section_id = 111 # потом изменить
            artDB = ArticleModel(id=art["ID"], section_id=self.section_id)
            if artDB.need_add():
                self.add(art)
            elif artDB.update(self.make_valid_article(art)):
                pass
        '''

        '''
        #Корпоративная газета ✔️
        data = [
            {
                "ID" : "342022",
                "IBLOCK_ID" : "2022",
                "NAME" : "№1 (2022)",
                "image" : "https://portal.emk.ru/intranet/news/gazeta/img/emk-001.jpg",
                "file" : "https://portal.emk.ru/intranet/news/gazeta/pdf/emk-001.pdf",
                "year" : "2022",
                "DATE_CREATE" : "01.01.2022",
            },
            {
                "ID" : "342023",
                "IBLOCK_ID" : "2023",
                "NAME" : "№2 (2023)",
                "image" : "https://portal.emk.ru/intranet/news/gazeta/img/emk-002.jpg",
                "file" : "https://portal.emk.ru/intranet/news/gazeta/pdf/emk-002.pdf",
                "year" : "2023",
                "DATE_CREATE" : "01.01.2023",
            },
            {
                "ID" : "342024",
                "IBLOCK_ID" : "2024",
                "NAME" : "№3 (2024)",
                "image" : "https://portal.emk.ru/intranet/news/gazeta/img/emk-003.jpg",
                "file" : "https://portal.emk.ru/intranet/news/gazeta/pdf/emk-003.pdf",
                "year" : "2024",
                "DATE_CREATE" : "01.01.2024",
            }
        ]

        for art in data:
            self.section_id = 34 # потом изменить
            artDB = ArticleModel(id=art["ID"], section_id=self.section_id)
            if artDB.need_add():
                self.add(art)
            elif artDB.update(self.make_valid_article(art)):
                pass
        
        #Конкурсы ЭМК 7 секция
        self.section_id = "128"
        competitions_info = self.get_inf()
        if competitions_info != []:
            for inf in logg.progress(competitions_info, "Загрузка 'Конкурсы ЭМК'"):
                #art_id = inf["ID"]
                self.section_id = 7
                art_DB = ArticleModel(id=inf["ID"], section_id=self.section_id)
                if art_DB.need_add():
                    self.add(inf)
                elif art_DB.update(self.make_valid_article(inf)):
                    pass
        '''
        


        '''самобытные блоки'''
        # полная статика
            # 11 Наша компания -> Наша компания ✔️
            # 12 История компании -> История компании ✔️

            # 110 Техника безопасности -> Техника безопасности ✔️
            # 34 Корпоративная газета ЭМК -> газеты ❌
            # 41 Гид по предприятиям -> 3D тур ♻️

        #переделки
            # 19 Дни рождения ✔️
            # 21 Подбор оборудования ✔️
            # 22 Поздравительная открытка ♻️
            # 23 ChatGPT ❌
            # 24 Разрешительная документация и сертиффикаты ❌
            # Новые сотрудники ✔️
            # Личный кабинет ✔️
            # Есть Идея ✔️

            #РЕДАКТОРКА

        #новые разделы
            # конфигуратор НПО Регулятор ✔️
            # DeepSeek ❌
            # VCard ✔️
            # система личной эффективности ❌
            # магазин мерча ❌

            # QR-код на САЗ ❌
            # YandexGPT5 + Yandex ART ❌
            # Юбилей САЗ ❌

        # Дамп данных в эластик
        self.dump_articles_data_es()

        return {"status" : True}

    def search_by_id(self, session_id=""):
        art = ArticleModel(id = self.id).find_by_id()
        files = File(art_id = int(self.id)).get_files_by_art_id()
        art['images'] = []
        art['videos_native'] = []
        art['videos_embed'] = []
        art['documentation'] = []
        
        for file in files:
            #файлы делятся по категориям
            if "image" in file["content_type"] or "jpg" in file["original_name"] or "jpeg" in file["original_name"] or "png" in file["original_name"]:
                url = file["file_url"]
                #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!
                art['images'].append(f"http://intranet.emk.org.ru{url}")
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            elif "video" in file["content_type"]:
                url = file["file_url"]
                art['videos_native'].append(f"http://intranet.emk.org.ru{url}")
            elif "link" in file["content_type"]:
                art['videos_embed'].append(file)
            else:
                art['documentation'].append(file)
        
        art["preview_file_url"] = self.get_preview()

        null_list = [17, 19, 111, 112, 14, 18, 25, 54, 55, 53, 7, 34, 175] # список секций где нет лайков

        if art['section_id'] not in null_list:
            user_id = self.get_user_by_session_id(session_id=session_id)
            if user_id is not None:
                # сюда добавить момент с лайками и просмотрами
                views_count = self.add_art_view() 

                # вызов количества лайков
                likes_count = self.get_all_likes()

                # нужно притянуть айдишник пользователя
                has_user_liked = User(id=user_id).has_liked(art_id=self.id)

                views_count['likes'] = {'count': likes_count, 'likedByMe': has_user_liked}
                
                art['reactions'] = views_count

        #обработаем конкурсы эмк где есть лайки, но нет просмотров
        elif art['section_id'] == 7:
            # вызов количества лайков
            user_id = self.get_user_by_session_id(session_id=session_id)
            if user_id is not None:
                likes_count = self.get_all_likes()
                has_user_liked = User(id=user_id).has_liked(art_id=self.id)
                art['reactions'] = {'count': likes_count, 'likedByMe': has_user_liked}
        
        return art

    def get_preview(self):
        files = File(art_id = int(self.id)).get_files_by_art_id()
        for file in files:
            if file["is_preview"]:
                url = file["file_url"]
                #внедряю компрессию
                if self.section_id == "18": #отдельный алгоритм для памятки новому сотруднику
                    preview_link = url.split("/")
                    preview_link[-2] = "compress_image/yowai_mo"
                    url = '/'.join(preview_link)
                #Для баготворительных проектов компрессия не требуется
                elif self.section_id == "55":
                    return f"http://intranet.emk.org.ru{url}"
                else:
                    preview_link = url.split("/")
                    preview_link[-2] = "compress_image"
                    url = '/'.join(preview_link)
                #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!!!!!
                return f"http://intranet.emk.org.ru{url}"
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #находим любую картинку, если она есть
        for file in files:
            if "image" in file["content_type"] or "jpg" in file["original_name"] or "jpeg" in file["original_name"] or "png" in file["original_name"]:
                url = file["file_url"]
                #внедряю компрессию
                if self.section_id == "18": #отдельный алгоритм для памятки новому сотруднику
                    preview_link = url.split("/")
                    preview_link[-2] = "compress_image/yowai_mo"
                    url = '/'.join(preview_link)
                #Для баготворительных проектов компрессия не требуется
                elif self.section_id == "55":
                    return f"http://intranet.emk.org.ru{url}"
                else:
                    preview_link = url.split("/")
                    preview_link[-2] = "compress_image"
                    url = '/'.join(preview_link)
                #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!!!!!
                return f"http://intranet.emk.org.ru{url}"
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        return None
        


    def search_by_section_id(self, session_id=""):
        if self.section_id == "0":
            main_page = [112, 19, 32, 4, 111, 31, 16, 33, 9, 53, 51] #section id
            page_view = []

            user_id = self.get_user_by_session_id(session_id=session_id)

            for page in main_page: # проходимся по каждой секции
                sec = self.main_page(page, user_id)
                page_view.append(sec) 
            page_view[-3]['content'] = [page_view[-2], page_view[-1]]
            del page_view[-2:]

            return page_view
        
        elif self.section_id == "19":
            users_bday_info = []
            date_bday = datetime.datetime.now().strftime("%d.%m")
            users = User().get_birthday_celebrants(date_bday)
            return users

        elif self.section_id == "112":
            return User().get_new_workers()
        

        
        elif self.section_id == "25" or self.section_id == "175":
            active_articles = []
            result = ArticleModel(section_id = self.section_id).find_by_section_id()
            for res in result:
                if res['active']:
                    self.id = res["id"]

                    #взаимствую логику поиска файлов из метода поиска статей по их id
                    art = ArticleModel(id = self.id).find_by_id()
                    files = File(art_id = int(self.id)).get_files_by_art_id()
                    res['images'] = []
                    res['videos_native'] = []
                    res['videos_embed'] = []
                    res['documentation'] = []
                    
                    for file in files:

                        
                        url = file["file_url"]
                        #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!
                        file["file_url"] = f"http://intranet.emk.org.ru{url}"
                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                        #файлы делятся по категориям
                        if "image" in file["content_type"] or "jpg" in file["original_name"] or "jpeg" in file["original_name"] or "png" in file["original_name"]:
                            res['images'].append(file)
                        elif "video" in file["content_type"]:
                            res['videos_native'].append(file)
                        elif "link" in file["content_type"]:
                            res['videos_embed'].append(file)
                        else:
                            
                            res['documentation'].append(file)

                    active_articles.append(res)
            
            return sorted(active_articles, key=lambda x: x['id'], reverse=True)

        elif self.section_id == "34":
            result = ArticleModel(section_id = self.section_id).find_by_section_id()
            sorted_active_articles = sorted(result, key=lambda x: x['id'], reverse=True)
            return sorted_active_articles

        elif self.section_id == "8": #Есть Идея
            ideas = Idea().get_ideas(session_id)
            if ideas is not None:
                sorted_active_articles = sorted(ideas, key=lambda x: x['number'], reverse=False)
                return sorted_active_articles
            else:
                return {"err" : "Auth Err"}

        else:
            null_list = [17, 19, 111, 112, 14, 18, 25, 54, 55, 53, 7, 34] # список секций где нет лайков
            active_articles = []
            result = ArticleModel(section_id = self.section_id).find_by_section_id()
            for res in result:
                if not (self.section_id == "16" and ("PROPERTY_1025" not in res['indirect_data'] or res['indirect_data']['PROPERTY_1025'] is None)) and res['active']:
                    
                    self.id = res["id"]
                    res["preview_file_url"] = self.get_preview()
                    # сюда лайки и просмотры

                    if int(self.section_id) not in null_list: # добавляем лайки и просмотры к статьям раздела. Внимательно добавить в список разделы без лайков
                        user_id = self.get_user_by_session_id(session_id=session_id)
                        if user_id is not None:
                            print('не сработалло', type(self.section_id))
                            views_count = self.get_art_views()
                            likes_count = self.get_all_likes()
                            has_user_liked = User(id=user_id).has_liked(art_id=self.id)
                            
                            likes = {'count': likes_count, 'likedByMe': has_user_liked}
                            reactions = {'views': views_count, 'likes': likes}
                            res['reactions'] = reactions

                    #обработаем конкурсы эмк где есть лайки, но нет просмотров
                    elif res['section_id'] == 7:
                        # вызов количества лайков
                        user_id = self.get_user_by_session_id(session_id=session_id)
                        if user_id is not None:
                            likes_count = self.get_all_likes()
                            has_user_liked = User(id=user_id).has_liked(art_id=self.id)
                            res['reactions'] = {'count': likes_count, 'likedByMe': has_user_liked}


                    active_articles.append(res)

            if self.section_id == "111":
                sorted_active_articles = sorted(active_articles, key=lambda x: x['name'], reverse=False)
            #отдельная сортировка Памятки новому сторуднику
            elif self.section_id == "18":
                sorted_active_articles = sorted(active_articles, key=lambda x: int(x['indirect_data']["sort"]), reverse=False)
            else:
                sorted_active_articles = sorted(active_articles, key=lambda x: x['id'], reverse=True)
            return sorted_active_articles
    
    def main_page(self, section_id, user_id):
        
        #Новые сотрудники
        if section_id == 112:
            img_new_workers = []     
            users = User().get_new_workers()  
            for user in users:
                user.pop('position')
                user.pop('department')
                user.pop('user_fio')
                img_new_workers.append(user)
            new_workers_view = {
                'id': section_id,
                'type': 'singleBlock',
                'title': 'Новые сотрудники',
                'images': img_new_workers,
                'href': 'newWorkers',
            } # словарь-заглушка для будущей секции "новые сотрудники"
            return new_workers_view

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

        # Орг развитие
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

            
            self.id = news_id
            image_URL = self.get_preview()
            second_page = {
                'id': section_id, 
                'type': 'singleBlock', 
                'title': 'Организационное развитие', 
                "href": "corpNews", 
                'images': [{'id': news_id, 'image': image_URL}]
                }
            return second_page
        
        # предложить идею
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

        # Открытые вакансии
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

        # Актуальные новости
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
                'href': 'actualArticle',
                'sectionId': 'actualNews',
                'images': []
            }

            business_news = []
            
            image_url = ''
            for i, row in enumerate(sorted_data):
                if i < 5:
                    news = {}
                    self.id = row[0]
                    preview_pict = self.get_preview()

                    if preview_pict is None:
                        image_url = None
                    else:
                        image_url = preview_pict
                    
                    news['id'] = row[0]
                    news['title'] = row[1]
                    # news['description'] = row[2]
                    news['image'] = image_url
                    # сюда реакции
                    if user_id is not None:
                        views_count = self.get_art_views()
                        likes_count = self.get_all_likes()
                        has_user_liked = User(id=user_id).has_liked(art_id=self.id)
                        
                        likes = {'count': likes_count, 'likedByMe': has_user_liked}
                        reactions = {'views': views_count, 'likes': likes}
                        
                        news['reactions'] = reactions
                    business_news.append(news)
            second_page['images'] = business_news
            return second_page

        # Видеоитервью
        elif section_id == 16:
            date_list = [] # список для сортировки по дате
            articles_in_section = ArticleModel(section_id=section_id).find_by_section_id()
            for values in articles_in_section:
                if values["active"] is False:
                        pass
                else:
                    if "PROPERTY_1025" not in values["indirect_data"] or values["indirect_data"]["PROPERTY_1025"] is None:
                        pass
                    else:
                        date_value = [] # список для хранения необходимых данных
                        date_value.append(values["id"])
                        date_value.append(values["name"])
                        date_value.append(values["preview_text"])
                        date_value.append(values["date_creation"])

                        self.id = values["id"]

                        date_list.append(date_value) # получили список с необходимыми данными
            # сортируем по дате
            sorted_data = sorted(date_list, key=lambda x: x[0], reverse=True)

            second_page = {
                'id': section_id,
                'type': 'fullRowBlock',
                'title': 'Видеоинтервью',
                'href': 'videoInterview',
                'sectionId': 'videoInterviews',
                'images': []
            }

            interview_news = []
            
            image_url = ''
            for i, row in enumerate(sorted_data):
                if i < 5:
                    news = {}
                    self.id = row[0]
                    preview_pict = self.get_preview()

                    if preview_pict is None:
                        image_url = None
                    else:
                        image_url = preview_pict
                    
                    news['id'] = row[0]
                    news['title'] = row[1]
                    news['description'] = row[2]
                    news['image'] = image_url                    
                    # сюда реакции
                    if user_id is not None:
                        views_count = self.get_art_views()
                        likes_count = self.get_all_likes()
                        has_user_liked = User(id=user_id).has_liked(art_id=self.id)
                        
                        likes = {'count': likes_count, 'likedByMe': has_user_liked}
                        reactions = {'views': views_count, 'likes': likes}
                        
                        news['reactions'] = reactions
                    interview_news.append(news)
            second_page['images'] = interview_news
            return second_page

        # Видеорепортажи
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
                'href': 'videoReport',
                'sectionId': 'videoReports',
                'images': []
            }

            video_news = []
            
            image_url = ''
            for i, row in enumerate(sorted_data):
                if i < 5:
                    news = {}
                    self.id = row[0]
                    preview_pict = self.get_preview()

                    if preview_pict is None:
                        image_url = None
                    else:
                        image_url = preview_pict
                    
                    news['id'] = row[0]
                    news['title'] = row[1]
                    news['description'] = row[2]
                    news['image'] = image_url
                    # сюда реакции
                    if user_id is not None:
                        views_count = self.get_art_views()
                        likes_count = self.get_all_likes()
                        has_user_liked = User(id=user_id).has_liked(art_id=self.id)
                        
                        likes = {'count': likes_count, 'likedByMe': has_user_liked}
                        reactions = {'views': views_count, 'likes': likes}
                        
                        news['reactions'] = reactions
                    video_news.append(news)
            second_page['images'] = video_news
            return second_page

        # микс
        elif section_id == 9:
            second_page = {
                "id": 9,
                "type": "mixedRowBlock",
                "content": []
            }
            return second_page

        # Афиша
        elif section_id == 53:
            date_list = [] # список для сортировки по дате
            articles_in_section = ArticleModel(section_id=section_id).find_by_section_id()
            for values in articles_in_section:
                if values["active"] is False:
                        pass
                else:
                    date_value = [] # список для хранения необходимых данных
                    date_value.append(values["id"])
                    date_list.append(date_value) # получили список с необходимыми данными
            # сортируем по дате
            sorted_data = sorted(date_list, key=lambda x: x[0], reverse=True)

            afisha = {
                'type': "singleBlock",
                'title': "Афиша",
                'href': 'eventAnnounces',
                'images': []
            } 
            image_url = ''
            afisha_news = []
            for i, row in enumerate(sorted_data):
                if i < 5:
                    news = {}
                    self.id = row[0]
                    preview_pict = self.get_preview()

                    if preview_pict is None:
                        image_url = None
                    else:
                        image_url = preview_pict
                    
                    news['id'] = row[0]
                    news['image'] = image_url
                    afisha_news.append(news)

            afisha['images'] = afisha_news


            return afisha
        
        # Корпоративные события
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
                'href': 'corpEvent',
                'sectionId': 'corpEvents',
                'images': []
            }
            image_url = ''
            corpevents_news = []
            for i, row in enumerate(sorted_data):
                if i < 5:
                    news = {}
                    self.id = row[0]
                    preview_pict = self.get_preview()

                    if preview_pict is None:
                        image_url = None
                    else:
                        image_url = preview_pict
                    
                    news['id'] = row[0]
                    news['title'] = row[1]
                    news['description'] = row[2]
                    news['image'] = image_url
                    # сюда реакции
                    if user_id is not None:
                        views_count = self.get_art_views()
                        likes_count = self.get_all_likes()
                        has_user_liked = User(id=user_id).has_liked(art_id=self.id)
                        
                        likes = {'count': likes_count, 'likedByMe': has_user_liked}
                        reactions = {'views': views_count, 'likes': likes}
                        
                        news['reactions'] = reactions
                    corpevents_news.append(news)

            corpevents['images'] = corpevents_news
            return corpevents

    # лайки
    def get_all_likes(self):
        return LikesModel(art_id=self.id).get_likes_count()

    def add_like(self, session_id):
        user_id = self.get_user_by_session_id(session_id=session_id)
        if user_id is not None:
            return LikesModel(user_id=user_id, art_id=self.id).add_or_remove_like()
        return {"err" : "Auth Err"}

    # просмотры
    def get_art_views(self):
        return ViewsModel(art_id=self.id).get_art_viewes()

    def add_art_view(self):
        return ViewsModel(art_id=self.id).add_art_view()

    # дамп данных по лайкам и просмотрам из Б24
    def upload_likes(self):
        result = [] 
        articles_info = ArticleModel().all()
        null_list = [17, 19, 111, 112, 14, 18, 25, 54, 55, 53, 7, 34] # список секций где нет лайков
        for inf in articles_info:
            if inf['section_id'] not in null_list:
                likes_info = B24().get_likes_views(inf['id'])
                
                if likes_info != "Not found" and 'VOTES' in likes_info.keys():
                    for vote in likes_info['VOTES']:
                        # проверяем есть ли такие юзеры в бд
                        user_exist = User(vote['USER_ID']).search_by_id()
                        if isinstance(user_exist, types.CoroutineType) or user_exist is None:
                            continue
                        else:
                            LikesModel(user_id=vote['USER_ID'], art_id=inf['id']).add_like_from_b24(vote['CREATED_'])

                    #удаляем тех, кто убрал лайк
                    b24_likers = [i['USER_ID'] for i in likes_info['VOTES']]
                    article_likers = LikesModel(art_id=inf['id']).get_article_likers()
                    for usr in article_likers:
                        if usr not in b24_likers:
                            LikesModel(user_id=usr, art_id=inf['id']).remove_like()
                        else:
                            pass

                    ViewsModel(views_count=likes_info['VIEWS'], art_id=inf['id']).add_view_b24()

        return {"status": True}

    # дамп данных в эластик
    def dump_articles_data_es(self):
        return ArticleSearchModel().dump()

    # для статистики лайки и просмотры
    def get_article_likers(self):
        return LikesModel(art_id=self.id).get_article_likers()
    
    def get_popular_articles(self, limit):
        return LikesModel().get_popular_articles(limit=limit)

    def get_recent_popular_articles(self, days, limit):
        return LikesModel().get_recent_popular_articles(days=days, limit=limit)

    def get_user_by_session_id(self, session_id):
        user = dict(AuthService().get_user_by_seesion_id(session_id))

        if user is not None:
            user_uuid = user["user_uuid"]
            username = user["username"]

            #получить и вывести его id
            user_inf = User(uuid = user_uuid).user_inf_by_uuid()
            return user_inf["ID"]
        return None
    
   


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
def get_article(ID, request: Request):
    session_id = ""
    token = request.cookies.get("Authorization")
    if token is None:
        token = request.headers.get("Authorization")
        if token is not None:
            session_id = token
    else:
        session_id = token
    return Article(id = ID).search_by_id(session_id=session_id)

#найти статьи раздела
@article_router.get("/find_by/{section_id}")
def get_articles(section_id, request: Request):
    session_id = ""
    token = request.cookies.get("Authorization")
    if token is None:
        token = request.headers.get("Authorization")
        if token is not None:
            session_id = token
    else:
        session_id = token
    
    return Article(section_id = section_id).search_by_section_id(session_id=session_id)

@article_router.put("/add_or_remove_like/{article_id}")
def add_or_remove_like(article_id, request: Request):
    session_id = ""
    token = request.cookies.get("Authorization")
    if token is None:
        token = request.headers.get("Authorization")
        if token is not None:
            session_id = token
    else:
        session_id = token
    
    return Article(id=article_id).add_like(session_id=session_id)

# поиск по статьям еластик
@article_router.get("/search/full_search_art/{keyword}")
def elastic_search(keyword: str, size_res: int = 20):
    return ArticleSearchModel().elasticsearch_article(key_word=keyword, size_res=size_res)


#выгрузка данных по лайкам в Б24
@article_router.put("/put_b24_likes")
def put_b24_likes():
    return Article().upload_likes()

#лайки и просмотры для статистики
@article_router.get("/get_article_likers/{ID}")
def get_article_likers(ID: int):
    return Article(id = ID).get_article_likers()

@article_router.get("/get_popular_articles/{limit}")
def get_popular_articles(limit: int):
    return Article().get_popular_articles(limit)

@article_router.get("/get_recent_popular_articles/{days}/{limit}")
def get_recent_popular_articles(days: int, limit: int):
    return Article().get_recent_popular_articles(days=days, limit=limit)

# #найти статьи раздела по названию
# @article_router.post("/search/title/{title}")
# def search_articles_by_title(title): # data = Body()
#     return ArticleSearchModel().search_by_title(title)

# #найти статьи раздела по заголовку
# @article_router.post("/search/preview/{preview}")
# def search_articles_by_preview(preview): # data = Body()
#     return ArticleSearchModel().search_by_preview(preview)

# #найти статьи раздела по тексту
# @article_router.post("/search/text/{text}")
# def search_articles_by_text(text): # data = Body()
#     return ArticleSearchModel().search_by_text(text)


#загрузить дату в эластик
# @article_router.put("/elastic_data")
# def upload_articles_to_es():
#     return ArticleSearchModel().dump()


#лайки и просмотры для статистики
# @article_router.get("/get_all_likes/{ID}")
# def get_all_likes(ID: int):
#     return Article(id = ID).get_all_likes()

# @article_router.get("/get_viewers/{ID}")
# def get_viewers(ID: int):
#     return Article(id = ID).get_art_views()
