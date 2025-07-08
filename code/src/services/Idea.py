from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.model.Article import Article
from src.service.Auth import AuthService




class Idea:
    def __init__(self, user_id=None, user_uuid=None):
        #беру идеи из битры
        b24_ideas = Article(section_id=121).get_inf()

        ideas = []
        #каждую идею
        for idea in self.b24_ideas:
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
                    val = idea[prop]
                cool_idea[key] = val
            valid_staus = {
                "" : "",
                "" : "",
                "" : "",
                "" : "",
            }
            cool_idea["status"] = valid_staus[cool_idea["status"]]
            ideas.append(cool_idea)



        self.ideas = ideas
        self.user_uuid = None
        self.username = None

    def get_user(self, session_id):
        self.user = AuthService().get_user_by_seesion_id(session_id)

        if self.user is not None:
            self.user_uuid = self.user["user_uuid"]
            self.username = self.user["username"]

            #получить и вывести его id
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
            return {'err' : "AuthCheckError!"}
