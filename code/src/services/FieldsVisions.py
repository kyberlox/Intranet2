from src.base.pSQLmodels import FieldVissionModel, UserVissionsRootModel
from src.base.SearchModel import StructureSearchModel, UserSearchModel
from src.base.B24 import B24
from src.services.LogsMaker import LogsMaker

#from fastapi import APIRouter

from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from jinja2 import Environment, FileSystemLoader
# import json

fieldsvisions_router = APIRouter(prefix="/fields_visions", tags=["Сервис области видимости"])

class Visions:
    def __init__(self, vission_name: str = '', vission_id: int = 0, user_id: int = 0):
        self.vission_name = vission_name
        self.vission_id = vission_id
        self.user_id = user_id

    def get_all_directors(self):
        return StructureSearchModel().get_directors()

    def get_dep_structure(self, parent_id):
        return StructureSearchModel().get_structure_by_parent_id(parent_id)

    def get_dep_structure_by_name(self, name):
        return StructureSearchModel().get_structure_by_name(name)
    
    def create_new_vission(self):
        return FieldVissionModel(vission_name=self.vission_name).add_field_vission()
    
    def get_vission_by_id(self):
        return FieldVissionModel(id=self.vission_id).find_vission_by_id()

    def delete_vission(self):
        return FieldVissionModel(id=self.vission_id).remove_field_vission()
    
    def get_all_vissions(self):
        return FieldVissionModel().find_all_vissions()

    def add_user_to_vission(self):
        return UserVissionsRootModel(vission_id=self.vission_id, user_id=self.user_id).upload_user_to_vission()

    def add_users_list_to_vission(self, dep_id):
        all_dep_users = []
        dep = self.get_dep_structure(dep_id)
        for de in dep:
            for user in de['users']:
                all_dep_users.append(user['user_id'])
        return UserVissionsRootModel(vission_id=self.vission_id).upload_users_to_vission(all_dep_users)
    
    def delete_user_from_vission(self):
        return UserVissionsRootModel(vission_id=self.vission_id, user_id=self.user_id).remove_user_from_vission()

    def get_users_in_vission(self):
        return UserVissionsRootModel(vission_id=self.vission_id).find_users_in_vission()


@fieldsvisions_router.get("/get_all_directors")
def get_all_directors():
    return Visions().get_all_directors()

@fieldsvisions_router.get("/get_dep_structure/{parent_id}")
def get_dep_structure(parent_id: int):
    return Visions().get_dep_structure(parent_id)

@fieldsvisions_router.get("/get_dep_structure_by_name/{word}")
def get_dep_structure_by_name(word: str):
    return Visions().get_dep_structure_by_name(word)

@fieldsvisions_router.get("/get_all_vissions")
def get_all_vissions():
    return Visions().get_all_vissions()

@fieldsvisions_router.put("/create_new_vission/{vission_name}")
def create_new_vission(vission_name: str):
    return Visions(vission_name).create_new_vission()

@fieldsvisions_router.delete("/delete_vission/{vission_id}")
def delete_vission(vission_id: int):
    return Visions(vission_id).delete_vission()

@fieldsvisions_router.put("/add_user_to_vission/{vission_id}/{user_id}")
def add_user_to_vission(vission_id: int, user_id: int):
    return Visions(vission_id=vission_id, user_id=user_id).add_user_to_vission()

@fieldsvisions_router.put("/add_users_list_to_vission/{vission_id}/{dep_id}")
def add_users_list_to_vission(vission_id: int, dep_id: int):
    return Visions(vission_id=vission_id).add_users_list_to_vission(dep_id)

@fieldsvisions_router.delete("/delete_user_from_vission/{vission_id}/{user_id}")
def delete_user_from_vission(vission_id: int, user_id: int):
    return Visions(vission_id=vission_id, user_id=user_id).delete_user_from_vission()

@fieldsvisions_router.get("/get_users_in_vission/{vission_id}")
def get_users_in_vission(vission_id: int):
    return Visions(vission_id=vission_id).get_users_in_vission()