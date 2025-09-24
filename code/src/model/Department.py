# from ..base.Elastic.StuctureSearchmodel import StructureSearchModel
from ..services.LogsMaker import LogsMaker

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

        from ..base.pSQL.objects.DepartmentModel import DepartmentModel
        self.department = DepartmentModel()

    def fetch_departments_data(self):
        from ..base.B24 import B24
        data = B24().getDeps()
        logg = LogsMaker()

        #отправить записи
        for dep in logg.progress(data, "Загрузка данных подразделений "):
            #if dep['ID'] == '420':
            self.department.upsert_dep(dep)
            
        # StructureSearchModel().create_index()
        return {"status" : True}
    
    def search_dep_by_id(self):
        self.department.id = self.id
        return self.department.find_dep_by_id()


# Департаменты можно обновить
@depart_router.put("")
def get_department():
    depart = Department()
    return depart.fetch_departments_data()

# Департамент можно выгрузить
@depart_router.get("/find_by/{id}")
def get_department(id):
    return Department(id).search_dep_by_id()

#загрузить дату в ES
@depart_router.put("/elastic_data")
def upload_department_to_es():
    return StructureSearchModel().dump()

