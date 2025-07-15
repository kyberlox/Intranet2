from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.services.LogsMaker import LogsMaker
from src.base.pSQLmodels import ArticleModel
from src.base.SearchModel import ArticleSearchModel
from src.base.mongodb import FileModel
from src.model.Article import Article
from src.model.File import File

import json

editor_router = APIRouter(prefix="/editor", tags=["Редактор"])

class Editor:
    #тут можно объявить классы лоя работы со статьями и файлами
    ArticleModel = ArticleModel()
    File = File()
    LogsMaker = LogsMaker()
    
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
        ArticleModel.id = self.art_id
        art = ArticleModel.find_by_id()
        keys = []
        for k in art.keys():
            if k not in keys and k != "indirect_data":
                keys.append(k)
        # вытащить поля из psql -> indirect_data
        if "indirect_data" in art:
            for k in art["indirect_data"].keys():
                if k not in keys:
                    keys.append(k)
        # протащить через словарь полей
        # вытащить файлы 
        # вывести
        return keys
    
    def add(self, data : dict):
        if self.section_id is None:
            return LogsMaker.warning_message("Укажите id раздела")
        #собрать поля статей раздела
        #валидировать данные data
        #добавить статью
    
    def update(self ):
        if self.art_id is None:
            return LogsMaker.warning_message("Укажите id статьи")
        # перезаписать основные поля из psql
        # перезаписать поля из psql -> idirect_data
        # перезаписать файлы 
        # сохранить

    def delete_file(self, file_id):
        pass
    
    def delete_file(self, file_id):
        pass
    
    def delete_file(self, file_id):
        pass



#рендеринг статьи
@editor_router.get("/rendering/{art_id}")
async def render(art_id ):
    return await Editor(art_id=art_id).rendering()

#изменить статью
@editor_router.put("/update/{art_id}")
async def updt(art_id ):
    return await Editor(art_id=art_id).update()

#добавить статью
@editor_router.post("/add")
async def set_new(data = Body()):
    return await Editor().add(data())



#посмотреть все файлы статьи
@editor_router.get("/rendering/files/{art_id}")
async def render(art_id ):
    return await Editor(art_id=art_id).rendering()

#заменить файл
@editor_router.put("/update/file/{art_id}/{f_id}")
async def updt(art_id ):
    return await Editor(art_id=art_id).update()

#добавить файл в статью
@editor_router.post("/add/file/{art_id}/{f_id}")
async def set_new(data = Body()):
    return await Editor().add(data())