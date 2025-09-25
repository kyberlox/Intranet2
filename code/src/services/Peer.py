# from ..base.pSQL.objects import ActivitiesModel, ActiveUsersModel, RootsModel, PeerUserModel
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

        from ..base.pSQL.objects.ActivitiesModel import ActivitiesModel
        self.ActivitiesModel = ActivitiesModel()

        from ..base.pSQL.objects.ActiveUsersModel import ActiveUsersModel
        self.ActiveUsersModel = ActiveUsersModel()

        from ..base.pSQL.objects.RootsModel import RootsModel
        self.RootsModel = RootsModel()

        from ..base.pSQL.objects.PeerUserModel import PeerUserModel
        self.PeerUserModel = PeerUserModel()

        self.Roots = self.RootsModel(user_uuid=self.user_uuid).get_token_by_uuid()
        self.roots = self.RootsModel(user_uuid=self.user_uuid).token_processing_for_vision(self.Roots)
    
    """Ручки которые доступны любому пользователю"""
    def sum(self): 
        return self.ActiveUsersModel().sum(self.user_uuid)
    
    def statistics(self):
        return self.ActiveUsersModel(uuid_to=self.user_uuid).statistics()
    
    def actions(self):
        return self.ActiveUsersModel().actions(self.roots)
    """"""
    def get_all_activities(self):
        return self.ActivitiesModel().find_all_activities()

    def upload_base_activities(self):
        return self.ActivitiesModel().upload_base_activities()
    
    def edit_activity(self):
        return self.ActivitiesModel(id=self.id, name=self.name, coast=self.coast, need_valid=self.need_valid).update_activity(self.roots)
    
    def remove_activity(self):
        return self.ActivitiesModel(id=self.id).delete_activity(self.roots)
    """"""
    def upload_past_moders(self):
        return self.PeerUserModel().upload_past_moders()
    
    def confirmation(self): 
        return self.PeerUserModel(activities_id=self.activities_id).confirmation()
    
    def do_valid(self, action_id, uuid_to): 
        return self.PeerUserModel(uuid=self.user_uuid).do_valid(action_id, uuid_to, self.roots)

    def do_not_valid(self, action_id): 
        return self.PeerUserModel(uuid=self.user_uuid).do_not_valid(action_id, self.roots)

    def points_to_confirm(self): 
        return self.PeerUserModel(activities_id=self.activities_id).points_to_confirm()
    
    def get_curators(self): 
        return self.PeerUserModel().get_curators()
    
    def new_activity(self, data): 
        return self.ActivitiesModel().new_activity(data, self.roots)

    """"""
    def upload_past_activeusers(self): 
        return self.ActiveUsersModel().upload_past_table_ActiveUsers()
        
    def history_mdr(self, activity_name): 
        return self.ActiveUsersModel().history_mdr(activity_name)

    def top(self): 
        return self.ActiveUsersModel().top()

    def my_place(self): 
        return self.ActiveUsersModel(uuid_to=self.user_uuid).my_place()
    
    def statistics_history(self):
        return self.ActiveUsersModel(uuid_to=self.user_uuid, activities_id=self.activities_id).statistics_history()

    def new_a_week(self): 
        return self.ActiveUsersModel(uuid_to=self.user_uuid).new_a_week()
    
    def user_history(self): 
        return self.ActiveUsersModel(uuid_to=self.user_uuid).user_history()
    """"""
    def send_points(self, data):
        return self.PeerUserModel().send_points(data=data, roots=self.roots)

    def get_admins_list(self):
        return self.PeerUserModel().get_admins_list(self.roots)

    def add_peer_admin(self, uuid):
        return self.PeerUserModel(uuid=uuid).add_peer_admin(self.roots)

    def delete_admin(self, uuid):
        return self.PeerUserModel(uuid=uuid).delete_admin(self.roots)
    
    def get_moders_list(self):
        return self.PeerUserModel().get_moders_list(self.roots)

    def add_peer_moder(self, uuid):
        return self.PeerUserModel(uuid=uuid).add_peer_moder(self.roots)

    def delete_peer_moder(self, uuid):
        return self.PeerUserModel(uuid=uuid).delete_peer_moder(self.roots)
    
    def get_moders_history(self):
        return self.PeerUserModel().get_moders_history(self.roots)

    def return_points_to_user(self, note_id, user_uuid):
        return self.PeerUserModel().return_points_to_user(note_id, user_uuid)
    

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


# # дампит старые данные
# @peer_router.put("/put_tables")
# def load_activities():
#     Peer().upload_base_activities()
#     Peer().upload_past_moders()
#     Peer().upload_past_activeusers()
#     return {"status": True} 

"""Ручки которые доступны любому пользователю"""
@peer_router.get("/sum")
def sum(request: Request):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid).sum()


# @peer_router.get("/statistics")
# def statistics(request: Request):
#     uuid = get_uuid_from_request(request)
#     return Peer(user_uuid=uuid).statistics()

@peer_router.get("/actions")
def actions(request: Request):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid).actions()
""""""
@peer_router.get("/get_all_activities")
def get_activities():
    return Peer().get_all_activities()

@peer_router.post("/edit_activity")
def edit_activity(request: Request, data = Body()):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid, id=data['id'], name=data['name'], coast=data['coast'], need_valid=data['need_valid']).edit_activity()

@peer_router.delete("/remove_activity")
def remove_activity(request: Request, id: str):
    uuid = get_uuid_from_request(request)
    return Peer(id=id, user_uuid=uuid).remove_activity()
""""""
@peer_router.post("/do_valid/{action_id}/{uuid_to}")
def do_valid(request: Request, action_id: int, uuid_to: int):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid).do_valid(action_id, uuid_to) 

@peer_router.post("/do_not_valid/{action_id}")
def do_not_valid(request: Request, action_id: int):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid).do_not_valid(action_id) 

@peer_router.get("/points_to_confirm/{activities_id}")
def points_to_confirm(activities_id: int):
    return Peer(activities_id=activities_id).points_to_confirm()

@peer_router.get("/get_curators")
def get_curators():
    return Peer().get_curators()

@peer_router.put("/new_activity")
def new_activity(request: Request, data = Body()):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid).new_activity(data) # {"name": str, "coast": int, "need_valid": bool, "uuid": str("*" или "4133")}

""""""
# @peer_router.get("/history_mdr/{activity_name}")
# def history_mdr(activity_name: str):
#     return Peer().history_mdr(activity_name)

# @peer_router.get("/statistics_history/{activities_id}/{uuid}")
# def statistics_history(activities_id: int, uuid: int):
#     return Peer(activities_id=activities_id, user_uuid=uuid).statistics_history()

# @peer_router.get("/top")
# def top():
#     return Peer().top()

# @peer_router.get("/my_place/{uuid}")
# def my_place(uuid: int):
#     return Peer(user_uuid=uuid).my_place()

# @peer_router.get("/new_a_week/{uuid}")
# def new_a_week(uuid: int):
#     return Peer(user_uuid=uuid).new_a_week()

@peer_router.get("/user_history")
def user_history(request: Request):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid).user_history()
""""""
@peer_router.put("/send_points")
def send_points(request: Request, data = Body()):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).send_points(data) # {"uuid_to": "2375", "activities_id": 0, "description": "Крутой тип"}

@peer_router.get("/get_admins_list")
def get_admins_list(request: Request):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).get_admins_list()

@peer_router.put("/add_peer_admin/{uuid}")
def add_peer_admin(uuid: int, request: Request):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).add_peer_admin(uuid)

@peer_router.delete("/delete_admin/{uuid}")
def delete_admin(uuid: str, request: Request):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).delete_admin(uuid)


@peer_router.get("/get_moders_list")
def get_moders_list(request: Request):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).get_moders_list()

@peer_router.put("/add_peer_moder/{uuid}")
def add_peer_moder(uuid: int, request: Request):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).add_peer_moder(uuid)

@peer_router.delete("/delete_peer_moder/{uuid}")
def delete_peer_moder(uuid: str, request: Request):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).delete_peer_moder(uuid)

@peer_router.get("/get_moders_history")
def get_moders_history(request: Request):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).get_moders_history()

@peer_router.post("/return_points_to_user/{user_uuid}/{note_id}")
def return_points_to_user(user_uuid: int, note_id: int):
    return Peer().return_points_to_user(note_id, user_uuid)