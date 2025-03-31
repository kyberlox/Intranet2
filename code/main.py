from fastapi import FastAPI, APIRouter, Body, Request#, Cookie, Header, Response
#from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.model.User import User
from src.model.Department import Department
from src.model.UsDep import UsDep

from src.model.Section import Section
from src.model.Article import Article

import time



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



@app.get("/test/{ID}")
def test(ID):
    return Article(section_id=ID).get_inf()



@app.get("/api/total_update")
def total_update():
    time_start = time.time()
    status = 0

    print("Обновление информации о подразделениях")
    if Department().fetch_departments_data()["status"]:
        status += 1
        print("Успешно!")
    else:
        print("Ошибка!")

    print("Обновление информации о пользователях")
    if User().fetch_users_data()["status"]:
        status += 1
        print("Успешно!")
    else:
        print("Ошибка!")

    print("Обновление информации о связи подразделений и пользователей")
    if UsDep().get_usr_dep()["status"]:
        status += 1
        print("Успешно!")
    else:
        print("Ошибка!")

    print("Обновление информации о разделах сайта")
    Section().load()
    status += 1
    print("Успешно!")

    print("Обновление информации о статьях сайта")
    if Article().uplod()["status"]:
        status += 1
        print("Успешно!")
    else:
        print("Ошибка!")

    time_end = time.time()
    total_time_sec = time_end - time_start

    return {"status_code" : f"{status}/5", "time_start" : time_start, "time_end" : time_end, "total_time_sec" : total_time_sec}

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



#Разделы и статьи сайта

#загрузить разделы из json файла
@app.put("/api/section", tags = ["Разделы"])
def upload_sections():
    return Section().load()

#получить все разделы
@app.get("/api/sections", tags = ["Разделы"])
def get_all_sections():
    return Section().get_all()

#получить раздел по id
@app.get("/api/section/{ID}", tags = ["Разделы"])
def get_section(ID):
    return Section(id = ID).find_by_id()

#получить подразделы раздела
@app.get("/api/section/subsection/{ID}", tags = ["Разделы"])
def get_all_sections(ID):
    return Section(parent_id = ID).find_by_parent_id()



#Получить данные инфоблока из Б24
@app.get("/api/infoblock/{ID}")
def test(ID):
    return Article(section_id=ID).get_inf()



#загрузить статьи из иноблоков Битрикса
@app.put("/api/article", tags = ["Статьи"])
def upload_articles():
    return Article().uplod()

#найти статью по id
@app.get("/api/article/{ID}", tags = ["Статьи"])
def get_article(ID):
    return Article(id = ID).search_by_id()

#найти статьи раздела
@app.get("/api/articles/{section_id}", tags = ["Статьи"])
def get_articles(section_id):
    return Article(section_id = section_id).search_by_section_id()

#найти статьи раздела
@app.post("/api/articles/search", tags = ["Статьи"])
def get_articles(data = Body()):
    pass