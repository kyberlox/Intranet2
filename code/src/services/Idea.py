from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.model.Article import Article
from src.service.Auth import AuthService




class Idea:
    def __init__(self, user_id=None, user_uuid=None):
        b24_ideas = Article(section_id=121).get_inf()
        
        self.user_uuid = None
        self.username = None

    def get_user(self, session_id):
        self.user = AuthService().get_user_by_seesion_id(session_id)

        if self.user is not None:
            self.user_uuid = self.user["user_uuid"]
            self.username = self.user["username"]
