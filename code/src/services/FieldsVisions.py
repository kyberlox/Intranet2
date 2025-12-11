from ..base.pSQL.objects import FieldvisionModel, UservisionsRootModel, RootsModel
from ..base.Elastic.StuctureSearchmodel import StructureSearchModel
from .LogsMaker import LogsMaker

from .Auth import AuthService
from ..model.User import User
# from fastapi import APIRouter

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

import asyncio

from fastapi import APIRouter, Request, Body

# from fastapi.responses import HTMLResponse
# from jinja2 import Environment, FileSystemLoader
# import json

fieldsvisions_router = APIRouter(prefix="/fields_visions", tags=["Сервис области видимости"])


class Visions:
    def __init__(self, vision_name: str = '', vision_id: int = 0, user_id: int = 0, art_id: int = 0):
        self.vision_name = vision_name
        self.vision_id = vision_id
        self.user_id = user_id
        self.art_id = art_id

        # self.Roots = RootsModel(user_uuid=self.user_id).get_token_by_uuid()
        # self.roots = RootsModel(user_uuid=self.user_id).token_processing_for_vision(self.Roots)

    async def get_full_structure(self):
        return StructureSearchModel().get_full_structure()

    async def get_dep_structure(self, parent_id):
        return StructureSearchModel().get_structure_by_parent_id(parent_id)

    async def get_dep_structure_by_name(self, name):
        return StructureSearchModel().get_structure_by_name(name)

    async def create_new_vision(self, session):
        return await FieldvisionModel(vision_name=self.vision_name).add_field_vision(session=session)

    async def get_vision_by_id(self, session):
        return await FieldvisionModel(id=self.vision_id).find_vision_by_id(session=session)

    async def delete_vision(self, session):
        users = await self.get_users_in_vision(session)
        users_id = [usr['id'] for usr in users]
        root_init = RootsModel(user_uuid=self.user_id)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_vision(roots_uuid)
        await FieldvisionModel(id=self.vision_id).remove_field_vision(session=session)
        await UservisionsRootModel(vision_id=self.vision_id).remove_users_from_vision(user_data=users_id, roots=roots,
                                                                                      session=session)
        # self.delete_users_from_vision(users=users_id)
        return True

    async def get_all_visions(self, session):
        return await FieldvisionModel().find_all_visions(session=session)

    async def add_user_to_vision(self, user_to, session):
        root_init = RootsModel(user_uuid=self.user_id)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_vision(roots_uuid)
        return await UservisionsRootModel(vision_id=self.vision_id, user_id=user_to).upload_user_to_vision(roots=roots,
                                                                                                           session=session)

    async def add_full_usdep_list_to_vision(self, dep_id, session):
        all_dep_users = []
        if dep_id == 53:
            dep = await self.get_dep_structure(dep_id)
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
            dep = await self.get_dep_structure(dep_id)
            for de in dep:
                for user in de['users']:
                    all_dep_users.append(user['id'])
        root_init = RootsModel(user_uuid=self.user_id)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_vision(roots_uuid)
        return await UservisionsRootModel(vision_id=self.vision_id).upload_users_to_vision(roots=roots,
                                                                                           user_data=all_dep_users,
                                                                                           session=session)

    async def add_dep_users_only(self, dep_id, session):
        all_dep_users = []
        dep = await self.get_dep_structure(dep_id)
        for de in dep:
            if de['id'] == dep_id:
                for user in de['users']:
                    all_dep_users.append(user['id'])
                break
            else:
                pass
        root_init = RootsModel(user_uuid=self.user_id)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_vision(roots_uuid)
        return await UservisionsRootModel(vision_id=self.vision_id).upload_users_to_vision(roots=roots,
                                                                                           user_data=all_dep_users,
                                                                                           session=session)

    async def add_users_list_to_vision(self, users, session):
        root_init = RootsModel(user_uuid=self.user_id)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_vision(roots_uuid)
        return await UservisionsRootModel(vision_id=self.vision_id).upload_users_to_vision(user_data=users, roots=roots,
                                                                                           session=session)

    async def delete_user_from_vision(self, user, session):
        root_init = RootsModel(user_uuid=self.user_id)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_vision(roots_uuid)
        return await UservisionsRootModel(vision_id=self.vision_id, user_id=user).remove_user_from_vision(roots=roots,
                                                                                                          session=session)

    async def delete_users_from_vision(self, users, session):
        root_init = RootsModel(user_uuid=self.user_id)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_vision(roots_uuid)
        return await UservisionsRootModel(vision_id=self.vision_id).remove_users_from_vision(user_data=users,
                                                                                             roots=roots,
                                                                                             session=session)

    async def get_users_in_vision(self, session):
        return await UservisionsRootModel(vision_id=self.vision_id).find_users_in_vision(session=session)

    async def remove_depart_in_vision(self, dep_id, session):
        root_init = RootsModel(user_uuid=self.user_id)
        roots_uuid = await root_init.get_token_by_uuid(session=session)
        roots = await root_init.token_processing_for_vision(roots_uuid)
        return await UservisionsRootModel(vision_id=self.vision_id).remove_depart_in_vision(dep_id=dep_id, roots=roots,
                                                                                            session=session)

    async def set_art_to_vision(self, session):
        return await FieldvisionModel(id=self.vision_id, art_id=self.art_id).set_art_to_vision(session=session)

    async def delete_art_from_vision(self, session):
        return await FieldvisionModel(id=self.vision_id, art_id=self.art_id).delete_art_from_vision(session=session)

    async def get_all_vis_in_art(self, session):
        return await FieldvisionModel(art_id=self.art_id).get_all_vis_in_art(session=session)

    async def check_user_root(self, session):
        return await FieldvisionModel(art_id=self.art_id).check_user_root(user_id=self.user_id, session=session)


async def get_uuid_from_request(request, session):
    session_id = ""
    token = request.cookies.get("session_id")
    if token is None:
        token = request.headers.get("session_id")
        if token is not None:
            session_id = token
    else:
        session_id = token

    user = dict(AuthService().get_user_info(session_id))

    if user is not None:
        user_id = user["ID"]

        # получить и вывести его id
        usr = User()
        usr.id = user_id
        user_inf = await usr.search_by_id(session=session)
        if user_inf is not None and "ID" in user_inf.keys():
            return user_inf["id"]
    return None


@fieldsvisions_router.get("/get_full_structure")
async def get_full_structure():
    return await Visions().get_full_structure()


@fieldsvisions_router.get("/get_dep_structure/{parent_id}")
async def get_dep_structure(parent_id: int):
    return await Visions().get_dep_structure(parent_id)


@fieldsvisions_router.get("/get_dep_structure_by_name/{word}")
async def get_dep_structure_by_name(word: str):
    return await Visions().get_dep_structure_by_name(word)


@fieldsvisions_router.get("/get_all_visions")
async def get_all_visions(session: AsyncSession = Depends(get_async_db)):
    return await Visions().get_all_visions(session)


@fieldsvisions_router.put("/create_new_vision/{vision_name}")
async def create_new_vision(vision_name: str, session: AsyncSession = Depends(get_async_db)):
    return await Visions(vision_name).create_new_vision(session)


@fieldsvisions_router.delete("/delete_vision/{vision_id}")
async def delete_vision(request: Request, vision_id: int, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(vision_id=vision_id, user_id=uuid).delete_vision(session)


@fieldsvisions_router.put("/add_user_to_vision/{vision_id}/{user_id}")
async def add_user_to_vision(request: Request, vision_id: int, user_id: int,
                             session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(vision_id=vision_id, user_id=uuid).add_user_to_vision(user_to=user_id, session=session)


@fieldsvisions_router.put("/add_dep_users_only/{vision_id}/{dep_id}")
async def add_dep_users_only(request: Request, vision_id: int, dep_id: int,
                             session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(vision_id=vision_id, user_id=uuid).add_dep_users_only(dep_id=dep_id, session=session)


@fieldsvisions_router.put("/add_full_usdep_list_to_vision/{vision_id}/{dep_id}")
async def add_full_usdep_list_to_vision(request: Request, vision_id: int, dep_id: int,
                                        session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(vision_id=vision_id, user_id=uuid).add_full_usdep_list_to_vision(dep_id=dep_id,
                                                                                          session=session)


@fieldsvisions_router.put("/add_users_list_to_vision/{vision_id}")
async def add_users_list_to_vision(request: Request, vision_id: int, users=Body(),
                                   session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(vision_id=vision_id, user_id=uuid).add_users_list_to_vision(users=users, session=session)


@fieldsvisions_router.delete("/delete_user_from_vision/{vision_id}/{user_id}")
async def delete_user_from_vision(request: Request, vision_id: int, user_id: int,
                                  session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(vision_id=vision_id, user_id=uuid).delete_user_from_vision(user=user_id, session=session)


@fieldsvisions_router.delete("/delete_users_from_vision/{vision_id}")
async def delete_users_from_vision(request: Request, vision_id: int, users=Body(),
                                   session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(vision_id=vision_id, user_id=uuid).delete_users_from_vision(users=users, session=session)


@fieldsvisions_router.get("/get_users_in_vision/{vision_id}")
async def get_users_in_vision(request: Request, vision_id: int, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(vision_id=vision_id, user_id=uuid).get_users_in_vision(session=session)


@fieldsvisions_router.delete("/remove_depart_in_vision/{vision_id}/{dep_id}")
async def remove_depart_in_vision(request: Request, vision_id: int, dep_id: int,
                                  session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(vision_id=vision_id, user_id=uuid).remove_depart_in_vision(dep_id=dep_id, session=session)


@fieldsvisions_router.put("/set_art_to_vision/{art_id}/{vis_id}")
async def set_art_to_vision(art_id: int, vis_id: int, session: AsyncSession = Depends(get_async_db)):
    return await Visions(vision_id=vis_id, art_id=art_id).set_art_to_vision(session=session)


@fieldsvisions_router.delete("/delete_art_from_vision/{art_id}/{vis_id}")
async def delete_art_from_vision(art_id: int, vis_id: int, session: AsyncSession = Depends(get_async_db)):
    return await Visions(vision_id=vis_id, art_id=art_id).delete_art_from_vision(session=session)


@fieldsvisions_router.get("/get_all_vis_in_art/{art_id}")
async def get_all_vis_in_art(art_id: int, session: AsyncSession = Depends(get_async_db)):
    return await Visions(art_id=art_id).get_all_vis_in_art(session=session)


@fieldsvisions_router.get("/check_user_root/{art_id}")
async def check_user_root(request: Request, art_id: int, session: AsyncSession = Depends(get_async_db)):
    uuid = await get_uuid_from_request(request, session)
    return await Visions(art_id=art_id, user_id=uuid).check_user_root(session=session)