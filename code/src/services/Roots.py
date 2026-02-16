from fastapi import APIRouter, Request, Body
from .LogsMaker import LogsMaker
from ..model.User import User
from fastapi import Depends, status, HTTPException
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

    async def get_token_by_id(self, session):
        self.RootsModel.user_uuid = self.user_uuid
        res = await self.RootsModel.get_token_by_id(session=session)
        return res

    async def token_processing_for_editor(self, roots):
        self.RootsModel.user_uuid = self.user_uuid
        res = await self.RootsModel.token_processing_for_editor(roots)
        return res

    async def give_gpt_gen_license(self, session):
        self.RootsModel.user_uuid = self.user_uuid
        res = await self.RootsModel.give_gpt_gen_license(session)
        return res
    
    async def stop_gpt_gen_license(self, session):
        self.RootsModel.user_uuid = self.user_uuid
        res = await self.RootsModel.stop_gpt_gen_license(session)
        return res
    
    async def get_gpt_gen_licenses(self, session):
        res = await self.RootsModel.gpt_gen_lic(session)
        return res




async def get_uuid_from_request(request, session):
    # user_id = None
    user_id = request.cookies.get("user_id") or request.headers.get("user_id")
    if user_id is not None:
        usr = User()
        usr.id = int(user_id)
        user_inf = await usr.search_by_id(session=session)
        if user_inf is not None and "id" in user_inf.keys():
            return user_inf["id"]
    return None


async def get_editor_roots(user_uuid, session):
    roots_model = Roots()
    roots_model.user_uuid = user_uuid
    all_roots = await roots_model.get_token_by_uuid(session=session)
    editor_roots = await roots_model.token_processing_for_editor(all_roots)
    if user_uuid is None:
        print('ФОРМИРУЕМ ЕМУ СЛОВАРЬ КОГСТЫЛЬ')
        editor_roots = {'EditorAdmin': True, 'EditorModer': [31, 33], 'VisionAdmin': True, 'GPT_gen_access': True}
    # 'PeerAdmin': True, 'PeerModer': True, 'PeerCurator': [], 
    return editor_roots

# Dependency для получения айдишника пользователя
async def get_user_id_by_session_id(request: Request) -> int:
    from ..base.RedisStorage import RedisStorage
    """Получение текущей сессии пользователя"""
    # Ищем session_id в куках или заголовках
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        auth_header = request.headers.get("session_id")
        if auth_header:# and auth_header.startswith("Bearer "):
            session_id = auth_header#[7:]
    
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    session_data = RedisStorage().get_session(key=session_id)

    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_id = session_data['user_info']['ID']
    return user_id

@roots_router.put("/create_primary_admins")
async def create_primary_admins(session: AsyncSession = Depends(get_async_db)):
    return await Roots().create_primary_admins(session=session)


@roots_router.put("/create_editor_moder/{user_uuid}/{sec_id}")
async def create_editor_moder(user_uuid: int, sec_id: int, user_id: int = Depends(get_user_id_by_session_id),
                              session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots(user_uuid=user_uuid).create_editor_moder(sec_id, session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.delete("/delete_editor_moder/{user_uuid}/{sec_id}")
async def delete_editor_moder(user_uuid: int, sec_id: int, user_id: int = Depends(get_user_id_by_session_id),
                              session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots(user_uuid=user_uuid).delete_editor_moder(sec_id, session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.put("/create_editor_admin/{user_uuid}")
async def create_editor_admin(user_uuid: int, user_id: int = Depends(get_user_id_by_session_id), session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots(user_uuid=user_uuid).create_editor_admin(session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.delete("/delete_editor_admin/{user_uuid}")
async def delete_editor_admin(user_uuid: int, user_id: int = Depends(get_user_id_by_session_id), session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots(user_uuid=user_uuid).delete_editor_admin(session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.get("/get_editors_list/{sec_id}")
async def get_editors_list(sec_id: int, user_id: int = Depends(get_user_id_by_session_id), session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots().get_editors_list(sec_id, session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")


@roots_router.get("/get_root_token_by_uuid")
async def get_token_by_uuid(user_id: int = Depends(get_user_id_by_session_id), session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_roots = await Roots(user_uuid=user_id).get_token_by_uuid(session=session)
    if user_id is None:
        print('ФОРМИРУЕМ ЕМУ СЛОВАРЬ КОГСТЫЛЬ')
        user_roots = {'PeerAdmin': True, 'EditorAdmin': True, 'EditorModer': [31, 33], 'VisionAdmin': True, 'GPT_gen_access': True}
        # user_roots = {}
    # 'PeerAdmin': True, 'PeerModer': True, 'PeerCurator': [], 
    return user_roots


@roots_router.put("/give_gpt_gen_license")
async def give_gpt_gen_license(user_id: int = Depends(get_user_id_by_session_id), session: AsyncSession = Depends(get_async_db), users_list: list = Body()):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        for user in users_list:
            await Roots(user_uuid=int(user)).give_gpt_gen_license(session=session)
        return True
    return LogsMaker().warning_message(f"Недостаточно прав")

@roots_router.delete("/stop_gpt_gen_license/{user_uuid}")
async def stop_gpt_gen_license(user_id: int = Depends(get_user_id_by_session_id), user_uuid: int, session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots(user_uuid=user_uuid).stop_gpt_gen_license(session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")

@roots_router.get("/get_gpt_gen_licenses")
async def gpt_gen_licenses(user_id: int = Depends(get_user_id_by_session_id), session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    editor_roots = await get_editor_roots(user_id, session=session)
    if "EditorAdmin" in editor_roots.keys() and editor_roots["EditorAdmin"] == True:
        return await Roots().get_gpt_gen_licenses(session=session)
    return LogsMaker().warning_message(f"Недостаточно прав")