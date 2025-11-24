from ..base.pSQL.objects import MerchStoreModel
from fastapi import APIRouter, Body, Request

from ..model import User
from .Auth import AuthService

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

import asyncio

store_router = APIRouter(prefix="/store", tags=["Магазин мерча"])


class MerchStore:
    def __init__(self, user_uuid: int = 0):
        self.user_uuid = user_uuid

    async def create_purchase(self, data, session):
        return await MerchStoreModel(user_id=self.user_uuid).create_purchase(data=data, session=session)


async def get_uuid_from_request(request, session):
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

        # получить и вывести его id
        user_inf = await User(uuid=user_uuid).user_inf_by_uuid(session)
        return user_inf["ID"]
    return None


@store_router.put("/create_purchase")
async def create_purchase(request: Request, data=Body(), session: AsyncSession = Depends(get_async_db)):
    user_uuid = await get_uuid_from_request(request, session)
    return await MerchStore(user_uuid).create_purchase(data=data, session=session)