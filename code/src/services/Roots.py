from fastapi import APIRouter, Request
from .LogsMaker import LogsMaker
from ..model.User import User
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

import asyncio

roots_router = APIRouter(prefix="/roots", tags=["Права пользователя"])


class Roots:
    def __init__(self, user_uuid=0):
        from ..base.pSQL.objects.RootsModel import RootsModel
        self.RootsModel = RootsModel()

        self.user_uuid = user_uuid

    async def create_primary_admins(self, session):
        result = await self.RootsModel.create_primary_admins(session=session)
        return {"status": True}

    async def create_editor_moder(self, sec_id, session):
        self.RootsModel.user_uuid = self.user_uuid
        res = await self.RootsModel.create_editor_moder(sec_id, session=session)
        return res

    async def delete_editor_moder(self, sec_id, session):
        self.RootsModel.user_uuid = self.user_uuid
        res = await self.RootsModel.delete_editor_moder(sec_id, session=session)
        return res

    async def create_editor_admin(self, session):
        self.RootsModel.user_uuid = self.user_uuid
        res = await  self.RootsModel.create_editor_admin(session=session)
        return res

    async def delete_editor_admin(self, session):
        self.RootsModel.user_uuid = self.user_uuid
        res = await  self.RootsModel.delete_editor_admin(session=session)
        return res

    async def get_editors_list(self, sec_id, session):
        res = await  self.RootsModel.get_editors_list(sec_id, session=session)
        return res

    async def get_token_by_uuid(self, session):
        self.RootsModel.user_uuid = self.user_uuid
        res = await  self.RootsModel.get_token_by_uuid(session=session)
        return res

    async def token_processing_for_editor(self, roots):
        self.RootsModel.user_uuid = self.user_uuid
        res = await  self.RootsModel.token_processing_for_editor(roots)
        return res


async def get_uuid_from_request(request, session):
    # user_id = None
    user_id = request.cookies.get("user_id")

    print(user_id, 'ВОЗЬМИСЬ!', type(user_id))
    if user_id is not None:
        # user_id = user["ID"]
        print('*')
        # получить и вывести его id
        usr = User()
        print('*')
        usr.id = int(user_id)
        print('*')
        user_inf = await usr.search_by_id(session=session)
        print('*')
        if user_inf is not None and "ID" in user_inf.keys():
            print('12343254')
            return user_inf["id"]
    return None


async def get_editor_roots(user_uuid, session):
    roots_model = Roots()
    roots_model.user_uuid = user_uuid
    all_roots = await roots_model.get_token_by_uuid(session=session)
    editor_roots = await roots_model.token_processing_for_editor(all_roots)
    return editor_roots


@roots_router.put("/create_primary_admins")
async def create_primary_admins(session: AsyncSession = Depends(get_async_db)):
    return await Roots().create_primary_admins(session=session)


@roots_router.put("/create_editor_moder/{user_uuid}/{sec_id}")
async def create_editor_moder(user_uuid: int, sec_id: int, request: Request,
                              session: AsyncSession = Depends(get_async_db)):
    user_id = await get_uuid_from_request(request, session=session)
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots(user_uuid=user_uuid).create_editor_moder(sec_id, session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.delete("/delete_editor_moder/{user_uuid}/{sec_id}")
async def delete_editor_moder(user_uuid: int, sec_id: int, request: Request,
                              session: AsyncSession = Depends(get_async_db)):
    user_id = await get_uuid_from_request(request, session=session)
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots(user_uuid=user_uuid).delete_editor_moder(sec_id, session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.put("/create_editor_admin/{user_uuid}")
async def create_editor_admin(user_uuid: int, request: Request, session: AsyncSession = Depends(get_async_db)):
    user_id = await get_uuid_from_request(request, session=session)
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots(user_uuid=user_uuid).create_editor_admin(session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.delete("/delete_editor_admin/{user_uuid}")
async def delete_editor_admin(user_uuid: int, request: Request, session: AsyncSession = Depends(get_async_db)):
    user_id = await get_uuid_from_request(request, session=session)
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots(user_uuid=user_uuid).delete_editor_admin(session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.get("/get_editors_list/{sec_id}")
async def get_editors_list(sec_id: int, request: Request, session: AsyncSession = Depends(get_async_db)):
    user_id = await get_uuid_from_request(request, session=session)
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots().get_editors_list(sec_id, session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.get("/get_root_token_by_uuid")
async def get_token_by_uuid(request: Request, session: AsyncSession = Depends(get_async_db)):
    user_id = await get_uuid_from_request(request, session=session)
    print(user_id)
    user_roots = await Roots(user_uuid=user_id).get_token_by_uuid(session=session)
    return user_roots
