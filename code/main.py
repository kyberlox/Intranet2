from fastapi import FastAPI, APIRouter, Body, Request#, Cookie, Header, Response
#from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.User import User

from src.Department import Department

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



@app.get("/test/{key}")
def test(key):
    return User().get_dep_usrs()

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