from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse

from src.services.LogsMaker import LogsMaker
from src.base.pSQLmodels import ArticleModel
from src.base.SearchModel import ArticleSearchModel
from src.base.mongodb import FileModel
from src.model.Article import Article
from src.model.File import File

import json

editor_router = APIRouter(prefix="/editor", tags=["Редактор"])

class Editor:
    
    def __init__(self, id=None, art_id=None, section_id=None):
        self.id = id #!!!проверить доступ!!!, а в будущем надо хранить изменения в таблице, чтобы знать, кто сколько чего публиковал, кто чего наредактировал
        self.art_id = art_id
        self.section_id = section_id

        #словарь полей
        fields_data_file = open("./src/base/fields.json", "r")
        self.fields = json.load(fields_data_file)
        fields_data_file.close()
    
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
                
                data_type = str(type(val)).split('\'')[1]

                # экземпляр поля
                fl = {
                    "name" : self.fields[k],
                    "value" : val,
                    "field" : k,
                    "data_type" : data_type
                }

                # проверяю редактируемость
                notEditble = ["id", "section_id", "date_creation"]
                if k in notEditble or val is None:
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
        art_keys = []
        for art in section:
            for k in art.keys():
                if k not in art_keys and k != "indirect_data":
                    art_keys.append(k)

            # вытащить поля из psql -> indirect_data
            if "indirect_data" in art:
                for k in art["indirect_data"].keys():
                    if k not in art_keys:
                        art_keys.append(k)
        
        for k in art_keys:
            if k in self.fields:
            

        return art_keys

    def add(self, data : dict):
        if self.section_id is None:
            return LogsMaker.warning_message("Укажите id раздела")
        
        #валидировать данные data
        #добавить статью
    


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
                file_infofile_info["type"] = "video_embed"
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
@editor_router.get("/rendering/{art_id}")
async def render(art_id ):
    return Editor(art_id=art_id).rendering()

#изменить статью
@editor_router.put("/update/{art_id}")
async def updt(art_id ):
    return Editor(art_id=art_id).update()

#добавить статью
@editor_router.get("/add/{section_id}")
async def get_form(section_id : int):
    return Editor(section_id=section_id).get_format()

@editor_router.post("/add")
async def set_new(data = Body()):
    return await Editor().add(data())



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
    return await Editor().add(data())