from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.base.B24 import B24
from src.services.Auth import AuthService
from src.model.User import User

import json


def take_value(PROPERTY):
    if type(PROPERTY) == type(dict()):
        return list(PROPERTY.values())[0]
    elif type(PROPERTY) == type(list()):
        return PROPERTY[0]
    else:
        return None

class Idea:
    def __init__(self, user_id=None, user_uuid=None):
        #беру идеи из битры
        b24_ideas = B24().getInfoBlock(121)

        ideas = []
        #каждую идею
        for idea in b24_ideas:
            #проебразую по шаблону с нормальными ключами
            prop_keys = {
                "ID" : "id",
                "NAME" : "name",
                "CREATED_BY" : "user_id",
                "CREATED_USER_NAME" : "username",
                "DETAIL_TEXT" : "content",
                "DETAIL_TEXT_TYPE" : "content_type",
                "DATE_CREATE" : "date_create",
                "PROPERTY_1049" : "number",
                "PROPERTY_1117" : "status",
            }

            cool_idea = dict()
            for prop in prop_keys.keys():
                
                val = None
                if prop in idea:
                    key = prop_keys[prop]
                    val = take_value(idea[prop])
                cool_idea[key] = val
            
            #валидирую статус идеи
            valid_staus = {
                None : None,
                "909" : "На экспертизе",
                "910" : "В работе",
                "912" : "Реализовано",
                "913" : "Отказано",
            }
            cool_idea["status"] = valid_staus[cool_idea["status"]]
            #сохраняю
            ideas.append(cool_idea)



        self.ideas = ideas
        self.user_uuid = None
        self.username = None

    def get_user(self, session_id):
        self.user = dict(AuthService().get_user_by_seesion_id(session_id))

        if self.user is not None:
            self.user_uuid = self.user["user_uuid"]
            self.username = self.user["username"]

            #получить и вывести его id
            user_inf = User(uuid = self.user_uuid).user_inf_by_uuid()
            return user_inf.id
        return None
        
    def get_ideas(self, session_id):
        user_id = self.get_user(session_id)
        if user_id is not None:
            result = []
            for idea in self.ideas:
                if str(idea['user_id']) == str(user_id):
                    result.append(idea)
            return result
        else:
            return None
