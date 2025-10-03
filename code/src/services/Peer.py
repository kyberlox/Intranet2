# from ..base.pSQL.objects import ActivitiesModel, ActiveUsersModel, RootsModel, PeerUserModel
from fastapi import APIRouter, Body, Request

from ..model import User
from .Auth import AuthService

#тут придется отладить ВСЕ

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

        self.RootsModel.user_uuid = self.user_uuid
        self.Roots = self.RootsModel.get_token_by_uuid()
        self.roots = self.RootsModel.token_processing_for_peer(self.Roots)
    
    """Ручки которые доступны любому пользователю"""
    def sum(self):
        result = self.ActiveUsersModel.sum(self.user_uuid)
        return result
    
    def statistics(self):
        self.ActiveUsersModel.uuid_to = self.user_uuid
        return self.ActiveUsersModel.statistics()
    
    def actions(self):
        result = self.ActiveUsersModel.actions(self.roots)
        return result
    """"""
    def get_all_activities(self):
        result = self.ActivitiesModel.find_all_activities()
        return result

    # def upload_base_activities(self):
    #     return self.ActivitiesModel.upload_base_activities()
    
    def edit_activity(self):
        self.ActivitiesModel.id = self.id
        self.ActivitiesModel.name = self.name
        self.ActivitiesModel.coast = self.coast
        self.ActivitiesModel.need_valid = self.need_valid
        return self.ActivitiesModel.update_activity(self.roots)
    
    def remove_activity(self):
        self.ActivitiesModel.id = self.id
        return self.ActivitiesModel.delete_activity(self.roots)
    """"""
    # def upload_past_moders(self):
    #     return self.PeerUserModel().upload_past_moders()
    
    def confirmation(self): 
        self.PeerUserModel.activities_id = self.activities_id
        return self.PeerUserModel.confirmation()
    
    def do_valid(self, action_id, uuid_to): 
        self.PeerUserModel.uuid = self.user_uuid
        return self.PeerUserModel.do_valid(action_id, uuid_to, self.roots)

    def do_not_valid(self, action_id): 
        self.PeerUserModel.uuid = self.user_uuid
        return self.PeerUserModel.do_not_valid(action_id, self.roots)

    def points_to_confirm(self): 
        self.PeerUserModel.activities_id = self.activities_id
        return self.PeerUserModel.points_to_confirm()
    
    def get_curators(self): 
        return self.PeerUserModel.get_curators()
    
    def add_curator(self, user_id):
        self.PeerUserModel.activities_id = self.activities_id
        self.PeerUserModel.uuid = user_id
        return self.PeerUserModel.add_curator(roots=self.roots)
    
    def delete_curator(self, user_id):
        self.PeerUserModel.activities_id = self.activities_id
        self.PeerUserModel.uuid = user_id
        result = self.PeerUserModel.delete_curator(roots=self.roots)
        return result

    def new_activity(self, data): 
        data["uuid"] = self.user_uuid
        return self.ActivitiesModel.new_activity(data, self.roots)

    """"""
    # def upload_past_activeusers(self): 
    #     return self.ActiveUsersModel().upload_past_table_ActiveUsers()
        
    # def history_mdr(self, activity_name): 
    #     return self.ActiveUsersModel().history_mdr(activity_name)

    # def top(self): 
    #     return self.ActiveUsersModel().top()

    # def my_place(self): 
    #     return self.ActiveUsersModel(uuid_to=self.user_uuid).my_place()
    
    # def statistics_history(self):
    #     return self.ActiveUsersModel(uuid_to=self.user_uuid, activities_id=self.activities_id).statistics_history()

    # def new_a_week(self): 
    #     return self.ActiveUsersModel(uuid_to=self.user_uuid).new_a_week()
    
    def user_history(self): 
        self.ActiveUsersModel.uuid_to = self.user_uuid
        return self.ActiveUsersModel.user_history()
    """"""
    def send_points(self, data):
        return self.PeerUserModel.send_points(data=data, roots=self.roots)

    def get_admins_list(self):
        return self.PeerUserModel.get_admins_list(self.roots)

    def add_peer_admin(self, uuid):
        self.PeerUserModel.uuid = uuid
        return self.PeerUserModel.add_peer_admin(self.roots)

    def delete_admin(self, uuid):
        self.PeerUserModel.uuid = uuid
        return self.PeerUserModel.delete_admin(self.roots)
    
    def get_moders_list(self):
        return self.PeerUserModel.get_moders_list(self.roots)

    def add_peer_moder(self, uuid):
        self.PeerUserModel.uuid = uuid
        return self.PeerUserModel.add_peer_moder(self.roots)

    def delete_peer_moder(self, uuid):
        self.PeerUserModel.uuid = uuid
        return self.PeerUserModel.delete_peer_moder(self.roots)
    
    def get_curators_history(self):
        return self.PeerUserModel.get_curators_history(self.roots)

    def return_points_to_user(self, note_id, user_uuid):
        return self.PeerUserModel.return_points_to_user(note_id, user_uuid)
    
    def remove_user_points(self, action_id, user_uuid):
        self.PeerUserModel.uuid = user_uuid
        return self.PeerUserModel.remove_user_points(action_id, self.roots)
        
    

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
        user = User()
        user.uuid = user_uuid
        user_inf = user.user_inf_by_uuid()
        if user_inf is not None and "ID" in user_inf.keys():
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
def get_actions(request: Request):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid).actions()
""""""
@peer_router.get("/get_all_activities")
def get_activities():
    return Peer().get_all_activities()

@peer_router.post("/edit_activity")
def post_edit_activity(request: Request, data = Body()):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid, id=data['id'], name=data['name'], coast=data['coast'], need_valid=data['need_valid']).edit_activity()

@peer_router.delete("/remove_activity/{id}")
def del_remove_activity(request: Request, id: str):
    uuid = get_uuid_from_request(request)
    return Peer(id=id, user_uuid=uuid).remove_activity()
""""""
@peer_router.post("/do_valid/{action_id}/{uuid_to}")
def post_do_valid(request: Request, action_id: int, uuid_to: int):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid).do_valid(action_id, uuid_to) 

@peer_router.post("/do_not_valid/{action_id}")
def post_do_not_valid(request: Request, action_id: int):
    uuid = get_uuid_from_request(request)
    return Peer(user_uuid=uuid).do_not_valid(action_id) 

@peer_router.get("/points_to_confirm/{activities_id}")
def get_points_to_confirm(activities_id: int):
    return Peer(activities_id=activities_id).points_to_confirm()

@peer_router.get("/get_curators")
def get_req_curators():
    return Peer().get_curators()

@peer_router.put("/add_curator/{uuid}/{activities_id}")
def add_curator(uuid: int, request: Request, activities_id: int):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid, activities_id=activities_id).add_curator(uuid)

@peer_router.delete("/delete_curator/{uuid}/{activities_id}")
def delete_curator(uuid: int, request: Request, activities_id: int):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid, activities_id=activities_id).delete_curator(uuid)

@peer_router.put("/new_activity")
def put_new_activity(request: Request, data = Body()):
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

@peer_router.get("/get_curators_history")
def get_curators_history(request: Request):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).get_curators_history()

@peer_router.post("/return_points_to_user/{user_uuid}/{note_id}")
def return_points_to_user(user_uuid: int, note_id: int):
    return Peer().return_points_to_user(note_id, user_uuid)

@peer_router.post("/remove_user_points/{uuid}/{action_id}")
def remove_user_points(request: Request, uuid: int, action_id: int):
    user_uuid = get_uuid_from_request(request)
    return Peer(user_uuid=user_uuid).remove_user_points(action_id, uuid)