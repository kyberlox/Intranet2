# from ..base.pSQL.objects import ActivitiesModel, ActiveUsersModel, RootsModel, PeerUserModel
from fastapi import APIRouter, Body, Request

from ..model import User
from .Auth import AuthService

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

import asyncio

# тут придется отладить ВСЕ

peer_router = APIRouter(prefix="/peer", tags=["Сервис системы эффективности"])


class Peer:
    def __init__(self, id: int = 0, name: str = '', coast: int = 0, user_uuid: int = 0, need_valid: bool = False,
                 active: bool = False, activities_id: int = 0):
        self.id = id
        self.name = name
        self.coast = coast
        self.user_uuid = user_uuid
        self.need_valid = need_valid
        self.active = active
        self.activities_id = activities_id

        from ..base.pSQL.objects.ActivitiesModel import ActivitiesModel
        self.ActivitiesModel = ActivitiesModel()

        from ..base.pSQL.objects.ActiveUsersModel import ActiveUsersModel
        self.ActiveUsersModel = ActiveUsersModel()

        from ..base.pSQL.objects.RootsModel import RootsModel
        self.RootsModel = RootsModel()

        from ..base.pSQL.objects.PeerUserModel import PeerUserModel
        self.PeerUserModel = PeerUserModel()

        # self.RootsModel.user_uuid = self.user_uuid
        # self.Roots = self.RootsModel.get_token_by_uuid()
        # self.roots = self.RootsModel.token_processing_for_peer(self.Roots)

    """Ручки которые доступны любому пользователю"""

    async def sum(self, session):
        result = await self.ActiveUsersModel.sum(uuid=self.user_uuid, session=session)
        return result

    async def statistics(self, session):
        self.ActiveUsersModel.uuid_to = self.user_uuid
        return await self.ActiveUsersModel.statistics(session)

    async def actions(self, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        result = await self.ActiveUsersModel.actions(session=session, roots=roots)
        return result

    """"""

    async def get_all_activities(self, session):
        result = await self.ActivitiesModel.find_all_activities(session=session)
        return result

    # async def upload_base_activities(self):
    #     return self.ActivitiesModel.upload_base_activities()

    async def edit_activity(self, session):
        self.ActivitiesModel.id = self.id
        self.ActivitiesModel.name = self.name
        self.ActivitiesModel.coast = self.coast
        self.ActivitiesModel.need_valid = self.need_valid
        self.ActivitiesModel.active = self.active
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        return await self.ActivitiesModel.update_activity(roots=roots, session=session)

    async def remove_activity(self, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.ActivitiesModel.id = self.id
        return await self.ActivitiesModel.delete_activity(roots=roots, session=session)

    """"""

    async def do_valid(self, action_id, uuid_to, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.uuid = self.user_uuid
        return await self.PeerUserModel.do_valid(session=session, action_id=action_id, uuid_to=uuid_to, roots=roots)

    async def do_not_valid(self, action_id, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.uuid = self.user_uuid
        return await self.PeerUserModel.do_not_valid(session=session, action_id=action_id, roots=roots)

    async def points_to_confirm(self, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.activities_id = self.activities_id
        return await self.PeerUserModel.points_to_confirm(session=session, roots=roots)

    async def get_curators(self, session):
        return await self.PeerUserModel.get_curators(session=session)

    async def add_curator(self, user_id, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.activities_id = self.activities_id
        self.PeerUserModel.uuid = user_id
        return await self.PeerUserModel.add_curator(session=session, roots=roots)

    async def delete_curator(self, user_id, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.activities_id = self.activities_id
        self.PeerUserModel.uuid = user_id
        result = await self.PeerUserModel.delete_curator(session=session, roots=roots)
        return result

    async def new_activity(self, data, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        # data["uuid"] = self.user_uuid
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if roots_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        return await self.ActivitiesModel.new_activity(data=data, roots=roots, session=session)

    """"""

    # async def upload_past_activeusers(self):
    #     return self.ActiveUsersModel().upload_past_table_ActiveUsers()

    # async def history_mdr(self, activity_name):
    #     return self.ActiveUsersModel().history_mdr(activity_name)

    # async def top(self):
    #     return self.ActiveUsersModel().top()

    # async def my_place(self):
    #     return self.ActiveUsersModel(uuid_to=self.user_uuid).my_place()

    # async def statistics_history(self):
    #     return self.ActiveUsersModel(uuid_to=self.user_uuid, activities_id=self.activities_id).statistics_history()

    # async def new_a_week(self):
    #     return self.ActiveUsersModel(uuid_to=self.user_uuid).new_a_week()

    async def user_history(self, session):
        self.ActiveUsersModel.uuid_to = self.user_uuid
        return await self.ActiveUsersModel.user_history(session=session)

    """"""

    async def send_points(self, data, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        return await self.PeerUserModel.send_points(data=data, roots=roots, session=session)
    
    async def send_auto_points(self, data, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        return await self.PeerUserModel.send_auto_points(data=data, roots=roots, session=session)


    async def get_admins_list(self, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        return await self.PeerUserModel.get_admins_list(session=session, roots=roots)

    async def add_peer_admin(self, uuid, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.uuid = uuid
        return await self.PeerUserModel.add_peer_admin(roots=roots, session=session)

    async def delete_admin(self, uuid, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.uuid = uuid
        return await self.PeerUserModel.delete_admin(session=session, roots=roots)

    async def get_moders_list(self, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        return await self.PeerUserModel.get_moders_list(roots=roots, session=session)

    async def add_peer_moder(self, uuid, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.uuid = uuid
        return await self.PeerUserModel.add_peer_moder(roots=roots, session=session)

    async def delete_peer_moder(self, uuid, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.uuid = uuid
        return await self.PeerUserModel.delete_peer_moder(roots=roots, session=session)

    async def get_curators_history(self, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        return await self.PeerUserModel.get_curators_history(roots=roots, session=session)

    async def return_points_to_user(self, note_id, user_uuid, session):
        return await self.PeerUserModel.return_points_to_user(session=session, note_id=note_id, user_uuid=user_uuid)

    async def remove_user_points(self, action_id, user_uuid, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        self.PeerUserModel.uuid = user_uuid
        return await self.PeerUserModel.remove_user_points(action_id=action_id, roots=roots, session=session)
    
    async def send_points_to_employee_of_the_year(self, session):
        from ..base.pSQL.objects.RootsModel import RootsModel
        root_init = RootsModel(user_uuid=self.user_uuid)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_peer(roots_uuid)
        if self.user_uuid is None:
            roots = {'user_id': 2366, 'EditorAdmin': True, "PeerAdmin": True}
        return await self.PeerUserModel.send_points_to_employee_of_the_year(roots=roots, session=session)
    
    async def send_points_to_realized_idea(self, session, user_id, name_idea):
        return await self.PeerUserModel.send_points_to_realized_idea(name_idea=name_idea, user_id=user_id, session=session)



async def get_uuid_from_request(request, session):
    user_id = None
    token = request.cookies.get("user_id")
    if token is None:
        token = request.headers.get("user_id")
        if token is not None:
            user_id = token
    else:
        user_id = token

    if user_id is not None:

        # получить и вывести его id
        usr = User()
        usr.id = int(user_id)
        user_inf = await usr.search_by_id(session=session)
        if user_inf is not None and "id" in user_inf.keys():
            return user_inf["id"]
    return None


# # дампит старые данные
# @peer_router.put("/put_tables")
# async def load_activities():
#     Peer().upload_base_activities()
#     Peer().upload_past_moders()
#     Peer().upload_past_activeusers()
#     return {"status": True}

"""Ручки которые доступны любому пользователю"""


@peer_router.get("/sum")
async def sum(request: Request, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    if uuid is None:
        uuid = 2366
    return await Peer(user_uuid=uuid).sum(session)


# @peer_router.get("/statistics")
# async def statistics(request: Request):
#     uuid = get_uuid_from_request(request)
#     return Peer(user_uuid=uuid).statistics()

@peer_router.get("/actions")
async def get_actions(request: Request, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    if uuid is None:
        uuid = 2366
    return await Peer(user_uuid=uuid).actions(session)


""""""


@peer_router.get("/get_all_activities")
async def get_activities(session: AsyncSession = Depends(get_async_db)):
    return await Peer().get_all_activities(session)


@peer_router.post("/edit_activity")
async def post_edit_activity(request: Request, session: AsyncSession = Depends(get_async_db), data=Body()):
    uuid = await get_uuid_from_request(request, session)
    if uuid is None:
        uuid = 2366
    return await Peer(user_uuid=uuid, id=data['id'], name=data['name'], coast=data['coast'],
                      need_valid=data['need_valid'], active=data['active']).edit_activity(session)


@peer_router.delete("/remove_activity/{id}")
async def del_remove_activity(request: Request, id: str, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    if uuid is None:
        uuid = 2366
    res = await Peer(id=id, user_uuid=uuid).remove_activity(session)
    await session.commit()
    return res


""""""


@peer_router.post("/do_valid/{action_id}/{uuid_to}")
async def post_do_valid(request: Request, action_id: int, uuid_to: int, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    if uuid is None:
        uuid = 2366
    return await Peer(user_uuid=uuid).do_valid(action_id=action_id, uuid_to=uuid_to, session=session)


@peer_router.post("/do_not_valid/{action_id}")
async def post_do_not_valid(request: Request, action_id: int, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    if uuid is None:
        uuid = 2366
    return await Peer(user_uuid=uuid).do_not_valid(action_id=action_id, session=session)


@peer_router.get("/points_to_confirm/{activities_id}")
async def get_points_to_confirm(request: Request, activities_id: int, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    if uuid is None:
        uuid = 2366

    return await Peer(activities_id=activities_id, user_uuid=uuid).points_to_confirm(session)


@peer_router.get("/get_curators")
async def get_req_curators(session: AsyncSession = Depends(get_async_db)):
    return await Peer().get_curators(session)


@peer_router.put("/add_curator/{uuid}/{activities_id}")
async def add_curator(uuid: int, request: Request, activities_id: int, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid, activities_id=activities_id).add_curator(user_id=uuid, session=session)


@peer_router.delete("/delete_curator/{uuid}/{activities_id}")
async def delete_curator(uuid: int, request: Request, activities_id: int,
                         session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    res = await Peer(user_uuid=user_uuid, activities_id=activities_id).delete_curator(user_id=uuid, session=session)
    await session.commit()
    return res


@peer_router.put("/new_activity")
async def put_new_activity(request: Request, data=Body(), session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    if uuid is None:
        uuid = 2366
    return await Peer(user_uuid=uuid).new_activity(data=data,session=session)  # {"name": str, "coast": int, "need_valid": bool, "uuid": str("*" или "4133")}


""""""


# @peer_router.get("/history_mdr/{activity_name}")
# async def history_mdr(activity_name: str):
#     return Peer().history_mdr(activity_name)

# @peer_router.get("/statistics_history/{activities_id}/{uuid}")
# async def statistics_history(activities_id: int, uuid: int):
#     return Peer(activities_id=activities_id, user_uuid=uuid).statistics_history()

# @peer_router.get("/top")
# async def top():
#     return Peer().top()

# @peer_router.get("/my_place/{uuid}")
# async def my_place(uuid: int):
#     return Peer(user_uuid=uuid).my_place()

# @peer_router.get("/new_a_week/{uuid}")
# async def new_a_week(uuid: int):
#     return Peer(user_uuid=uuid).new_a_week()

@peer_router.get("/user_history")
async def user_history(request: Request, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    if uuid is None:
        uuid = 2366
    return await Peer(user_uuid=uuid).user_history(session=session)


""""""


@peer_router.put("/send_points")
async def send_points(request: Request, data=Body(), session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).send_points(data=data,
                                                       session=session)  # {"uuid_to": "2375", "activities_id": 0, "description": "Крутой тип"}


@peer_router.get("/get_admins_list")
async def get_admins_list(request: Request, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).get_admins_list(session=session)


@peer_router.put("/add_peer_admin/{uuid}")
async def add_peer_admin(uuid: int, request: Request, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).add_peer_admin(uuid=uuid, session=session)


@peer_router.delete("/delete_admin/{uuid}")
async def delete_admin(uuid: str, request: Request, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).delete_admin(uuid=uuid, session=session)


@peer_router.get("/get_moders_list")
async def get_moders_list(request: Request, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).get_moders_list(session)


@peer_router.put("/add_peer_moder/{uuid}")
async def add_peer_moder(uuid: int, request: Request, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).add_peer_moder(uuid=uuid, session=session)


@peer_router.delete("/delete_peer_moder/{uuid}")
async def delete_peer_moder(uuid: str, request: Request, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).delete_peer_moder(uuid=uuid, session=session)


@peer_router.get("/get_curators_history")
async def get_curators_history(request: Request, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).get_curators_history(session=session)


@peer_router.post("/return_points_to_user/{user_uuid}/{note_id}")
async def return_points_to_user(user_uuid: int, note_id: int, session: AsyncSession = Depends(get_async_db)):
    return await Peer().return_points_to_user(note_id=note_id, user_uuid=user_uuid, session=session)


@peer_router.post("/remove_user_points/{uuid}/{action_id}")
async def remove_user_points(request: Request, uuid: int, action_id: int,
                             session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).remove_user_points(action_id=action_id, user_uuid=uuid, session=session)

@peer_router.post("/send_points_to_employee_of_the_year")
async def send_points_to_employee_of_the_year(request: Request, session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await Peer(user_uuid=user_uuid).send_points_to_employee_of_the_year(session=session)