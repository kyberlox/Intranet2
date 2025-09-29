from fastapi import APIRouter

roots_router = APIRouter(prefix="/roots", tags=["Права пользователя"])

class Roots:
    def __init__(self):
        from ..base.pSQL.objects.RootsModel import RootsModel
        self.RootsModel = RootsModel()

    def create_primary_admins(self):
        result = self.RootsModel.create_primary_admins()
        return True

@roots_router.put("/create_primary_admins")
def create_primary_admins():
    return Roots().create_primary_admins()