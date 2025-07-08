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
            id = idea["ID"]
            prop_keys = {
                "" : ""
            }

            cool_idea = dict()
            for prop in prop_keys.keys():
                
                val = None
                if prop in idea:
                    key = prop_keys[prop]
                    val = idea[prop]
                cool_idea[key] = val
            
            ideas.append(cool_idea)
            


        self.ideas = ideas
        self.user_uuid = None
        self.username = None

    def get_user(self, session_id):
        self.user = AuthService().get_user_by_seesion_id(session_id)

        if self.user is not None:
            self.user_uuid = self.user["user_uuid"]
            self.username = self.user["username"]
        

