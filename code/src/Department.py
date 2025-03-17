from src.pSQLmodels import DepartmentModel
from src.B24 import B24

import requests
import json

class Department:
    def __init__(self, id, name, father_id, data):
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