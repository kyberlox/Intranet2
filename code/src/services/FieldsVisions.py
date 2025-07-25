from src.base.pSQLmodels import FieldvisionModel, UservisionsRootModel
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
    def __init__(self, vision_name: str = '', vision_id: int = 0, user_id: int = 0):
        self.vision_name = vision_name
        self.vision_id = vision_id
        self.user_id = user_id

    def get_all_directors(self):
        return StructureSearchModel().get_directors()

    def get_dep_structure(self, parent_id):
        return StructureSearchModel().get_structure_by_parent_id(parent_id)

    def get_dep_structure_by_name(self, name):
        return StructureSearchModel().get_structure_by_name(name)
    
    def create_new_vision(self):
        return FieldvisionModel(vision_name=self.vision_name).add_field_vision()
    
    def get_vision_by_id(self):
        return FieldvisionModel(id=self.vision_id).find_vision_by_id()

    def delete_vision(self):
        return FieldvisionModel(id=self.vision_id).remove_field_vision()
    
    def get_all_visions(self):
        return FieldvisionModel().find_all_visions()

    def add_user_to_vision(self):
        return UservisionsRootModel(vision_id=self.vision_id, user_id=self.user_id).upload_user_to_vision()

    def add_users_list_to_vision(self, dep_id):
        all_dep_users = []
        dep = self.get_dep_structure(dep_id)
        for de in dep:
            for user in de['users']:
                all_dep_users.append(user['user_id'])
        return UservisionsRootModel(vision_id=self.vision_id).upload_users_to_vision(all_dep_users)
    
    def delete_user_from_vision(self):
        return UservisionsRootModel(vision_id=self.vision_id, user_id=self.user_id).remove_user_from_vision()

    def get_users_in_vision(self):
        return UservisionsRootModel(vision_id=self.vision_id).find_users_in_vision()


@fieldsvisions_router.get("/get_all_directors")
def get_all_directors():
    return Visions().get_all_directors()

@fieldsvisions_router.get("/get_dep_structure/{parent_id}")
def get_dep_structure(parent_id: int):
    return Visions().get_dep_structure(parent_id)

@fieldsvisions_router.get("/get_dep_structure_by_name/{word}")
def get_dep_structure_by_name(word: str):
    return Visions().get_dep_structure_by_name(word)

@fieldsvisions_router.get("/get_all_visions")
def get_all_visions():
    return Visions().get_all_visions()

@fieldsvisions_router.put("/create_new_vision/{vision_name}")
def create_new_vision(vision_name: str):
    return Visions(vision_name).create_new_vision()

@fieldsvisions_router.delete("/delete_vision/{vision_id}")
def delete_vision(vision_id: int):
    return Visions(vision_id).delete_vision()

@fieldsvisions_router.put("/add_user_to_vision/{vision_id}/{user_id}")
def add_user_to_vision(vision_id: int, user_id: int):
    return Visions(vision_id=vision_id, user_id=user_id).add_user_to_vision()

@fieldsvisions_router.put("/add_users_list_to_vision/{vision_id}/{dep_id}")
def add_users_list_to_vision(vision_id: int, dep_id: int):
    return Visions(vision_id=vision_id).add_users_list_to_vision(dep_id)

@fieldsvisions_router.delete("/delete_user_from_vision/{vision_id}/{user_id}")
def delete_user_from_vision(vision_id: int, user_id: int):
    return Visions(vision_id=vision_id, user_id=user_id).delete_user_from_vision()

@fieldsvisions_router.get("/get_users_in_vision/{vision_id}")
def get_users_in_vision(vision_id: int):
    return Visions(vision_id=vision_id).get_users_in_vision()