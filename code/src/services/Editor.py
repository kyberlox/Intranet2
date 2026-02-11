from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie, UploadFile, \
    File
from fastapi.responses import JSONResponse
from typing import Annotated, List, Optional

from .LogsMaker import LogsMaker
from ..base.pSQL.objects.ArticleModel import ArticleModel
# from ..base.mongodb import FileModel
from ..base.pSQL.objects.FilesDBModel import FilesDBModel
from ..model.Article import Article
from ..model.Section import Section
from ..model.File import File as storeFile
from ..model.User import User
from ..model.Tag import Tag

from bson.objectid import ObjectId

import json
import datetime

import os
from dotenv import load_dotenv

import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

load_dotenv()

DOMAIN = os.getenv('HOST')

editor_router = APIRouter(prefix="/editor", tags=["Редактор"])


def make_date_valid(date):
    if date is not None:
        if isinstance(date, str):
            if '-' in date:
                if 'T' in date:
                    try:
                        # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                        return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                    except:
                        # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                        # return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                        return datetime.datetime.strptime(date, '%Y-%m-%d')
                else:
                    try:
                        # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    except:
                        # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                        # return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                        return datetime.datetime.strptime(date, '%Y-%m-%d')
            elif '.' in date:
                try:
                    return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                    # return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                except:
                    # return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
                    return datetime.datetime.strptime(date, '%d.%m.%Y')
                    # return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

def get_type(value):
    tp = str(type(value)).split('\'')[1]
    if tp == "NoneType":
        tp = "str"
    return tp


class Editor:

    def __init__(self, id=None, art_id=None, section_id=None, session=None):
        self.id = id  # !!!проверить доступ!!!, а в будущем надо хранить изменения в таблице, чтобы знать, кто сколько чего публиковал, кто чего наредактировал
        self.session = session
        self.section_id = section_id
        self.art_id = art_id

        self.variable = {
            "active": [True, False],
            "content_type": ["HTML", "Markdown", None]
        }

        # словарь полей
        fields_data_file = open("./src/base/fields.json", "r")
        self.fields = json.load(fields_data_file)
        fields_data_file.close()

        self.fundamental = ["id, section_id", "name", "content_text", "content_type", "active", "date_publiction",
                            "date_creation", "preview_text"]
        self.notEditble = ["id", "section_id", "date_creation", "content_type", "author", "users"]
        self.pattern = None

    async def validate(self):
        if self.art_id is not None and self.section_id is None:

            art = await ArticleModel(id=int(self.art_id)).find_by_id(session=self.session)
            # art = asyncio.run(ArticleModel(id = self.art_id).find_by_id(session=self.session))

            if "section_id" in art:
                self.section_id = art["section_id"]

        if self.section_id in [14, 18, 41, 42, 52, 54, 111, 172, 56]:
            self.notEditble.append("preview_text")
        if self.section_id in [41, 42, 111, 52]:
            self.notEditble.append("content_text")

        # список шаблонов для каждого раздела
        pattern_data_file = open("./src/base/patterns.json", "r")
        pattern_data = json.load(pattern_data_file)

        if self.section_id is not None:
            for sec_pattern, value in pattern_data.items():
                if self.section_id == int(sec_pattern):
                    self.pattern = value
        else:
            self.pattern = None
        pattern_data_file.close()

    async def get_pattern(self):
        await self.validate()
        # и ошибка тут
        # список шаблонов для каждого раздела
        pattern_data_file = open("./src/base/patterns.json", "r")
        pattern_data = json.load(pattern_data_file)
        # if self.section_id is not None:
        #     for sec_pattern in pattern_data:
        #         if self.section_id in sec_pattern["section_id"].keys():
        #             self.pattern = sec_pattern
        # else:
        #     self.pattern = None
        if self.section_id is not None:
            for sec_pattern, value in pattern_data.items():
                if self.section_id == int(sec_pattern):
                    self.pattern = value
        else:
            self.pattern = None
        pattern_data_file.close()

        return self.pattern

    async def set_pattern(self, new_pattern):
        await self.validate()

        # получить текущие паттерны
        pattern_data_file = open("./src/base/patterns.json", "r")
        pattern_data = json.load(pattern_data_file)
        pattern_data_file.close()

        # заменить паттерн
        pattern_data[self.section_id] = new_pattern

        # сохранить в файле
        pattern_data_file = open("./src/base/patterns.json", "w")
        json.dump(pattern_data, pattern_data_file, indent=4)
        pattern_data_file.close()

        return pattern_data

    '''
    def get_fast_format(self ):
        #собрать поля статьи
        section = ArticleModel(section_id = self.section_id).find_by_section_id()

        fields = []
        files_keys = dict()
        #иду по всем статьям раздела
        for art in section:
            #иду по всем полям статьи
            for k in art.keys():
                values = []

                #если такого поля ещё нет
                fields_names = [f["field"] for f in fields]
                if k not in fields_names and k != "indirect_data" and k in self.fields.keys():

                    field = {
                        "name" : self.fields[k], #хватай имя
                        "field" : k, #хватай поле
                        "data_type" : get_type(art[k]) #хватай тип данных
                    }
                    fields.append(field)
                #если есть
                else:
                    #если тип не совпадает - вписать тот, который не None
                    for field in fields:
                        if field["data_type"] != get_type(art[k]):
                            if field["data_type"] == "NoneType":
                                field["data_type"] = get_type(art[k])
                            elif get_type(art[k]) != "NoneType":
                                field["data_type"] = "str"

                # вытащить поля из psql -> indirect_data
                if "indirect_data" in art and art["indirect_data"] is not None:
                    for k in art["indirect_data"].keys():
                        fields_names = [f["field"] for f in fields]

                        if k not in fields_names and k != "indirect_data" and k in self.fields.keys():
                            field = {
                                "name" : self.fields[k], #хватай имя
                                "field" : k, #хватай поле
                                "data_type" : get_type(art["indirect_data"][k]) #хватай тип данных
                            }
                            fields.append(field)
                        #если есть
                        else:
                            #если тип не совпадает - вписать тот, который не None
                            for field in fields:
                                if field["data_type"] != get_type(art["indirect_data"][k]):
                                    if field["data_type"] == "NoneType":
                                        field["data_type"] = get_type(art["indirect_data"][k])
                                    elif get_type(art["indirect_data"][k]) != "NoneType":
                                        field["data_type"] = "str"



            #теперь проверим какие файлы бывают у статей раздела
            self.art_id = int(art['id'])
            files=self.get_files()

            # беру ключи словаря
            for f_key in files.keys():
                # ЕСЛИ ключ ещё не записан в files_keys и там не пустой массив
                if f_key not in files_keys.keys() and files[f_key] != [] and files[f_key] is not None:
                    files_keys[f_key] = []


            #if "photo_file_url" in art.keys():
                # "Фотография (URL)",

        #пост обработка
        for field in fields:
            # если значения варьируются
            if field["field"] in self.variable.keys():
                field["values"] = self.variable[field["field"]]

            # если поле нередаактируемое
            if field["field"] in self.notEditble:
                    field["disabled"] = True

        need_del = False 
        indx = None
        del_key = ["photo_file_url", ""]
        del_val = []
        for i, field in enumerate(fields):
            #если есть uuid
            if field["field"] == "uuid" or field['field'] == "author_uuid" or "uuid" in field['field']:
                field["data_type"] = "search_by_uuid"
                #стереть возможность грузить photo_file_url и заполнить заранее по uuid
                need_del = True
            if field["field"] in del_key:
                del_val.append(i)

        if need_del:
            for i in del_val:
                fields.pop(i)

        return {"fields" : fields, "files" : files_keys}

    def get_format(self ):
        #собрать поля статьи
        section = ArticleModel(section_id = self.section_id).find_by_section_id()

        fields = []
        files_keys = dict()
        #иду по всем статьям раздела
        for art in section:
            #иду по всем полям статьи
            for k in art.keys():
                values = []

                #если такого поля ещё нет
                fields_names = [f["field"] for f in fields]
                if k not in fields_names and k != "indirect_data" and k in self.fields.keys():

                    field = {
                        "name" : self.fields[k], #хватай имя
                        "field" : k, #хватай поле
                        "data_type" : get_type(art[k]) #хватай тип данных
                    }
                    fields.append(field)
                #если есть
                else:
                    #если тип не совпадает - вписать тот, который не None
                    for field in fields:
                        if field["data_type"] != get_type(art[k]):
                            if field["data_type"] == "NoneType":
                                field["data_type"] = get_type(art[k])
                            elif get_type(art[k]) != "NoneType":
                                field["data_type"] = "str"

                # вытащить поля из psql -> indirect_data
                if "indirect_data" in art and art["indirect_data"] is not None:
                    for k in art["indirect_data"].keys():
                        fields_names = [f["field"] for f in fields]

                        if k not in fields_names and k != "indirect_data" and k in self.fields.keys():
                            field = {
                                "name" : self.fields[k], #хватай имя
                                "field" : k, #хватай поле
                                "data_type" : get_type(art["indirect_data"][k]) #хватай тип данных
                            }
                            fields.append(field)
                        #если есть
                        else:
                            #если тип не совпадает - вписать тот, который не None
                            for field in fields:
                                if field["data_type"] != get_type(art["indirect_data"][k]):
                                    if field["data_type"] == "NoneType":
                                        field["data_type"] = get_type(art["indirect_data"][k])
                                    elif get_type(art["indirect_data"][k]) != "NoneType":
                                        field["data_type"] = "str"




            #теперь проверим какие файлы бывают у статей раздела
            self.art_id = int(art['id'])
            files=self.get_files()

            # беру ключи словаря
            for f_key in files.keys():
                # ЕСЛИ ключ ещё не записан в files_keys и там не пустой массив
                if f_key not in files_keys.keys() and files[f_key] != [] and files[f_key] is not None:
                    files_keys[f_key] = []

            for field in fields:
                #if "photo_file_url" in art.keys():
                    # "Фотография (URL)",

                if field["field"] == "active":
                    field["value"] = False

                # если значения варьируются
                if field["field"] in self.variable.keys():
                    field["values"] = self.variable[field["field"]]

                # если поле нередактируемое
                if field["field"] in self.notEditble:
                    field["disabled"] = True

        need_del = False 
        indx = None
        del_key = ["photo_file_url", ""]
        del_val = []
        for i, field in enumerate(fields):
            #если есть uuid
            if field["field"] == "uuid" or field['field'] == "author_uuid" or "uuid" in field['field']:
                field["data_type"] = "search_by_uuid"
                #стереть возможность грузить photo_file_url и заполнить заранее по uuid
                need_del = True
            if field["field"] in del_key:
                del_val.append(i)

        if need_del:
            for i in del_val:
                fields.pop(i)



        return {"fields" : fields, "files" : files_keys}

    def get_sections(self ):
        all_sections = Section().get_all()
        valid_id = [13, 14, 15, 16, 18, 22, 31, 32, 34, 41, 42, 51, 52, 53, 54, 55, 56, 110, 111, 172, 175]
        edited_sections = []
        for sec in all_sections:
            if sec["id"] in valid_id:
                self.section_id = sec["id"]
                #Отдельно вручную укажу правильный шаблон для 56 Магазина Мерча
                if sec["id"] == 56:
                    Pattern = {
                        "fields": [
                            {
                                "name": "Размер s",
                                "field": "s",
                                "data_type": "int"
                            },
                            {
                                "name": "Размер m",
                                "field": "m",
                                "data_type": "int"
                            },
                            {
                                "name": "Размер l",
                                "field": "l",
                                "data_type": "int"
                            },
                            {
                                "name": "Размер xl",
                                "field": "xl",
                                "data_type": "int"
                            },
                            {
                                "name": "Размер xxl",
                                "field": "xxl",
                                "data_type": "int"
                            },
                            {
                                "name": "Безразмерный",
                                "field": "no_size",
                                "data_type": "int"
                            },
                            {
                                "name": "Цена",
                                "field": "price",
                                "data_type": "int"
                            },
                            {
                                "name": "ID",
                                "field": "id",
                                "data_type": "str"
                            },
                            {
                                "name": "Активна",
                                "field": "active",
                                "data_type": "str"
                            },
                            {
                                "name": "Содержимое",
                                "field": "content_text",
                                "data_type": "str"
                            },
                            {
                                "name": "Дата публикации",
                                "field": "date_publiction",
                                "data_type": "str"
                            },
                            {
                                "name": "Название статьи",
                                "field": "name",
                                "data_type": "str"
                            },
                            {
                                "name": "ID раздела",
                                "field": "section_id",
                                "data_type": "str"
                            },
                            {
                                "name": "Тип форматирования",
                                "field": "content_type",
                                "data_type": "str"
                            },
                            {
                                "name": "Дата создания",
                                "field": "date_creation",
                                "data_type": "str",
                                "disabled": True
                            },
                            {
                                "name": "Аннотация",
                                "field": "preview_text",
                                "data_type": "str",
                                "disabled": True
                            } 
                        ],
                        "files": {
                            "images": []
                        }
                    }

                # Шаблон собирается по скаченным из Интранета статьям
                else:
                    #Собрать шаблон
                    Pattern = self.get_format()

                #записать паттерн
                self.set_pattern(Pattern)

        pattern_data_file = open("./src/base/patterns.json", "r")
        pattern_data = json.load(pattern_data_file)
        pattern_data_file.close()
        return pattern_data
    '''

    async def section_rendering(self):
        await self.validate()
        result = await Article(section_id=self.section_id).all_serch_by_date(self.session)
        for art in result:
            self.id = art["id"]
            art["preview_file_url"] = await Article(id=int(self.id)).get_preview(self.session)
        return result

    async def rendering(self):
        await self.validate()
        if self.art_id is None:
            return LogsMaker().warning_message("Укажите id статьи")

        # вытащить основные поля из psql
        art = await Article(id=self.art_id).find_by_id(self.session)
        if self.section_id is None:
            if "section_id" in art:
                self.section_id = art["section_id"]
            else:
                return LogsMaker().warning_message("Неверный id статьи")

        art_keys = []
        for k in art.keys():
            if k not in art_keys and k != "indirect_data":
                art_keys.append(k)

        # вытащить поля из psql -> indirect_data
        if "indirect_data" in art and art["indirect_data"] is not None:
            for k in art["indirect_data"].keys():
                if k not in art_keys:
                    art_keys.append(k)

        # Протащить через словарь полей
        field = []
        for k in art_keys:
            if k in self.fields:

                # забираю занчение
                val = None
                if k in art:
                    val = art[k]
                elif k in art["indirect_data"]:
                    val = art["indirect_data"][k]

                data_type = get_type(val)
                # экземпляр поля
                fl = {
                    "name": self.fields[k],
                    "value": val,
                    "field": k,
                    "data_type": data_type
                }

                # если значения варьируются
                if k in self.variable.keys():
                    fl["values"] = self.variable[k]

                # проверяю редактируемость
                if k in self.notEditble:
                    fl["disabled"] = True

                # загрузил
                field.append(fl)

        got_fields = field

        # photo_file_url нужен только там, где он есть
        # for f, i in enumerate(field):
        #     if field["field"] == "photo_file_url" and field["value"] is None:
        #         field.pop(i)

        # заполнить поля по шаблону
        result_fields = []
        curr_patterns = await self.get_pattern()
        for need_field in curr_patterns["fields"]:
            has_added = False
            for got_field in got_fields:

                # если такое поле есть среди заполненных
                if need_field["field"] == got_field["field"]:

                    # отдельно проверить валидность типа
                    if need_field["data_type"] != got_field["data_type"]:
                        got_field["data_type"] = need_field["data_type"]

                        # отдельно проверить валидность вариантов выбора значения
                    if "values" in need_field:
                        if "values" not in got_field or need_field["values"] != got_field["values"]:
                            got_field["values"] = need_field["values"]

                    # вписываем
                    result_fields.append(got_field)
                    has_added = True

            # если среди заполненных нет - вписать из шаблона
            if not has_added:
                if need_field["field"] == "all_tags":
                    # получаешь список ВСЕХ доступных тэгов
                    tags_list = await Tag().get_all_tags(self.session)
                    sorted_tags = sorted(tags_list, key=lambda x: x.tag_name, reverse=False)
                    # записываешь в need_field["values"] и в need_field["values"]
                    need_field["values"] = sorted_tags

                if need_field["field"] == "tags":
                    need_field["values"] = await Tag(art_id=self.art_id).get_art_tags(self.session)
                    # need_field.pop("value")

                result_fields.append(need_field)

        # вытащить файлы
        self.art_id = int(self.art_id)
        files = await self.get_files()

        '''
        need_del = []
        for f in got_files.keys():
            if got_files[f] == []:
                need_del.append(f)
        for f in need_del:
            got_files.pop(f)

        #заполнить файлы по шаблону
        for need_files in self.get_pattern()["files"].keys():
            #если есть файлы
            if got_files.get(need_files) is not None:
                #вписываем
        '''

        need_del = []
        for f in files.keys():
            curr_pattern = await self.get_pattern()
            if files[f] == [] and curr_pattern["files"].get(f) is None:
                need_del.append(f)
        for f in need_del:
            files.pop(f)

        # вывести
        return {"fields": result_fields, "files": files}

    async def pre_add(self, ):
        await self.validate()
        # Получаю поля паттерна
        fields = self.pattern["fields"]

        # пост обработка и создание пустой болванки
        for field in fields:

            # если это ID статьи
            if field["field"] == "id":
                # отдельно засылаю будущий уже инкрементированнный ID статьи
                self.art_id = await ArticleModel().get_current_id(self.session)
                field["value"] = self.art_id

                # создать пустую неактивную статью с этим ID
                art = dict()

                # вписываю значения нередактируемых параметров сам:
                art["id"] = self.art_id
                art["active"] = False
                art["section_id"] = self.section_id
                art["date_creation"] = make_date_valid(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))

                # добавить статью
                await Article().set_new(art, self.session)
                LogsMaker().ready_status_message(f"Создал {self.art_id}")

            elif field["field"] == "all_tags":
                # получаешь список ВСЕХ доступных тэгов
                tags_list = await Tag().get_all_tags(self.session)
                sorted_tags = sorted(tags_list, key=lambda x: x.tag_name, reverse=False)
                # записываешь в need_field["values"] и в need_field["values"]
                field["values"] = sorted_tags

        # Вношу изменеения
        self.pattern["fields"] = fields

        return self.pattern

    async def add(self, data: dict):
        await self.validate()
        # self.art_id = int(data["id"])
        if self.art_id is None:
            return LogsMaker.warning_message("Укажите id раздела")

        art = await Article(id=self.art_id).find_by_id(self.session)
        if '_sa_instance_state' in art:
            art.pop('_sa_instance_state')
        indirect_data = dict()
        # валидировать данные data
        for key in data.keys():

            # если это редактируемый параметр
            if key not in self.notEditble:
                # если это один из основных параметров
                if key in self.fundamental:
                    # фиксирую
                    art[key] = data[key]

                    # если это часть indirect_data
                else:
                    # отдельно проверяю дату начала для афиши
                    # if "date_from" == key and data[key] is not None:
                    #     indirect_data[key] = make_date_valid(data[key])
                    
                    # # отдельно проверяю дату конца для афиши
                    # elif "date_to" == key and data[key] is not None:
                    #     indirect_data[key] = make_date_valid(data[key])
                    
                    # else:
                    indirect_data[key] = data[key]

            # найти человека по uuid
            if key == "uuid" or key == "author_uuid":
                uuid = int(data[key])
                
                # поиск по uuid
                usr_dt = await User(uuid).search_by_id(self.session)
                photo = usr_dt["personal_photo"]
                indirect_data["photo_file_url"] = photo

            if key == "tags":
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # ОТДЕЛЬНЫМ МЕТОДОМ ДОБАВИТЬ ВЫБРАННЫЕ ТЕГИ К ЭТОЙ СТАТЬЕ на подобии get_users_info
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # вытащить список выбранных тегов
                tags_id = data[key]
                # заменить старое значение новым
                indirect_data["tags"] = tags_id

        art["indirect_data"] = indirect_data

        # отдельно проверяю дату публикации
        if "date_publiction" in art and art["date_publiction"] is not None:
            art["date_publiction"] = make_date_valid(art["date_publiction"])
        
        

        # отдельно перевожу стоку в булевое значение для active
        if type(art["active"]) == type(str()):
            art["active"] = True if (art["active"] == 'true' or art["active"] == 'True') else False

        if "content_type" in data:
            art["content_type"] = data["content_type"]
        else:
            art["content_type"] = None
        
        # вставить данные в статью
        res = await Article(id=self.art_id).update(art, self.session)
        return res

    async def delete_art(self):
        await self.validate()
        res = await Article(id=self.art_id).delete(self.session)
        return res

    async def update(self, data: dict):
        # print(data)

        from ..base.Elastic.ArticleSearchModel import ArticleSearchModel
        await self.validate()
        if self.art_id is None:
            return LogsMaker.warning_message("Укажите id статьи")

        # получаю текущие значения
        # вытащить основные поля из psql
        art = await ArticleModel(id=self.art_id).find_by_id(self.session)
        if "_sa_instance_state" in art:
            art.pop("_sa_instance_state")
        # вытаскию новые значения
        # валидировать данные data
        for key in data.keys():
            # если это редактируемый параметр
            if key not in self.notEditble:
                # если это один из основных параметрова
                if key in self.fundamental:
                    if key == 'date_publiction':
                        art[key] = make_date_valid(data[key])
                    else:
                        # фиксирую
                        art[key] = data[key]

                        # отправляю данные в elastic
                        if key == 'active':
                            if data['active'] is True:
                                art_data = data.copy()
                                await ArticleSearchModel().update_art_el_index(article_data=art_data,
                                                                               session=self.session,
                                                                               section_id=art_data['section_id'])

                            else:
                                await ArticleSearchModel().delete_art_from_el_index(art_id=self.art_id)



                # если это часть indirect_data
                else:
                    if "indirect_data" in art and art["indirect_data"] is not None:
                        if key == "tags":
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # ОТДЕЛЬНЫМ МЕТОДОМ ДОБАВИТЬ ВЫБРАННЫЕ ТЕГИ К ЭТОЙ СТАТЬЕ на подобии get_users_info
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                            tags_id = data["tags"]
                            # заменить старое значение новым
                            art["indirect_data"]["tags"] = tags_id
                        
                        #СЮДА ПОТОМ ЗАСУНУТЬ ФУНКЦИЮ ДЛЯ ОТПРАВКИ ПОЛЬЗОВАТЕЛЮ БАЛЛОВ ЗА НОВОСТЬ
                        # elif key == 'author_uuid':
                        #     print(data[key])
                        art["indirect_data"][key] = data[key]

        # перезаписать файлы
        # сохранить
        res = await ArticleModel(id=self.art_id).update(art, self.session)
        return res

    async def get_files(self):
        await self.validate()
        # file_data = await FileModel(art_id=self.art_id).find_all_by_art_id(self.session)
        file_data = await FilesDBModel(article_id=self.art_id).find_all_by_art_id(self.session)
        file_list = []
        for file in file_data:
            file_info = {}
            file_info["id"] = str(file["id"])
            file_info["original_name"] = file["original_name"]
            file_info["stored_name"] = file["stored_name"]
            file_info["content_type"] = file["content_type"]

            # файлы делятся по категориям
            if "image" in file["content_type"]:
                url = file["file_url"]
                file_info["type"] = "image"
                file_info["file_url"] = f"{DOMAIN}{url}"
            elif "video" in file["content_type"]:
                url = file["file_url"]
                file_info["file_url"] = f"{DOMAIN}{url}"
                file_info["type"] = "video"
            elif "link" in file["content_type"]:
                file_info["file_url"] = file["file_url"]
                file_info["type"] = "video_embed"
            else:
                url = file["file_url"]
                file_info["file_url"] = f"{DOMAIN}{url}"
                file_info["type"] = "documentation"

            file_info["article_id"] = file["article_id"]
            file_info["b24_url"] = file["b24_url"]

            print(file_info["file_url"] )

            file_info["active"] = file["active"]
            file_info["is_preview"] = file["is_preview"]

            file_list.append(file_info)

        # разбить по категориям
        result = dict()
        result['images'] = []
        result['videos_native'] = []
        result['videos_embed'] = []
        result['documentation'] = []

        for file in file_list:
            # файлы делятся по категориям
            if "image" in file["content_type"] or "jpg" in file["original_name"] or "jpeg" in file[
                "original_name"] or "png" in file["original_name"]:
                url = file["file_url"]
                result['images'].append(file)
            elif "video" in file["content_type"]:
                url = file["file_url"]
                result['videos_native'].append(file)
            elif "link" in file["content_type"]:
                result['videos_embed'].append(file)
            else:
                result['documentation'].append(file)
        sorted_images = sorted(result['images'], key=lambda x: int(x['id']), reverse=False)
        result['images'] = sorted_images
        return result

    async def get_sections_list(self):
        await self.validate()
        all_sections = await Section().get_all()

        pattern_data_file = open("./src/base/patterns.json", "r")
        pattern_data = json.load(pattern_data_file)
        pattern_data_file.close()

        valid_sec_id = list(pattern_data.keys())
        valid_sec_id = [int(item) for item in valid_sec_id]

        # valid_sec_id = [13, 14, 15, 16, 18, 110, 111, 172, 175, 22, 31, 32, 34, 41, 42, 51, 52, 53, 54, 55, 56, 7, 71]
        edited_sections = []
        for sec in all_sections:
            if sec["id"] in valid_sec_id:
                edited_sections.append(sec)
        return edited_sections

    async def get_users_info(self, user_id_list):
        await self.validate()
        art = await Article(id=int(self.art_id)).find_by_id(self.session)

        if user_id_list == []:
            art['indirect_data']['users'] = []
        else:
            # иду по списку user_id
            for user_id in user_id_list:
                user_info = await User(id=user_id).search_by_id(self.session)

                if art['indirect_data'] is None:
                    art['indirect_data'] = {"users": []}

                if 'users' not in art['indirect_data']:
                    art['indirect_data']['users'] = []

                users = art['indirect_data']['users']

                if users != []:
                    # проверяю есть ли такой в списке статьи
                    had_find = False

                    for user in users:
                        if int(user["id"]) == int(user_id):
                            had_find = True

                        # если есть в стаье, но нет в user_id_list
                        elif int(user["id"]) not in user_id_list:
                            # выписываю
                            art['indirect_data']['users'].remove(user)

                    # если ещё нет
                    if not had_find:

                        # хватаю ФИО
                        if "last_name" in user_info:
                            last_name = user_info['last_name']
                        else:
                            last_name = ""
                        if "name" in user_info:
                            name = user_info['name']
                        else:
                            name = ""
                        if "second_name" in user_info:
                            second_name = user_info['second_name']
                        else:
                            second_name = ""

                        fio = last_name + " " + user_info['name'] + " " + user_info['second_name']

                        # фото
                        if "photo_file_url" in user_info:
                            photo_file_url = user_info["photo_file_url"]
                        else:
                            photo_file_url = "https://portal.emk.ru/local/templates/intranet/img/no-user-photo.png"

                        # взять должность
                        if "work_position" in user_info:
                            position = user_info["work_position"]
                        else:
                            position = ""

                        usr = {
                            "id": user_id,
                            "fio": fio,
                            "photo_file_url": photo_file_url,
                            "position": position
                        }

                        # записываю
                        art['indirect_data']['users'].append(usr)
                else:
                    # хватаю ФИО
                    if "last_name" in user_info:
                        last_name = user_info['last_name']
                    else:
                        last_name = ""
                    if "name" in user_info:
                        name = user_info['name']
                    else:
                        name = ""
                    if "second_name" in user_info:
                        second_name = user_info['second_name']
                    else:
                        second_name = ""

                    fio = last_name + " " + user_info['name'] + " " + user_info['second_name']

                    # фото
                    if "photo_file_url" in user_info:
                        photo_file_url = user_info["photo_file_url"]
                    else:
                        photo_file_url = "https://portal.emk.ru/local/templates/intranet/img/no-user-photo.png"

                    # взять должность
                    if "work_position" in user_info:
                        position = user_info["work_position"]
                    else:
                        position = ""

                    usr = {
                        "id": user_id,
                        "fio": fio,
                        "photo_file_url": photo_file_url,
                        "position": position
                    }

                    # записываю
                    art['indirect_data']['users'] = [usr]

        # print(art['indirect_data'])

        # сохранил
        await Article(id=self.art_id).update(art, self.session)

        return art['indirect_data']['users']

    async def get_user_info(self, user_id):
        await self.validate()
        result = {}
        fields_to_return = {
            "14": [
                "name",
                "second_name",
                "last_name",
                "work_position",
                "department",
                "photo_file_url"
            ],
            "15": [
                "id",
                "name",
                "second_name",
                "last_name",
                "work_position",
                "photo_file_url"
            ],
            "31": [
                "id",
                "name",
                "second_name",
                "last_name",
                "work_position",
                "department",
                "photo_file_url"
            ],
            "172": [
                "name",
                "second_name",
                "last_name",
                "work_position",
                "photo_file_url"
            ],
            "71": [
                "name",
                "second_name",
                "last_name",
                "work_position",
                "department"
            ]
        }
        if user_id == 0:
            art = await Article(id=int(self.art_id)).find_by_id(self.session)
            art_fields = fields_to_return[str(art['section_id'])]
            if art['section_id'] == 31:
                art['indirect_data'].pop('author')
                # сохранил
                await Article(id=self.art_id).update(art, self.session)
                return []
            for art_field in art_fields:
                art['indirect_data'].pop(art_field)
            await Article(id=self.art_id).update(art, self.session)
            return []
        # user_id = int(user_id)
        user_info = await User(id=user_id).search_by_id(self.session)
        if str(self.section_id) in fields_to_return.keys():
            fields = fields_to_return[str(self.section_id)]
            for field in fields:
                if field == "work_position" and field in user_info['indirect_data'].keys():
                    result['position'] = user_info['indirect_data'][field]
                elif field == "department":
                    result[field] = user_info['indirect_data']['uf_department']
                elif field == "photo_file_url":
                    if "photo_file_url" not in user_info or user_info["photo_file_url"] == None:
                        photo_replace = "https://portal.emk.ru/local/templates/intranet/img/no-user-photo.png"
                    else:
                        photo = user_info["photo_file_url"]
                        photo_replace = photo.replace("user_files", "compress_image/user")
                    photo_file_url = photo_replace
                    result[field] = photo_file_url
                elif field == "id":
                    result["author_uuid"] = user_id
                else:
                    if field in user_info:
                        result[field] = user_info[field]
                    elif field in user_info['indirect_data']:
                        result[field] = user_info['indirect_data'][field]
                    else:
                        result[field] = ""

        result['user_id'] = user_id

        if "name" in result.keys():
            result['fio'] = result['last_name'] + " " + result['name'] + " " + result['second_name']
            result.pop('name')
            result.pop('second_name')
            result.pop('last_name')

        if "department" in result.keys() and type(result["department"]) == type(list()):
            res_dep = result["department"][0]
            if len(result["department"]) > 1:
                for dep_i in range(0, len(result["department"])):
                    res_dep = res_dep + ", " + result["department"][dep_i]
            result["department"] = res_dep

        # получаю статью
        art = await Article(id=self.art_id).find_by_id(self.session)

        if self.section_id == 14:
            art["name"] = result["fio"]

        if self.section_id == 15:
            result["author"] = result["fio"] + "; " + result['position']
            result["TITLE"] = result["fio"]
            result.pop("fio")
            result.pop('position')

        if self.section_id == 71:
            result["representative_text"] = result["fio"] + ", " + result['position'] + ", " + result["department"]
            result.pop("fio")
            result.pop("department")
            result.pop('position')

        

        # вписываю в неё эти значения
        for key in result.keys():
            if art['indirect_data'] is None:
                art['indirect_data'] = dict()
            art['indirect_data'][key] = result[key]

        if self.section_id == 31:
            art['indirect_data']['author'] = {
                'id': user_id,
                'fio': result["fio"],
                'position': result["position"],
                'photo_file_url': result["photo_file_url"]
            }

        #Отправляем баллы пользователю на 31 раздел
        if self.section_id == 31:
            from .Peer import Peer
            await Peer().send_points_to_article_author(session=self.session, article_id=self.art_id, author_id=user_id)

        # сохранил
        await Article(id=self.art_id).update(art, self.session)

        return result


async def get_uuid_from_request(request, session):
    # from .Auth import AuthService
    user_id = None
    token = request.cookies.get("user_id")
    if token is None:
        token = request.headers.get("user_id")
        if token is not None:
            user_id = token
    else:
        user_id = token

    if user_id is not None:

        # получить и вывести его id
        usr = User()
        usr.id = int(user_id)
        user_inf = await usr.search_by_id(session=session)
        if user_inf is not None and "id" in user_inf.keys():
            return user_inf["id"]
    return None


async def get_editor_roots(user_uuid, session):
    from ..base.pSQL.objects.RootsModel import RootsModel
    roots_model = RootsModel()
    roots_model.user_uuid = user_uuid
    all_roots = await roots_model.get_token_by_uuid(session)
    editor_roots = await roots_model.token_processing_for_editor(all_roots)
    # print('ПИШЕМ УСЛОВИЕ ДЛЯ ИГОРЯ В EDITOR', user_uuid)

    if user_uuid is None:
        print('ФОРМИРУЕМ ЕМУ СЛОВАРЬ КОГСТЫЛЬ')
        editor_roots = {'PeerAdmin': True, 'EditorAdmin': True, 'VisionAdmin': True, 'GPT_gen_access': True}
        # editor_roots = {}
        print(editor_roots, 'ФОРМИРУЕМ ЕМУ СЛОВАРЬ КОГСТЫЛЬ')
    # 'PeerAdmin': True, 'PeerModer': True, 'PeerCurator': [], 
    return editor_roots


@editor_router.get("/get_user_info/{section_id}/{art_id}/{user_id}")
async def set_user_info(section_id: int, art_id: int, user_id, session: AsyncSession = Depends(get_async_db)):
    return await Editor(art_id=art_id, section_id=section_id, session=session).get_user_info(user_id)


@editor_router.post("/get_users_info")
async def set_user_info(session: AsyncSession = Depends(get_async_db), data=Body()):
    if "art_id" in data:
        art_id = data["art_id"]
    else:
        return "\'art_id\' is not found"
    if "users_id" in data:
        users_id = data["users_id"]
    else:
        return "\'users_id\' is not found"

    return await Editor(art_id=art_id, session=session).get_users_info(user_id_list=users_id)


# получить паттерн
@editor_router.get("/pattern/{section_id}")
async def get_pattern_by_sec_id(section_id: int):
    return Editor(section_id=section_id).get_pattern()


# заменить/создать паттерн
@editor_router.post("/pattern")
async def get_pattern_by_sec_id(data=Body()):
    section_id = int(data["section_id"])
    data.pop("section_id")
    return Editor(section_id=section_id).get_pattern(data)


'''
#автосборка паттернов
@editor_router.get("/edit_sections")
async def get_edit_sections():
    return Editor().get_sections()
'''


# вывод списка редактируемых секций
@editor_router.get("/get_sections_list")
async def get_sections_list(request: Request, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    # user_uuid = 261
    editor_roots = await get_editor_roots(user_uuid, session)
    # editor_roots = {'user_id': 2366, 'EditorAdmin': False, 'EditorModer': []}
    print(editor_roots, 'мои права')
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        print('я одмин')
        return await Editor(session=session).get_sections_list()
    elif "EditorModer" in editor_roots.keys() and editor_roots["EditorModer"] != []:
        print('я не одмин')
        sections = await Editor(session=session).get_sections_list()
        result = [section for section in sections if section['id'] in editor_roots["EditorModer"]]
        return result
    return LogsMaker().warning_message(f"Недостаточно прав")


# рендеринг статьи
@editor_router.get("/rendering/{art_id}")
async def render(art_id: int, session: AsyncSession = Depends(get_async_db)):
    return await Editor(art_id=art_id, session=session).rendering()


# рендеринг статей по раздела
@editor_router.get("/section_rendering/{sec_id}")
async def sec_render(request: Request, sec_id: int, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    # user_uuid = 2366
    editor_roots = await get_editor_roots(user_uuid, session)
    # editor_roots = {'user_id': 2366, 'EditorAdmin': False, 'EditorModer': []}

    if ("EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True) or (
            "EditorModer" in editor_roots.keys() and sec_id in editor_roots["EditorModer"]):
        return await Editor(section_id=sec_id, session=session).section_rendering()
    return LogsMaker().warning_message(f"Недостаточно прав")


# изменить статью
@editor_router.post("/update/{art_id}")
async def updt(art_id: int, session: AsyncSession = Depends(get_async_db), data=Body()):
    # from ..base.Elastic.ArticleSearchModel import ArticleSearchModel
    # await ArticleSearchModel().update_art_el_index(article_data=data, session=session)
    return await Editor(art_id=art_id, session=session).update(data)


# добавить статью
@editor_router.get("/add/{section_id}")
async def get_form(section_id: int, session: AsyncSession = Depends(get_async_db)):
    return await Editor(section_id=section_id, session=session).pre_add()


@editor_router.post("/add/{art_id}")
async def set_new(art_id: int, session: AsyncSession = Depends(get_async_db), data=Body()):
    # section_id = data["section_id"]
    from ..base.Elastic.ArticleSearchModel import ArticleSearchModel
    await ArticleSearchModel().update_art_el_index(article_data=data, session=session)

    return await Editor(art_id=art_id, session=session).add(data)


@editor_router.delete("/del/{art_id}")
async def del_art(art_id: int, session: AsyncSession = Depends(get_async_db)):
    from ..base.Elastic.ArticleSearchModel import ArticleSearchModel
    await ArticleSearchModel().delete_art_from_el_index(art_id=art_id)
    return await Editor(art_id=int(art_id), session=session).delete_art()


# посмотреть все файлы статьи
@editor_router.get("/rendering/files/{art_id}")
async def render(art_id: int):
    return await Editor(art_id=art_id).get_files()


# @editor_router.post("/set_link")
# async def new_link(data=Body(), session: AsyncSession = Depends(get_async_db)):
#     art_id = data["art_id"]
#     file_id = 
#     return 





### тестирую работу с файлами
@editor_router.post("/upload_file/{art_id}")
async def create_file(file: UploadFile, art_id: int,
                      session: AsyncSession = Depends(get_async_db)):  # нельзя асинхронить
    # Здесь нужно сохранить файл или обработать его содержимое
    f_inf = await storeFile(art_id=int(art_id)).editor_add_file(session=session, file=file)
    return f_inf


@editor_router.delete('/delete_file/{file_id}')
async def del_file(file_id: str, session: AsyncSession = Depends(get_async_db)):
    return await storeFile(id=file_id).editor_del_file(session=session)


@editor_router.post("/upload_files/{art_id}")
async def create_upload_files(request: Request, art_id, files: List[UploadFile] = File(...), session: AsyncSession = Depends(get_async_db)):
    try:
        # headers_from = request.headers
        # Обработка каждого файла
        file_infos = []
        for file in files:
            # Здесь можно сохранить файл или обработать его содержимое
            f_inf = await storeFile(art_id=art_id).editor_add_file(file=file, session=session)
            file_infos.append(f_inf)
        return file_infos

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
