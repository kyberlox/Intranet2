from src.base.pSQLmodels import DepartmentModel
from src.base.B24 import B24
from src.services.LogsMaker import LogsMaker

import requests
import json

from fastapi import APIRouter, Body, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="./front_jinja")

depart_router = APIRouter(prefix="/departments", tags=["Департамент"])

class Department:
    def __init__(self, id=0, name="", father_id="", data=""): #убрать = после каждой переменной в будущем
        self.id = id
        self.name = name
        self.father_id = father_id
        self.data = data

    def fetch_departments_data(self):
        b24 = B24()
        data = b24.getDeps()
        DepSQL = DepartmentModel()
        logg = LogsMaker()

        #отправить записи
        for dep in logg.progress(data, "Загрузка данных подразделений "):
            #if dep['ID'] == '420':
            DepSQL.upsert_dep(dep)
            

        return {"status" : True}
    
    def search_dep_by_id(self):
        return DepartmentModel(self.id).find_dep_by_id()


# Департаменты можно обновить
@depart_router.put("")
def get_department():
    depart = Department()
    return depart.fetch_departments_data()

# фронт
@depart_router.get("/view")
def get_user(request: Request):
    return templates.TemplateResponse(name="depart.html", context={"request": request})

# Департамент можно выгрузить
@depart_router.get("/find_by/{id}")
def get_department(id):
    return Department(id).search_dep_by_id()

#Пользователя можно найти
@depart_router.post("/search")
def get_user(jsn=Body()):
    #будет работать через elasticsearch
    pass

