from src.base.pSQLmodels import ActivitiesModel, ModersModel, ActiveUsersModel
from fastapi import APIRouter, Body

peer_router = APIRouter(prefix="/peer", tags=["Сервис системы эффективности"])

class Peer:
    def __init__(self, id: int = 0, name: str = '', coast: int = 0, user_uuid: int = 0, need_valid: bool = False, activities_id: int = 0):
        self.id = id
        self.name = name
        self.coast = coast
        self.user_uuid = user_uuid
        self.need_valid = need_valid
        self.activities_id = activities_id
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
    """"""
    def upload_past_activeusers(self): 
        return ActiveUsersModel().upload_past_table_ActiveUsers()

    def actions(self): 
        return ActiveUsersModel(uuid_from=self.user_uuid).actions()




@peer_router.put("/put_tables")
def load_activities():
    Peer().upload_base_activities()
    Peer().upload_past_moders()
    Peer().upload_past_activeusers()
    return {"status": True} 

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
""""""
@peer_router.get("/actions/{uuid}")
def actions(uuid: int):
    return Peer(user_uuid=uuid).actions()

