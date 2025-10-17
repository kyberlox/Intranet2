from fastapi import APIRouter, Request
from .LogsMaker import LogsMaker
from ..model.User import User

roots_router = APIRouter(prefix="/roots", tags=["Права пользователя"])

class Roots:
    def __init__(self, user_uuid=0):
        from ..base.pSQL.objects.RootsModel import RootsModel
        self.RootsModel = RootsModel()

        self.user_uuid = user_uuid

    def create_primary_admins(self):
        result = self.RootsModel.create_primary_admins()
        return True

    def create_editor_moder(self, sec_id):
        self.RootsModel.user_uuid = self.user_uuid
        return self.RootsModel.create_editor_moder(sec_id)
    
    def delete_editor_moder(self, sec_id):
        self.RootsModel.user_uuid = self.user_uuid
        return self.RootsModel.delete_editor_moder(sec_id)
    
    def create_editor_admin(self):
        self.RootsModel.user_uuid = self.user_uuid
        return self.RootsModel.create_editor_admin()
    
    def delete_editor_admin(self):
        self.RootsModel.user_uuid = self.user_uuid
        return self.RootsModel.delete_editor_admin()
    
    def get_editors_list(self, sec_id):
        return self.RootsModel.get_editors_list(sec_id)
    
    def get_token_by_uuid(self):
        self.RootsModel.user_uuid = self.user_uuid
        return self.RootsModel.get_token_by_uuid()
    
    def token_processing_for_editor(self, roots):
        self.RootsModel.user_uuid = self.user_uuid
        return self.RootsModel.token_processing_for_editor(roots)

def get_uuid_from_request(request):
    from .Auth import AuthService
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

def get_editor_roots(user_uuid):
    roots_model = Roots()
    roots_model.user_uuid = user_uuid
    all_roots = roots_model.get_token_by_uuid()
    editor_roots = roots_model.token_processing_for_editor(all_roots)
    return editor_roots

@roots_router.put("/create_primary_admins")
def create_primary_admins():
    return Roots().create_primary_admins()

@roots_router.put("/create_editor_moder/{user_uuid}/{sec_id}")
def create_editor_moder(user_uuid: int, sec_id: int, request: Request):
    user_id = get_uuid_from_request(request)
    editor_roots = get_editor_roots(user_id)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return Roots(user_uuid=user_uuid).create_editor_moder(sec_id)
    return LogsMaker().warning_message(f"Недостаточно прав")

@roots_router.delete("/delete_editor_moder/{user_uuid}/{sec_id}")
def delete_editor_moder(user_uuid: int, sec_id: int, request: Request):
    user_id = get_uuid_from_request(request)
    editor_roots = get_editor_roots(user_id)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return Roots(user_uuid=user_uuid).delete_editor_moder(sec_id)
    return LogsMaker().warning_message(f"Недостаточно прав")
    

@roots_router.put("/create_editor_admin/{user_uuid}")
def create_editor_admin(user_uuid: int, request: Request):
    user_id = get_uuid_from_request(request)
    editor_roots = get_editor_roots(user_id)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return Roots(user_uuid=user_uuid).create_editor_admin()
    return LogsMaker().warning_message(f"Недостаточно прав")
    

@roots_router.delete("/delete_editor_admin/{user_uuid}")
def delete_editor_admin(user_uuid: int, request: Request):
    user_id = get_uuid_from_request(request)
    editor_roots = get_editor_roots(user_id)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return Roots(user_uuid=user_uuid).delete_editor_admin()
    return LogsMaker().warning_message(f"Недостаточно прав")
    

@roots_router.get("/get_editors_list/{sec_id}")
def get_editors_list(sec_id: int, request: Request):
    user_id = get_uuid_from_request(request)
    editor_roots = get_editor_roots(user_id)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return Roots().get_editors_list(sec_id)
    return LogsMaker().warning_message(f"Недостаточно прав")

@roots_router.get("/get_root_token_by_uuid")
def get_token_by_uuid(request: Request):
    user_id = get_uuid_from_request(request)
    user_roots = Roots(user_uuid=user_id).get_token_by_uuid()
    return user_roots
    