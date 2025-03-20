from src.pSQLmodels import DepartmentModel
from src.B24 import B24

import requests
import json

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

        #отправить записи
        for dep in data:
            #if dep['ID'] == '420':
            DepSQL.upsert_dep(dep)
            

        return {"status" : True}
    
    def search_dep_by_id(self):
        return DepartmentModel(self.id).find_dep_by_id()