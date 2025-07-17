from src.base.pSQLmodels import UsDepModel
from src.base.SearchModel import StructureSearchModel
from src.base.B24 import B24
from src.services.LogsMaker import LogsMaker

from fastapi import APIRouter

usdep_router = APIRouter(prefix="/users_depart", tags=["Пользователь-Департамент"])



class UsDep:
    def __init__(self, ID=0, usr_id=0, dep_id=0):
        self.ID = ID
        self.usr_id = usr_id
        self.dep_id = dep_id
    
    def get_usr_dep(self):
        b24 = B24()
        data = b24.getUsers()
        UserSQL = UsDepModel()
        logg = LogsMaker()
        
        result = dict()
        # for usr in logg.progress(data, "Загрузка данных связей пользователей и подразделений "):


        for usr in logg.progress(data, "Загрузка данных связей пользователей и подразделений "):
            if usr['ID'] is not None:
                result[int(usr['ID'])] = usr['UF_DEPARTMENT']
        StructureSearchModel().dump()
        return {"status" : UserSQL.put_uf_depart(result)}
        
    def search_usdep_by_id(self):
        return UsDepModel(self.ID).find_dep_by_user_id()


#Таблицу пользователей и департаментов можно обновить
@usdep_router.put("")
def get_user():
    return UsDep().get_usr_dep()

#Пользователя и его департамент можно выгрузить
@usdep_router.get("/find_by/{id}")
def get_usdepart(id):
    return UsDep(id).search_usdep_by_id()

#поиск по id подразделения
@usdep_router.get("/get_structure_by_dep_id/{parent_id}")
def get_structure_by_dep_id(parent_id: int):
    return StructureSearchModel().get_structure_by_id(parent_id)
