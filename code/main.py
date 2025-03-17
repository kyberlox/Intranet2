from fastapi import FastAPI, APIRouter, Body#, Cookie, Header, Response
#from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.User import User

app = FastAPI()
router = APIRouter()

origins = [
    "http://localhost:8000",
    "http://intranet.emk.org.ru:8000",
    "http://intranet.emk.org.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "OPTIONS", "PATH"],
    allow_headers=["*"]
    #allow_headers=["Content-Type", "Accept", "Authorization", "Location", "Allow", "Content-Disposition", "Sec-Fetch-Dest", "Access-Control-Allow-Credentials"],
)



@app.get("/test/{key}")
def test(key):
    return User().get_dep_usrs()

#Заглушка фронта
@app.get("/api/view/user", tags=["Пользователь", "View"])
def get_user():
    pass

#Пользоваетелей можно обновить
@app.put("/api/users", tags=["Пользователь"])
def get_user():
    usr = User()
    return usr.fetch_users_data()

#Пользователя можно выгрузить
@app.get("/api/user/{id}", tags=["Пользователь"])
def get_user():
    pass

#Пользователя можно найти
@app.post("/api/user/search", tags=["Пользователь"])
def get_user(jsn=Body()):
    #будет работать через elasticsearch
    pass