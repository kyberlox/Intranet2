from fastapi import FastAPI, APIRouter, Body, Request#, Cookie, Header, Response
#from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.User import User
from src.Department import Department
from src.UsDep import UsDep

from src.Section import Section
from src.Article import Article

app = FastAPI()
router = APIRouter()

app.mount("/api/view/static", StaticFiles(directory="./front_jinja/static"), name="static")

templates = Jinja2Templates(directory="./front_jinja")

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




@app.get("/test/{id}")
def test(id):
    return Article(id=id).get_all()


#Заглушки фронта
@app.get("/api/view/menu", tags=["Меню", "View"])
def get_user(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})

@app.get("/api/view/department", tags=["Департамент", "View"])
def get_user(request: Request):
    return templates.TemplateResponse(name="depart.html", context={"request": request})

@app.get("/api/view/user", tags=["Пользователь", "View"])
def get_user(request: Request):
    return templates.TemplateResponse(name="user.html", context={"request": request})



#Пользоваетелей можно обновить
@app.put("/api/users", tags=["Пользователь"])
def get_user():
    usr = User()
    return usr.fetch_users_data()

#Пользователя можно выгрузить
@app.get("/api/user/{id}", tags=["Пользователь"])
def get_user(id):
    return User(id).search_by_id()

#Пользователя можно найти
@app.post("/api/user/search", tags=["Пользователь"])
def get_user(jsn=Body()):
    #будет работать через elasticsearch
    pass



# Департаменты можно обновить
@app.put("/api/departments", tags=["Департамент"])
def get_department():
    depart = Department()
    return depart.fetch_departments_data()

# Департамент можно выгрузить
@app.get("/api/department/{id}", tags=["Департамент"])
def get_department(id):
    return Department(id).search_dep_by_id()

#Пользователя можно найти
@app.post("/api/department/search", tags=["Департамент"])
def get_user(jsn=Body()):
    #будет работать через elasticsearch
    pass



#Таблицу пользователей и департаментов можно обновить
@app.put("/api/users_depart", tags=["Пользователь-Департамент"])
def get_user():
    return UsDep().get_usr_dep()

#Пользователя и его департамент можно выгрузить
@app.get("/api/users_depart/{id}", tags=["Пользователь-Департамент"])
def get_usdepart(id):
    return UsDep(id).search_usdep_by_id()