from ..base.pSQL.objects import FieldvisionModel, UservisionsRootModel, RootsModel
from ..base.Elastic.StuctureSearchmodel import StructureSearchModel
from .LogsMaker import LogsMaker

from .Auth import AuthService
from ..model.User import User
#from fastapi import APIRouter

from fastapi import APIRouter, Request, Body
# from fastapi.responses import HTMLResponse
# from jinja2 import Environment, FileSystemLoader
# import json

fieldsvisions_router = APIRouter(prefix="/fields_visions", tags=["Сервис области видимости"])

class Visions:
    def __init__(self, vision_name: str = '', vision_id: int = 0, user_id: int = 0):
        self.vision_name = vision_name
        self.vision_id = vision_id
        self.user_id = user_id

        self.Roots = RootsModel(user_uuid=self.user_id).get_token_by_uuid()
        self.roots = RootsModel(user_uuid=self.user_id).token_processing_for_vision(self.Roots)

    def get_full_structure(self):
        return StructureSearchModel().get_full_structure()

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

    def add_user_to_vision(self, user_to):
        return UservisionsRootModel(vision_id=self.vision_id, user_id=self.user_id).upload_user_to_vision(user_to, self.roots)

    def add_full_usdep_list_to_vision(self, dep_id):
        all_dep_users = []
        if dep_id == 53:
            dep = self.get_dep_structure(dep_id)
            for de in dep:
                if de['id'] == 53:
                    for user in de['users']:
                        all_dep_users.append(user['id'])
                else:
                    dep_n_1 = self.get_dep_structure(de['id'])
                    for dep_users in dep_n_1:
                        for user in dep_users['users']:
                            all_dep_users.append(user['id'])

        else:
            dep = self.get_dep_structure(dep_id)
            for de in dep:
                for user in de['users']:
                    all_dep_users.append(user['user_id'])
        return UservisionsRootModel(vision_id=self.vision_id).upload_users_to_vision(self.roots, all_dep_users)
    
    def add_dep_users_only(self, dep_id):
        all_dep_users = []
        dep = self.get_dep_structure(dep_id)
        for de in dep:
            if de['id'] == dep_id:
                for user in de['users']:
                    all_dep_users.append(user['user_id'])
                break
            else:
                pass
        return UservisionsRootModel(vision_id=self.vision_id).upload_users_to_vision(self.roots, all_dep_users)
        
    def add_users_list_to_vision(self, users):
        return UservisionsRootModel(vision_id=self.vision_id).upload_users_to_vision(users, self.roots)

    def delete_user_from_vision(self, user):
        return UservisionsRootModel(vision_id=self.vision_id, user_id=self.user_id).remove_user_from_vision(self.roots)
    
    def delete_users_from_vision(self, users):
        return UservisionsRootModel(vision_id=self.vision_id).remove_users_from_vision(users, self.roots)

    def get_users_in_vision(self):
        return UservisionsRootModel(vision_id=self.vision_id).find_users_in_vision()
    
    def remove_depart_in_vision(self, dep_id):
        return UservisionsRootModel(vision_id=self.vision_id).remove_depart_in_vision(dep_id, self.roots)

def get_uuid_from_request(request):
    session_id = ""
    token = request.cookies.get("Authorization")
    if token is None:
        token = request.headers.get("Authorization")
        if token is not None:
            session_id = token
    else:
        session_id = token
    
    user = dict(AuthService().get_user_by_seesion_id(session_id))

    if user is not None:
        user_uuid = user["user_uuid"]
        username = user["username"]

        #получить и вывести его id
        user_inf = User(uuid = user_uuid).user_inf_by_uuid()
        return user_inf["ID"]
    return None


@fieldsvisions_router.get("/get_full_structure")
def get_full_structure():
    return Visions().get_full_structure()

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
    return Visions(vision_id=vision_id).delete_vision()

@fieldsvisions_router.put("/add_user_to_vision/{vision_id}/{user_id}")
def add_user_to_vision(request: Request, vision_id: int, user_id: int):
    uuid = get_uuid_from_request(request)
    return Visions(vision_id=vision_id, user_id=uuid).add_user_to_vision(user_id)

@fieldsvisions_router.put("/add_dep_users_only/{vision_id}/{dep_id}")
def add_dep_users_only(request: Request, vision_id: int, dep_id: int):
    uuid = get_uuid_from_request(request)
    return Visions(vision_id=vision_id, user_id=uuid).add_dep_users_only(dep_id)

@fieldsvisions_router.put("/add_full_usdep_list_to_vision/{vision_id}/{dep_id}")
def add_full_usdep_list_to_vision(request: Request, vision_id: int, dep_id: int):
    uuid = get_uuid_from_request(request)
    return Visions(vision_id=vision_id, user_id=uuid).add_full_usdep_list_to_vision(dep_id)

@fieldsvisions_router.put("/add_users_list_to_vision/{vision_id}")
def add_users_list_to_vision(request: Request, vision_id: int, users = Body()):
    uuid = get_uuid_from_request(request)
    return Visions(vision_id=vision_id, user_id=uuid).add_users_list_to_vision(users)

@fieldsvisions_router.delete("/delete_user_from_vision/{vision_id}/{user_id}")
def delete_user_from_vision(request: Request, vision_id: int, user_id: int):
    uuid = get_uuid_from_request(request)
    return Visions(vision_id=vision_id, user_id=uuid).delete_user_from_vision(user_id)

@fieldsvisions_router.delete("/delete_users_from_vision/{vision_id}")
def delete_users_from_vision(request: Request, vision_id: int, users = Body()):
    uuid = get_uuid_from_request(request)
    return Visions(vision_id=vision_id, user_id=uuid).delete_users_from_vision(users)

@fieldsvisions_router.get("/get_users_in_vision/{vision_id}")
def get_users_in_vision(request: Request, vision_id: int):
    uuid = get_uuid_from_request(request)
    return Visions(vision_id=vision_id, user_id=uuid).get_users_in_vision()

@fieldsvisions_router.delete("/remove_depart_in_vision/{vision_id}/{dep_id}")
def remove_depart_in_vision(request: Request, vision_id: int, dep_id: int):
    uuid = get_uuid_from_request(request)
    return Visions(vision_id=vision_id, user_id=uuid).remove_depart_in_vision(dep_id)