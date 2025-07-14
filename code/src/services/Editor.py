from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.base.pSQLmodels import ArticleModel
from src.base.SearchModel import ArticleSearchModel
from src.base.mongodb import FileModel
from src.model.Article import Article
from src.model.File import File

editor_router = APIRouter(prefix="/editor", tags=["Редактор"])

class Editor:
    #тут можно объявить классы лоя работы со статьями и файлами
    self.Article = Article()
    self.File = File()

    #словарь полей
    fields_data_file = open("./src/base/fields.json", "r")
    self.fields = json.load(section_data_file)
    fields_data_file.close()
    
    def __init__(self, id=None, art_id=None):
        self.id = id #в будущем надо хранить изменения в таблице, чтобы знать, кто сколько чего публиковал, кто чего наредактировал
        self.art_id = art_id
    
    def rendering():
        if self.art_id is None:
            return 
        # вытащить основные поля из psql
        # вытащить поля из psql -> idirect_data
        # протащить через словарь полей
        # вытащить файлы 
        # вывести
    
    def update():
        if self.art_id is None:
            return 
        # перезаписать основные поля из psql
        # перезаписать поля из psql -> idirect_data
        # перезаписать файлы 
        # сохранить



@editor_router.get("/rendering/{art_id}")
async def render(art_id ):
    return await Editor(art_id=art_id).rendering()

@editor_router.put("/update/{art_id}")
async def updt(art_id ):
    return await Editor(art_id=art_id).update()