from ..base.pSQL.objects import MerchStoreModel
from fastapi import APIRouter, Body, Request

from ..model import User
from .Auth import AuthService

from .SendMail import SendEmail

from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

import asyncio

store_router = APIRouter(prefix="/store", tags=["Магазин мерча"])


class MerchStore:
    def __init__(self, user_uuid: int = 0):
        self.user_uuid = user_uuid

    async def create_purchase(self, data, session):
        res = await MerchStoreModel(user_id=self.user_uuid).create_purchase(data=data, session=session)
        if "not_enough" in res:
            return res
        #отправляем письмо о покупке res = f"{merch_info.name}, Куплено {total_count} штук(а)"\
        if 'status' in res:
            return res
        user_sql = await User(id=self.user_uuid).search_by_id(session=session)
        mail_data = {
            'sender': user_sql['email'],
            'items': res,
            'user_info': f'ID={user_sql['id']}, ФИО = {user_sql['last_name']} {user_sql['name']} {user_sql['second_name']}'
        }
        SendEmail(data=mail_data).send_active_purchase()
        return True
    
    async def buy_split(self, data, session):
        res = await MerchStoreModel(user_id=self.user_uuid).buy_split(data=data, session=session)
        #отправляем письмо о покупке res = f"{merch_info.name}, Куплено {total_count} штук(а)"
        if 'status' in res:
            return res
        user_sql = await User(id=self.user_uuid).search_by_id(session=session)
        mail_data = {
            'sender': user_sql['email'],
            'items': res,
            'user_info': f'ID={user_sql['id']}, ФИО = {user_sql['last_name']} {user_sql['name']} {user_sql['second_name']}'
        }
        SendEmail(data=mail_data).send_active_purchase()
        return True




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

@store_router.put("/create_purchase")
async def create_purchase(user_id: int = Depends(get_user_id_by_session_id), data=Body(), session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    # if user_id is None:
    #     user_id = 2366
    return await MerchStore(user_id).create_purchase(data=data, session=session)

@store_router.put("/buy_split")
async def buy_split(user_id: int = Depends(get_user_id_by_session_id), data=Body(), session: AsyncSession = Depends(get_async_db)):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    # if user_id is None:
    #     user_id = 2366
    return await MerchStore(user_id).buy_split(data=data, session=session)