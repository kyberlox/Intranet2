from fastapi import FastAPI, APIRouter, Body, Request, UploadFile, HTTPException, Response, Request
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks #, Cookie, Header
from fastapi.responses import Response, JSONResponse#, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request, HTTPException, status



# from bson import Binary
from src.model.User import User, users_router
from src.model.Department import Department, depart_router
from src.model.UsDep import UsDep, usdep_router
from src.model.Section import Section, section_router
from src.model.Article import Article, article_router
from src.model.Tag import Tag, tag_router
from src.model.File import File, file_router


from src.base.Elastic.App import search_router
from src.base.Elastic import StructureSearchModel, ArticleSearchModel, UserSearchModel
from src.base.B24 import B24, b24_router

from src.services.VCard import vcard_app
from src.services.Chelp import C_app
from src.services.Auth import AuthService, auth_router
from src.services.Comporession import compress_router
from src.services.Idea import idea_router
from src.services.Editor import editor_router
from src.services.FieldsVisions import fieldsvisions_router
from src.services.Peer import peer_router
from src.services.Roots import roots_router, Roots
from src.services.MerchStore import store_router
from src.services.AIchat import ai_router

from src.services.LogsMaker import LogsMaker

from typing import Awaitable, Callable, Optional

from PIL import Image
from io import BytesIO

import os
from dotenv import load_dotenv

import time

import asyncio



load_dotenv()

DOMAIN = os.getenv('HOST')

app = FastAPI(timeout=60*20)

app.include_router(users_router, prefix="/api")
app.include_router(depart_router, prefix="/api")
app.include_router(usdep_router, prefix="/api")
app.include_router(section_router, prefix="/api")
app.include_router(article_router, prefix="/api")
app.include_router(file_router, prefix="/api")
app.include_router(vcard_app, prefix="/api")
app.include_router(search_router, prefix="/api")

app.include_router(editor_router, prefix="/api")

app.include_router(auth_router, prefix="/api")
app.include_router(compress_router, prefix="/api")

app.include_router(b24_router, prefix="/api")
app.include_router(idea_router, prefix="/api")
app.include_router(fieldsvisions_router, prefix="/api")
app.include_router(tag_router, prefix="/api")
app.include_router(ai_router, prefix="/api")

app.include_router(peer_router, prefix="/api")
app.include_router(roots_router, prefix="/api")
app.include_router(store_router, prefix="/api")

app.include_router(C_app, prefix="/api")


#app.mount("/api/view/app", StaticFiles(directory="./front_jinja/static"), name="app")

#templates = Jinja2Templates(directory="./front_jinja") 

# origins = [
#     "http://localhost:8000",
#     DOMAIN,
#     #"http://intranet.emk.org.ru:8000",
#     #"http://intranet.emk.org.ru"
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "OPTIONS", "PATH"],
    allow_headers=["*"]
    #allow_headers=["Content-Type", "Accept", "Authorization", "Location", "Allow", "Content-Disposition", "Sec-Fetch-Dest", "Access-Control-Allow-Credentials"],
)



# Настройки
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

USER_STORAGE_PATH = "./files_db/user_photo"
os.makedirs(USER_STORAGE_PATH, exist_ok=True)

# Монтируем статику
app.mount("/api/tours", StaticFiles(directory="./files_db/tours"), name="tours")
app.mount("/api/files", StaticFiles(directory=STORAGE_PATH), name="files")
app.mount("/api/user_files", StaticFiles(directory=USER_STORAGE_PATH), name="user_files")



# Исключаем эндпоинты, которые не требуют авторизации (например, сам эндпоинт авторизации)
open_links = [
    "/docs",
    "/api/users_update",
    "/api/users/update_user_info",
    "/openapi.json",
    "/api/auth_router",
    "/api/total_update",
    "/api/files",
    "/api/tours",
    "/api/compress_image", "compress_image",
    "/api/user_files",
    "test", "dump", "get_file", "get_all_files",
    "/api/total_background_task_update",
    "/ws/progress"
]

#Проверка авторизации для ВСЕХ запросов
@app.middleware("http")
async def auth_middleware(request: Request, call_next : Callable[[Request], Awaitable[Response]]):
    # Внедряю свою отладку
    log = LogsMaker()

    

    for open_link in open_links:
        if open_link in request.url.path:
            return await call_next(request)

            # try:
            #     #return call_next(request)
            #     print('тут')
            #     return await call_next(request)
            # except:
            #     return JSONResponse(
            #         status_code = status.HTTP_401_UNAUTHORIZED,
            #         content = log.warning_message(message="Error when trying to follow the link without authorization")
            #     )



    # Проверяем авторизацию для всех остальных /api эндпоинтов
    if request.url.path.startswith("/api"):
        token = request.cookies.get("Authorization")
        if token is None:
            token = request.headers.get("Authorization")
            if token is None:
                return JSONResponse(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    content = log.warning_message(message="Authorization cookies or headers missing")
                )
                # raise HTTPException(
                #     status_code=status.HTTP_401_UNAUTHORIZED,
                #     detail="Authorization cookies missing",
                # )

        try:
            session = AuthService().validate_session(token)
            if not session:
                return JSONResponse(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    content = log.warning_message(message="Invalid token")
                )
                # raise HTTPException(
                #     status_code=status.HTTP_401_UNAUTHORIZED,
                #     detail="Invalid token",
                # )

        except IndexError:
            return JSONResponse(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    content = log.warning_message(message="Invalid authorization cookies or headers format")
                )
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Invalid authorization cookies format",
            # )

    return await call_next(request)



# Прогресс процесса через вебсокет
@app.websocket("/ws/progress/{upload_id}")
async def websocket_endpoint(websocket: WebSocket, upload_id: int):
    from src.model.File import UPLOAD_PROGRESS
    global UPLOAD_PROGRESS
    await websocket.accept()
    LogsMaker().info_message(f"Трансляция на вебсокет по upload_id = {upload_id}")
    try:
        while True:
            # Отправляем прогресс каждые 0.1 секунду
            if upload_id in UPLOAD_PROGRESS:
                progress = UPLOAD_PROGRESS[upload_id]
                await websocket.send_text(f"{progress}")

                LogsMaker().info_message(f"Значение статуса загрузки = {UPLOAD_PROGRESS[upload_id]}%")
                
                # Если загрузка завершена или произошла ошибка, удаляем из хранилища
                if progress >= 100 or progress == -1:
                    # Сначала отправляем финальное сообщение
                    if progress >= 100:
                        await websocket.send_text("Загрузка завершена!")
                        LogsMaker().ready_status_message("Загрузка завершена!")
                    else:
                        await websocket.send_text("Ошибка загрузки!")
                        LogsMaker().warning_message("Ошибка загрузки!")
                    
                    # Ждем немного перед закрытием
                    await asyncio.sleep(0.5)
                    
                    # Удаляем из хранилища
                    if upload_id in UPLOAD_PROGRESS:
                        del UPLOAD_PROGRESS[upload_id]
                    
                    # Закрываем соединение
                    await websocket.close()
                    break
            else:
                # Если upload_id не найден, отправляем сообщение и закрываем
                await websocket.send_text("upload_id не найден")
                LogsMaker().warning_message("upload_id не найден")
                await asyncio.sleep(0.5)  # Даем время отправить сообщение
                await websocket.close()
                break
                
            await asyncio.sleep(0.1)
            

    except WebSocketDisconnect:
        # Клиент отключился
        LogsMaker().warning_message(f"Client disconnected for upload {upload_id}")
    except RuntimeError as e:
        # Игнорируем ошибки "send after close"
        if "close message" not in str(e):
            LogsMaker().error_message(f"WebSocket error: {e}")
    finally:
        # Очистка при любом выходе
        if upload_id in UPLOAD_PROGRESS and (UPLOAD_PROGRESS[upload_id] >= 100 or UPLOAD_PROGRESS[upload_id] == -1):
            del UPLOAD_PROGRESS[upload_id]

# @app.get("/api/progress/{upload_id}")
# async def websocket_endpoint(upload_id: int):
#     from src.model.File import UPLOAD_PROGRESS
#     if upload_id in UPLOAD_PROGRESS:
#         progress = UPLOAD_PROGRESS[upload_id]
#         return progress
#     else:
#         return f'нет такого upload_id = {upload_id}'

@app.get("/get_info_message")
def get_info_message():
    file_path = "./files_db/Информационное_письмо_НПО_ЭМК.docx"

    if not os.path.exists(file_path):
        return LogsMaker().error_message("Файл отсутствует")

    return FileResponse(
        path=file_path,
        filename="Информационное_письмо_НПО_ЭМК.docx",  # Имя файла для пользователя
        media_type='application/octet-stream'
    )

@app.get("/get_test_elastic/{word}")
def get_test_elastic(word: str):
    return StructureSearchModel().get_structure_by_name(word)

@app.get("/get_sec_data/{section_id}")
def test_sec_data(section_id):
    b24 = B24()
    sec_data = b24.getInfoBlock(section_id)
    return sec_data

@app.get("/get_file/{inf_id}/{file_id}")
def test_file_get(inf_id, file_id):
    b24 = B24()
    file_data = b24.get_file(file_id, inf_id)
    return file_data

@app.get("/get_all_files/{file_id}")
def test_file_get(file_id):
    b24 = B24()
    file_data = b24.get_all_files(file_id)
    return file_data

@app.get("/api/full_search/{keyword}")
def elastic_search(keyword: str):
    from src.base.Elastic.App import search_everywhere
    return search_everywhere(key_word=keyword)

@app.put("/api/full_elastic_dump")
def elastic_dump():
    from src.base.Elastic.UserSearchModel import UserSearchModel
    from src.base.Elastic.StuctureSearchmodel import StructureSearchModel
    from src.base.Elastic.ArticleSearchModel import ArticleSearchModel
    UserSearchModel().dump()
    StructureSearchModel().dump()
    ArticleSearchModel().dump()
    return {"status": True}

@app.get("/down_file/{inf_id}/{art_id}/{property}")
def find(inf_id, art_id, property):
    return File().download(inf_id, art_id, property)

@app.get("/find_file/{inf_id}/{file_id}")
def find(inf_id, file_id):
    return B24().get_file(file_id, inf_id)

@app.put("/api/total_background_task_update")
def total_background_task_update(background_tasks: BackgroundTasks):
    background_tasks.add_task(Department().fetch_departments_data)
    background_tasks.add_task(User().fetch_users_data)
    background_tasks.add_task(UsDep().get_usr_dep)
    background_tasks.add_task(Section().load)
    background_tasks.add_task(Tag().add_b24_tag)
    background_tasks.add_task(Article().uplod)
    background_tasks.add_task(Article().upload_likes)
    background_tasks.add_task(Roots().create_primary_admins)
    return {"status" : "started", "message" : "Загрузка запущена в фоновом режиме!"}



@app.get("/api/users_update/")
def total_users_update():
    time_start = time.time()
    status = False

    print("Обновление информации о подразделениях")
    if Department().fetch_departments_data()["status"]:
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
        print("Успешно!")
    else:
        print("Ошибка!")
    
    time_end = time.time()
    total_time_sec = time_end - time_start

    return {"status_code" : status, "time_start" : time_start, "time_end" : time_end, "total_time_sec" : total_time_sec}

@app.get("/api/art_update/")
def total_users_update():
    time_start = time.time()
    status = False

    from src.model.Article import Article
    LogsMaker().info_message("Обновление информации о статьях сайта")
    if Article().uplod()["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")
    
    time_end = time.time()
    total_time_sec = time_end - time_start

    return {"status_code" : status, "time_start" : time_start, "time_end" : time_end, "total_time_sec" : total_time_sec}



@app.put("/api/total_update")
def total_update():
    time_start = time.time()
    status = 0

    
    '''
    from src.model.Department import Department
    LogsMaker().info_message("Обновление информации о подразделениях")
    if Department().fetch_departments_data()["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")
    '''
    LogsMaker().info_message("Обновление информации о пользователях")
    from src.model.User import User
    dowload_status = User().fetch_users_data()["status"]
    if dowload_status:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")

    from src.model.UsDep import UsDep
    LogsMaker().info_message("Обновление информации о связи подразделений и пользователей")
    if UsDep().get_usr_dep()["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")

    '''
    from src.model.Section import Section
    LogsMaker().info_message("Обновление информации о разделах сайта")
    Section().load()
    status += 1
    LogsMaker().ready_status_message("Успешно!")

    from src.model.Tag import Tag
    LogsMaker().info_message("Обновление информации о тэгах сайта")
    if Tag().add_b24_tag()["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")

    from src.model.Article import Article
    LogsMaker().info_message("Обновление информации о статьях сайта")
    if Article().uplod()["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")

    from src.services.Roots import Roots
    LogsMaker().info_message("Обновление информации об администратарах сайта")
    if Roots().create_primary_admins()["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")

    #Права пользователей
    # Лайки и просмотры
    # Тэги
    # Система эфективности
    '''

    time_end = time.time()
    total_time_sec = time_end - time_start

    return {"status_code" : f"{status}/5", "time_start" : time_start, "time_end" : time_end, "total_time_sec" : total_time_sec}

# @app.get("/elastic_dump")
# def elastic_dump():
#     # res = UserSearchModel().dump()
#     res = StructureSearchModel().dump()
#     return res
'''
! Особенные запросы
'''
