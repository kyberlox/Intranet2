from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse

from src.services.LogsMaker import LogsMaker
from src.base.pSQLmodels import ArticleModel
from src.base.SearchModel import ArticleSearchModel
from src.base.mongodb import FileModel
from src.model.Article import Article
from src.model.Section import Section
from src.model.File import File

import json
import datetime

editor_router = APIRouter(prefix="/editor", tags=["Редактор"])

def make_date_valid(date):
    if date is not None:
        try:
            return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        except:
            return datetime.datetime.strptime(date, '%d.%m.%Y')
    else:
        return None

def get_type(value):
    return str(type(value)).split('\'')[1]

class Editor:
    
    def __init__(self, id=None, art_id=None, section_id=None):
        self.id = id #!!!проверить доступ!!!, а в будущем надо хранить изменения в таблице, чтобы знать, кто сколько чего публиковал, кто чего наредактировал
        self.art_id = art_id
        self.section_id = section_id

        self.fundamental = ["id, section_id", "name", "content_text", "content_type", "active", "date_publiction", "date_creation", "preview_text"]

        self.notEditble = ["id", "section_id", "date_creation", "content_type"]

        self.variable = {
            "active" : [True, False],
            "content_type" : ["HTML", "Markdown", None]
        }

        #словарь полей
        fields_data_file = open("./src/base/fields.json", "r")
        self.fields = json.load(fields_data_file)
        fields_data_file.close()
    
    def get_sections(self):
        all_sections = Section().get_all()
        valid_id = [13, 14, 15, 16, 172, 175, 18, 110, 111, 31, 32, 34, 41, 42, 51, 52, 53, 54, 55]
        edited_sections = []
        for sec in all_sections:
            if sec["id"] in valid_id:
                edited_sections.append(sec)
        return edited_sections

    
    def rendering(self ):
        if self.art_id is None:
            return LogsMaker.warning_message("Укажите id статьи")
        
        # вытащить основные поля из psql
        art = ArticleModel(id = self.art_id).find_by_id()

        art_keys = []
        for k in art.keys():
            if k not in art_keys and k != "indirect_data":
                art_keys.append(k)

        # вытащить поля из psql -> indirect_data
        if "indirect_data" in art:
            for k in art["indirect_data"].keys():
                if k not in art_keys:
                    art_keys.append(k)

        # протащить через словарь полей
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
                    "name" : self.fields[k],
                    "value" : val,
                    "field" : k,
                    "data_type" : data_type
                }

                # проверяю редактируемость
                if k in self.notEditble or val is None:
                    fl["disabled"] = True

                #загрузил
                field.append(fl)

        # вытащить файлы
        self.art_id = int(self.art_id)
        files=self.get_files()
        
        # вывести
        return {"fields" : field, "files" : files}
    
    
    def get_format(self ):
        #собрать поля статьи
        section = ArticleModel(section_id = self.section_id).find_by_section_id()
        
        fields = []
        files_keys = []
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
                if "indirect_data" in art:
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
                if f_key not in files_keys and files[f_key] != []:
                    files_keys.append(f_key)
            
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

        return {"fields" : fields, "files" : files_keys}

    def add(self, data : dict):
        self.section_id = int(data["section_id"])
        if self.section_id is None:
            return LogsMaker.warning_message("Укажите id раздела")

        art = dict()
        indirect_data = dict()
        #валидировать данные data
        for key in data.keys():
            #если это редактируемый параметр
            if key not in self.notEditble:
                #если это один из основных параметров
                if key in self.fundamental:
                    #фиксирую
                    art[key] = data[key]    

                #если это часть indirect_data
                else:
                    indirect_data[key] = data[key]  

        art["indirect_data"] = indirect_data

        #отдельно проверяю дату публикации
        if "date_publiction" in art and art["date_publiction"] is not None:
            art["date_publiction"] = make_date_valid(art["date_publiction"])

        #отдельно перевожу стоку в билевое значение для active
        if type(art["active"]) == type(str()):
            art["active"] = True if (art["active"] == 'true' or art["active"] == 'True') else False

            

        #вписываю значения нередактируемы параметров сам:
        art["section_id"] = self.section_id
        art["date_creation"] = make_date_valid(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
        if "content_type" in data:
            art["content_type"] = data["content_type"]
        else:
            art["content_type"] = None

        #добавить файлы к статье

        #добавить статью
        return Article().set_new(art)

    def delete_art(self, ):
        return Article(id = self.art_id).delete()
        



    def update(self ):
        if self.art_id is None:
            return LogsMaker.warning_message("Укажите id статьи")
        # перезаписать основные поля из psql

        # перезаписать поля из psql -> idirect_data
        # перезаписать файлы 
        # сохранить

    def get_files(self ):
        file_data = FileModel(art_id=self.art_id).find_all_by_art_id()
        file_list = []
        for file in file_data:
            file_info = {}
            file_info["id"] = str(file["_id"])
            file_info["original_name"] = file["original_name"]
            file_info["stored_name"] = file["stored_name"]
            file_info["content_type"] = file["content_type"]

            #файлы делятся по категориям
            if "image" in file["content_type"]:
                file_info["type"] = "image"
            elif "video" in file["content_type"]:
                file_info["type"] = "video"
            elif "link" in file["content_type"]:
                file_info["type"] = "video_embed"
            else:
                file_info["type"] = "documentation"

            file_info["article_id"] = file["article_id"]
            file_info["b24_id"] = file["b24_id"]
            url = file["file_url"]
            #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!
            file_info["file_url"] = f"http://intranet.emk.org.ru{url}"
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            file_info["is_archive"] = file["is_archive"]
            file_info["is_preview"] = file["is_preview"]

            file_list.append(file_info)

        #разбить по категориям
        result = dict()
        result['images'] = []
        result['videos_native'] = []
        result['videos_embed'] = []
        result['documentation'] = []
        
        for file in file_list:
            #файлы делятся по категориям
            if "image" in file["content_type"] or "jpg" in file["original_name"] or "jpeg" in file["original_name"] or "png" in file["original_name"]:
                url = file["file_url"]
                result['images'].append(file)
            elif "video" in file["content_type"]:
                url = file["file_url"]
                result['videos_native'].append(file)
            elif "link" in file["content_type"]:
                result['videos_embed'].append(file)
            else:
                result['documentation'].append(file)

        return result

    
    def change_file(self, file_id):
        pass
    
    def delete_file(self, file_id):
        pass



#рендеринг статьи
@editor_router.get("/edit_sections/")
async def get_edit_sections():
    return Editor().get_sections()

@editor_router.get("/rendering/{art_id}")
async def render(art_id : int ):
    return Editor(art_id=art_id).rendering()

#изменить статью
@editor_router.put("/update/{art_id}")
async def updt(art_id : int):
    return Editor(art_id=art_id).update()

#добавить статью
@editor_router.get("/add/{section_id}")
async def get_form(section_id : int):
    return Editor(section_id=section_id).get_format()

@editor_router.post("/add")
async def set_new(data = Body()):
    return Editor().add(data)

@editor_router.delete("/del/{art_id}")
async def del_art(art_id : int):
    return Editor(art_id=int(art_id)).delete_art()



#посмотреть все файлы статьи
@editor_router.get("/rendering/files/{art_id}")
async def render(art_id : int):
    return Editor(art_id=art_id).get_files()

#заменить файл
@editor_router.put("/update/file/{art_id}/{f_id}")
async def updt(art_id ):
    return await Editor(art_id=art_id).update()

#добавить файл в статью
@editor_router.post("/add/file/{art_id}/{f_id}")
async def set_new(data = Body()):
    return await Editor().add(data)