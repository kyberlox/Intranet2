from src.base.pSQLmodels import DepartmentModel
from src.base.SearchModel import StructureSearchModel
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

# можно выгрузить иерархию
@depart_router.get("/structure")
def view_all_departs():
    return StructureSearchModel().get_structure()

#Пользователя можно найти
@depart_router.post("/search/{username}")
def get_user(username: str): # jsn=Body()
    return StructureSearchModel().search_by_username(username)

#По названию должностей можно найти отдел и пользователя
@depart_router.post("/search_by_position/{position}")
def get_user_by_position(position: str): # jsn=Body()
    return StructureSearchModel().search_by_position(position)

#загрузить дату в ES
@depart_router.put("/elastic_data")
def upload_department_to_es():
    return StructureSearchModel().dump()