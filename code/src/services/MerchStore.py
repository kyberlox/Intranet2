from ..base.pSQL.objects import MerchStoreModel
from fastapi import APIRouter, Body, Request

from ..model import User
from .Auth import AuthService

from .SendMail import SendEmail

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

import asyncio

store_router = APIRouter(prefix="/store", tags=["Магазин мерча"])


class MerchStore:
    def __init__(self, user_uuid: int = 0):
        self.user_uuid = user_uuid

    async def create_purchase(self, data, session):
        res = await MerchStoreModel(user_id=self.user_uuid).create_purchase(data=data, session=session)
        #отправляем письмо о покупке res = f"{merch_info.name}, Куплено {total_count} штук(а)"
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


@store_router.put("/create_purchase")
async def create_purchase(request: Request, data=Body(), session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    if user_uuid is None:
        user_uuid = 2366
    return await MerchStore(user_uuid).create_purchase(data=data, session=session)