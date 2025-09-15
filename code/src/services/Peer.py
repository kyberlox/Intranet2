from ..base.pSQL.objects import ActivitiesModel, ModersModel, ActiveUsersModel, AdminModel
from fastapi import APIRouter, Body, Request

from ..model import User
from .Auth import AuthService

peer_router = APIRouter(prefix="/peer", tags=["Сервис системы эффективности"])

class Peer:
    def __init__(self, id: int = 0, name: str = '', coast: int = 0, user_uuid: int = 0, need_valid: bool = False, activities_id: int = 0):
        self.id = id
        self.name = name
        self.coast = coast
        self.user_uuid = user_uuid
        self.need_valid = need_valid
        self.activities_id = activities_id
    
    """Ручки которые доступны любому пользователю"""
    def sum(self, session_id): 
        user = self.get_user_by_session_id(session_id)
        return ActiveUsersModel(uuid_to=user).sum()
    
    def statistics(self, session_id):
        user = self.get_user_by_session_id(session_id) 
        return ActiveUsersModel(uuid_to=user).statistics()
    
    def actions(self, session_id):
        user = self.get_user_by_session_id(session_id)  
        return ActiveUsersModel(uuid_from=user).actions()
    """"""
    def get_all_activities(self):
        return ActivitiesModel().find_all_activities()

    def upload_base_activities(self):
        return ActivitiesModel().upload_base_activities()
    
    def edit_activity(self):
        return ActivitiesModel(id=self.id, name=self.name, coast=self.coast, need_valid=self.need_valid).update_activity()
    
    def remove_activity(self):
        return ActivitiesModel(id=self.id).delete_activity()
    """"""
    def upload_past_moders(self):
        return ModersModel().upload_past_moders()
    
    def confirmation(self): 
        return ModersModel(activities_id=self.activities_id).confirmation()
    
    def do_valid(self, action_id): 
        return ModersModel(uuid=self.user_uuid).do_valid(action_id)

    def do_not_valid(self, action_id): 
        return ModersModel(uuid=self.user_uuid).do_not_valid(action_id)

    def confirmation(self): 
        return ModersModel(activities_id=self.activities_id).confirmation()
    
    def get_moders(self): 
        return ModersModel().get_moders()
    
    def add_moder(self): 
        return ModersModel(activities_id=self.activities_id, uuid=self.user_uuid).add_moder()

    def is_moder(self): 
        return ModersModel(uuid=self.user_uuid).is_moder()
    """"""
    def upload_past_activeusers(self): 
        return ActiveUsersModel().upload_past_table_ActiveUsers()
        
    def history_mdr(self, activity_name): 
        return ActiveUsersModel().history_mdr(activity_name)

    def top(self): 
        return ActiveUsersModel().top()

    def my_place(self): 
        return ActiveUsersModel(uuid_to=self.user_uuid).my_place()

    
    
    def statistic_history(self):
        return ActiveUsersModel(uuid_to=self.user_uuid, activities_id=self.activities_id).statistics_history()

    def new_a_week(self): 
        return ActiveUsersModel(uuid_to=self.user_uuid).new_a_week()
    
    def user_history(self): 
        return ActiveUsersModel(uuid_to=self.user_uuid).user_history()
    """"""
    def new_active(self, data):
        return AdminModel().new_active(data)

    def get_admins_list(self):
        return AdminModel().get_admins_list()

    def add_peer_admin(self):
        return AdminModel(uuid=self.user_uuid).add_peer_admin()

    def delete_admin(self):
        return AdminModel(uuid=self.user_uuid).delete_admin()
    
    def get_user_by_session_id(self, session_id):
        user = dict(AuthService().get_user_by_seesion_id(session_id))

        if user is not None:
            user_uuid = user["user_uuid"]
            username = user["username"]

            #получить и вывести его id
            user_inf = User(uuid = user_uuid).user_inf_by_uuid()
            return user_inf["ID"]
        return None



# дампит старые данные
@peer_router.put("/put_tables")
def load_activities():
    Peer().upload_base_activities()
    Peer().upload_past_moders()
    Peer().upload_past_activeusers()
    return {"status": True} 

"""Ручки которые доступны любому пользователю"""
@peer_router.get("/sum")
def sum(request: Request):
    session_id = ""
    token = request.cookies.get("Authorization")
    if token is None:
        token = request.headers.get("Authorization")
        if token is not None:
            session_id = token
    else:
        session_id = token

    return Peer().sum(session_id=session_id)


@peer_router.get("/statistics")
def statistics(request: Request):
    session_id = ""
    token = request.cookies.get("Authorization")
    if token is None:
        token = request.headers.get("Authorization")
        if token is not None:
            session_id = token
    else:
        session_id = token
    return Peer().statistics(session_id=session_id)

@peer_router.get("/actions")
def actions(request: Request):
    session_id = ""
    token = request.cookies.get("Authorization")
    if token is None:
        token = request.headers.get("Authorization")
        if token is not None:
            session_id = token
    else:
        session_id = token
    return Peer().actions(session_id=session_id)
""""""
@peer_router.get("/get_all_activities")
def get_activities():
    return Peer().get_all_activities()

@peer_router.post("/edit_activity")
def edit_activity(data = Body()):
    return Peer(id=data['id'], name=data['name'], coast=data['coast'], need_valid=data['need_valid']).edit_activity()

@peer_router.delete("/remove_activity")
def remove_activity(id: str):
    return Peer(id=id).remove_activity()
""""""
@peer_router.post("/do_valid/{action_id}/{uuid}")
def do_valid(action_id: int, uuid: int):
    return Peer(user_uuid=uuid).do_valid(action_id) 

@peer_router.post("/do_not_valid/{action_id}/{uuid}")
def do_not_valid(action_id: int, uuid: int):
    return Peer(user_uuid=uuid).do_not_valid(action_id) 

@peer_router.get("/confirmation/{activities_id}")
def confirmation(activities_id: int):
    return Peer(activities_id=activities_id).confirmation()

@peer_router.get("/get_moders")
def get_moders():
    return Peer().get_moders()

@peer_router.put("/add_moder/{activities_id}/{uuid}")
def add_moder(activities_id: int, uuid: int):
    return Peer(user_uuid=uuid, activities_id=activities_id).add_moder() 

@peer_router.get("/is_moder/{uuid}")
def is_moder(uuid: int):
    return Peer(user_uuid=uuid).is_moder()
""""""
@peer_router.get("/history_mdr/{activity_name}")
def history_mdr(activity_name: str):
    return Peer().history_mdr(activity_name)

@peer_router.get("/statistics_history/{activities_id}/{uuid}")
def statistics_history(activities_id: int, uuid: int):
    return Peer(activities_id=activities_id, user_uuid=uuid).statistic_history()

@peer_router.get("/top")
def top():
    return Peer().top()

@peer_router.get("/my_place/{uuid}")
def my_place(uuid: int):
    return Peer(user_uuid=uuid).my_place()


# @peer_router.get("/statistics_history/{activities_id}/{uuid}")
# def statistics_history(activities_id: int, uuid: int):
#     return Peer(user_uuid=uuid, activities_id=activities_id).statistic_history()

@peer_router.get("/new_a_week/{uuid}")
def new_a_week(uuid: int):
    return Peer(user_uuid=uuid).new_a_week()

@peer_router.get("/user_history/{uuid}")
def user_history(uuid: int):
    return Peer(user_uuid=uuid).user_history()
""""""
@peer_router.put("/send_points")
def send_points(data = Body()):
    return Peer().new_active(data) # {"uuid_from": "4133", "uuid_to": "2375", "activities_id": 0, "description": "Крутой тип"}

@peer_router.get("/get_admins_list")
def get_admins_list():
    return Peer().get_admins_list()

@peer_router.put("/add_peer_admin/{uuid}")
def add_peer_admin(uuid: int):
    return Peer(user_uuid=uuid).add_peer_admin()

@peer_router.delete("/delete_admin/{uuid}")
def delete_admin(uuid: str):
    return Peer(user_uuid=uuid).delete_admin()

