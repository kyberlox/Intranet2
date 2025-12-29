from fastapi import APIRouter
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from ..model.User import User

import requests

ai_router = APIRouter(prefix="/ai", tags=["AI"])

class Dialog(BaseModel):
    ID : str
    name: str
    user_uuid: str
    messages: list

class History:
    def __init__(self, user_id):
        self.user_id = user_id
        self.dialog = Dialog()
    
    #получить диалоги по uuid

    #получить диалог

    #переименовать диалог

    #создать диалог

    #изменить диалог (добавить сообщение)

    #удалить диалог

class GPT:
    def __init__(self ):
        self.token = "0WnS5hZAYRDpVP7NMTl^n8@XRxYEO4lR"
    
    def send_to_gpt(self, messages):
        #проверить доступ
        #проксировать запросы
        pass