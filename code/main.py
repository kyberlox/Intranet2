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


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.pSQL.objects.App import get_async_db

load_dotenv()

DOMAIN = os.getenv('HOST')

#app = FastAPI(title="МЕГА ТУРБО ГИПЕР УЛЬТРА ИНТРАНЕТ", docs_url="/api/docs") # timeout=60*20 version="2.0", openapi="3.1.0", docs_url="/api/docs"
app = FastAPI(
    titile="Intranet2.0 API DOCS",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json"
)

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

templates = Jinja2Templates(directory="./src/services/templates") 

# origins = [
#     "http://localhost:8000",
#     DOMAIN,
#     "https://intranet.emk.ru",
#     "http://intranet.emk.ru"
# ]


origins = ['*']

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
    "/api/docs",
    "/api/users/update",
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


@app.put("/create_tables")
async def create_tables():
    from src.base.pSQL.models.App import create_tables
    res = await create_tables()
    return res

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
async def elastic_dump(session: AsyncSession=Depends(get_async_db)):
    from src.base.Elastic.UserSearchModel import UserSearchModel
    from src.base.Elastic.StuctureSearchmodel import StructureSearchModel
    from src.base.Elastic.ArticleSearchModel import ArticleSearchModel
    await UserSearchModel().dump(session)
    await StructureSearchModel().dump(session)
    await ArticleSearchModel().dump(session)
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
    if asyncio.run(Article().uplod())["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")
    
    time_end = time.time()
    total_time_sec = time_end - time_start

    return {"status_code" : status, "time_start" : time_start, "time_end" : time_end, "total_time_sec" : total_time_sec}



@app.put("/api/total_update")
async def total_update(session: AsyncSession=Depends(get_async_db)):
    time_start = time.time()
    status = 0

    
    from src.base.pSQL.models.App import create_tables
    res = await create_tables()
    
  
    from src.model.Department import Department
    LogsMaker().info_message("Обновление информации о подразделениях")
    res = await Department().fetch_departments_data(session)
    if res["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")

    

    
    LogsMaker().info_message("Обновление информации о пользователях")
    from src.model.User import User
    dowload_status = await User().fetch_users_data(session)
    if dowload_status["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")
    
    
    from src.model.UsDep import UsDep
    LogsMaker().info_message("Обновление информации о связи подразделений и пользователей")
    res = await UsDep().get_usr_dep(session)
    if res["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")

    
    from src.model.Section import Section
    LogsMaker().info_message("Обновление информации о разделах сайта")
    await Section().load(session)
    status += 1
    LogsMaker().ready_status_message("Успешно!")

    from src.model.Tag import Tag
    LogsMaker().info_message("Обновление информации о тэгах сайта")
    res = await Tag().add_b24_tag(session)
    if res["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")

    from src.model.Article import Article
    LogsMaker().info_message("Обновление информации о статьях сайта")
    res = await Article().uplod(session)
    if res["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")

    from src.services.Roots import Roots
    LogsMaker().info_message("Обновление информации об администратарах сайта")
    res = await Roots().create_primary_admins(session)
    if res["status"]:
        status += 1
        LogsMaker().ready_status_message("Успешно!")
    else:
        LogsMaker().error_message("Ошибка!")
    #Права пользователей
    # Лайки и просмотры
    # Тэги
    # Система эфективности

    time_end = time.time()
    total_time_sec = time_end - time_start

    return {"status_code" : f"{status}/5", "time_start" : time_start, "time_end" : time_end, "total_time_sec" : total_time_sec}

@app.delete("/api/delete_tables")
async def delete_tables(session: AsyncSession=Depends(get_async_db)):
    from sqlalchemy import text
    try:
        # Удаляем таблицы (важен порядок из-за foreign keys)
        await session.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        await session.execute(text("DROP TABLE IF EXISTS userfiles CASCADE"))
        await session.commit()
        
        print("✅ Таблицы User и UserFiles успешно удалены")
        return True
        
    except Exception as e:
        await session.rollback()
        print(f"❌ Ошибка при удалении таблиц: {e}")
        return False



from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

# Встроенный CSS стиль
CUSTOM_STYLE = """
<style>
    /* Основные цвета */
    :root {
        --orange: #ff6600;
        --black: #000000;
        --dark-bg: #0a0a0a;
        --white: #ffffff;
        --gray: #333333;
    }
    
    /* Общие стили */
    body {
        background-color: var(--dark-bg) !important;
        color: var(--white) !important;
    }
    
    /* Контейнер Swagger UI */
    .swagger-ui {
        font-family: sans-serif !important;
        background-color: var(--dark-bg) !important;
    }
    
    /* Верхняя панель */
    .swagger-ui .topbar {
        background-color: var(--black) !important;
        border-bottom: 2px solid var(--orange) !important;
        padding: 10px 0 !important;
    }
    
    .swagger-ui .topbar-wrapper {
        display: flex !important;
        align-items: center !important;
    }
    
    .swagger-ui .topbar-wrapper svg {
        display: none !important;
    }
    
    .swagger-ui .topbar-wrapper .link {
        color: var(--orange) !important;
        font-size: 1.5em !important;
        font-weight: bold !important;
        text-decoration: none !important;
    }
    
    /* Заголовки */
    .swagger-ui .info .title {
        color: var(--orange) !important;
        font-size: 2em !important;
        font-weight: bold !important;
        margin-bottom: 20px !important;
    }
    
    .swagger-ui .info h2 {
        color: var(--orange) !important;
    }
    
    /* Методы запросов */
    .swagger-ui .opblock-tag {
        color: var(--white) !important;
        font-size: 1.2em !important;
        border-bottom: 1px solid var(--gray) !important;
        padding-bottom: 10px !important;
        margin-top: 20px !important;
    }
    
    .swagger-ui .opblock-tag:hover {
        background-color: var(--black) !important;
    }
    
    .swagger-ui .opblock .opblock-summary-method {
        background-color: var(--orange) !important;
        color: var(--black) !important;
        font-weight: bold !important;
        border-radius: 3px !important;
        padding: 5px 10px !important;
        min-width: 80px !important;
        text-align: center !important;
    }
    
    /* Карточки */
    .swagger-ui .opblock {
        background-color: var(--black) !important;
        border: 1px solid var(--gray) !important;
        border-left: 4px solid var(--orange) !important;
        border-radius: 4px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
    }
    
    .swagger-ui .opblock .opblock-summary {
        padding: 15px !important;
    }
    
    .swagger-ui .opblock .opblock-summary-path,
    .swagger-ui .opblock .opblock-summary-description {
        color: var(--white) !important;
    }
    
    /* Секция с параметрами и ответами */
    .swagger-ui .opblock .opblock-section-header {
        background-color: #111111 !important;
        border-bottom: 1px solid var(--gray) !important;
    }
    
    .swagger-ui .opblock .opblock-section-header h4 {
        color: var(--white) !important;
    }
    
    .swagger-ui .opblock .tab-header .tab-item.active h4 span {
        color: var(--orange) !important;
    }
    
    /* Кнопки */
    .swagger-ui .btn {
        background-color: var(--orange) !important;
        color: var(--black) !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        padding: 8px 16px !important;
        transition: background-color 0.3s !important;
    }
    
    .swagger-ui .btn:hover {
        background-color: #ff8533 !important;
    }
    
    .swagger-ui .btn.execute {
        background-color: var(--orange) !important;
        color: var(--black) !important;
    }
    
    /* Текст */
    .swagger-ui .info p,
    .swagger-ui .info li,
    .swagger-ui .opblock-tag {
        color: var(--white) !important;
    }
    
    .swagger-ui .info li {
        margin-bottom: 5px !important;
    }
    
    /* Input поля */
    .swagger-ui input[type="text"],
    .swagger-ui select,
    .swagger-ui textarea {
        background-color: var(--black) !important;
        color: var(--white) !important;
        border: 1px solid var(--gray) !important;
        border-radius: 4px !important;
        padding: 8px !important;
    }
    
    .swagger-ui .parameters-col_name {
        color: var(--white) !important;
    }
    
    .swagger-ui .parameter__type {
        color: var(--orange) !important;
    }
    
    /* Таблицы */
    .swagger-ui table thead tr th,
    .swagger-ui table thead tr td {
        background-color: var(--black) !important;
        color: var(--white) !important;
        border-bottom: 2px solid var(--orange) !important;
        padding: 10px !important;
    }
    
    .swagger-ui table tbody tr {
        background-color: #111111 !important;
    }
    
    .swagger-ui table tbody tr td {
        color: var(--white) !important;
        padding: 10px !important;
        border-bottom: 1px solid var(--gray) !important;
    }
    
    /* Модели */
    .swagger-ui section.models {
        background-color: var(--black) !important;
        border: 1px solid var(--gray) !important;
    }
    
    .swagger-ui section.models .model-container {
        background-color: #111111 !important;
        color: var(--white) !important;
    }
    
    .swagger-ui .model-title {
        color: var(--orange) !important;
    }
    
    .swagger-ui .model {
        color: var(--white) !important;
    }
    
    /* Плейсхолдеры */
    .swagger-ui .placeholder-text {
        color: #888 !important;
    }
    
    /* Ссылки */
    .swagger-ui a {
        color: var(--orange) !important;
    }
    
    .swagger-ui a:hover {
        color: #ff8533 !important;
    }
    
    /* Попапы */
    .swagger-ui .dialog-ux .modal-ux-header {
        background-color: var(--black) !important;
        border-bottom: 1px solid var(--orange) !important;
    }
    
    .swagger-ui .dialog-ux .modal-ux-content {
        background-color: #111111 !important;
        color: var(--white) !important;
    }
    
    /* Секция авторизации */
    .swagger-ui .auth-btn-wrapper {
        margin: 20px 0 !important;
    }
    
    /* Секция информации */
    .swagger-ui .info {
        margin: 30px 0 !important;
    }
    
    /* Загрузка */
    .swagger-ui .loading-container {
        color: var(--white) !important;
    }
</style>
"""

# 1. Создаем кастомную OpenAPI схему
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Intranet2.0 API Docs",
        version="2.0.0",
        description="""
        Добро пожаловать в документация к ресурсам REST API, реализованного с помощью Python3 Fastapi, для внутреннего функционирования веб-сервиса Intranet2.0!

        Особенности проекта:
            - Модульная структура
            - Аснхронность
            - Взаимодействие 3х Баз Данных
        """,
        routes=app.routes,
        openapi_version="3.1.0"
    )

    # # Добавляем кастомную информацию
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjEwMCIgaGVpZ2h0PSIxMDAiIGZpbGw9IiMwMDAwMDAiLz48cGF0aCBkPSJNNTAgMTVMODUgNTBMNTAgODVMMTUgNTBMNTAgMTVaIiBmaWxsPSIjZmY2NjAwIi8+PHBhdGggZD0iTTUwIDI1TDc1IDUwTDUwIDc1TDI1IDUwTDUwIDI1WiIgZmlsbD0iI2ZmODUzMyIvPjxjaXJjbGUgY3g9IjUwIiBjeT0iNTAiIHI9IjE1IiBmaWxsPSIjZmZmZmZmIi8+PC9zdmc+",
    #     "backgroundColor": "#000000",
    #     "altText": "API Logo"
    # }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 2. Endpoint для получения OpenAPI схемы
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return app.openapi()

# Кастомный HTML для Swagger UI с inline стилями
SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🚀 Intranet2.0 API Docs</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/index.css">
    <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/favicon-32x32.png" sizes="32x32">
    <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/favicon-16x16.png" sizes="16x16">
    <style>
        :root {
            --orange: #ff6600;
            --black: #000000;
            --dark-bg: #0a0a0a;
            --white: #ffffff;
            --gray: #333333;
            --light-gray: #444444;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: sans-serif;
            background: var(--dark-bg);
            color: var(--white);
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, var(--black) 0%, #1a1a1a 100%);
            padding: 20px 40px;
            border-bottom: 3px solid var(--orange);
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .logo-title {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .logo {
            width: 60px;
            height: 60px;
            background: var(--orange);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            color: var(--black);
            box-shadow: 0 4px 8px rgba(255,102,0,0.3);
        }
        
        .title-section h1 {
            color: var(--orange);
            font-size: 28px;
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .title-section p {
            color: #cccccc;
            font-size: 16px;
        }
        
        .version-badge {
            background: var(--orange);
            color: var(--black);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            margin-left: 15px;
        }
        
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 40px;
        }
        
        /* Swagger UI Customizations */
        #swagger-ui {
            padding-top: 20px;
        }
        
        .swagger-ui .information-container {
            background: var(--black) !important;
            border: 1px solid var(--gray) !important;
            border-radius: 8px !important;
            margin: 20px 0 !important;
            padding: 25px !important;
        }
        
        .swagger-ui .info .title {
            color: var(--orange) !important;
            font-size: 32px !important;
            margin-bottom: 10px !important;
        }
        
        .swagger-ui .info .description {
            color: #cccccc !important;
            font-size: 16px !important;
            line-height: 1.8 !important;
        }
        
        .swagger-ui .opblock-tag {
            color: var(--white) !important;
            font-size: 22px !important;
            border-bottom: 2px solid var(--orange) !important;
            padding-bottom: 10px !important;
            margin-top: 40px !important;
            background: rgba(0,0,0,0.3) !important;
            padding: 15px !important;
            border-radius: 8px !important;
        }
        
        .swagger-ui .opblock {
            background: var(--black) !important;
            border: 1px solid var(--gray) !important;
            border-left: 5px solid var(--orange) !important;
            border-radius: 8px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }
        
        .swagger-ui .opblock:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(0,0,0,0.4) !important;
        }
        
        .swagger-ui .opblock .opblock-summary-method {
            background: var(--orange) !important;
            color: var(--black) !important;
            font-weight: bold !important;
            border-radius: 4px !important;
            min-width: 85px !important;
            text-align: center !important;
            padding: 6px 0 !important;
            font-size: 14px !important;
            border: none !important;
        }
        
        .swagger-ui .opblock .opblock-summary-path {
            color: var(--white) !important;
            font-size: 16px !important;
            font-family: monospace !important;
        }
        
        .swagger-ui .opblock .opblock-summary-description {
            color: #cccccc !important;
            font-size: 14px !important;
        }
        
        .swagger-ui .btn {
            background: var(--orange) !important;
            color: var(--black) !important;
            border: none !important;
            border-radius: 4px !important;
            font-weight: bold !important;
            padding: 10px 20px !important;
            transition: all 0.3s ease !important;
        }
        
        .swagger-ui .btn:hover {
            background: #ff8533 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px rgba(255,102,0,0.3) !important;
        }
        
        .swagger-ui .btn.execute {
            background: var(--orange) !important;
            color: var(--black) !important;
        }
        
        .swagger-ui .btn.cancel {
            background: var(--light-gray) !important;
            color: var(--white) !important;
        }
        
        .swagger-ui input[type="text"],
        .swagger-ui select,
        .swagger-ui textarea {
            background: rgba(0,0,0,0.5) !important;
            color: var(--white) !important;
            border: 1px solid var(--gray) !important;
            border-radius: 4px !important;
            padding: 10px !important;
            font-size: 14px !important;
        }
        
        .swagger-ui input[type="text"]:focus,
        .swagger-ui select:focus,
        .swagger-ui textarea:focus {
            border-color: var(--orange) !important;
            outline: none !important;
            box-shadow: 0 0 0 2px rgba(255,102,0,0.2) !important;
        }
        
        .swagger-ui .parameters-col_name {
            color: var(--white) !important;
            font-weight: 500 !important;
        }
        
        .swagger-ui .parameter__type {
            color: var(--orange) !important;
            font-weight: bold !important;
        }
        
        .swagger-ui .response-col_status {
            color: var(--orange) !important;
            font-weight: bold !important;
        }
        
        .swagger-ui .response-col_description {
            color: #cccccc !important;
        }
        
        .swagger-ui .tab {
            border-bottom: 2px solid transparent !important;
        }
        
        .swagger-ui .tab.active {
            border-bottom-color: var(--orange) !important;
        }
        
        .swagger-ui .tab-item.active h4 span {
            color: var(--orange) !important;
        }
        
        .swagger-ui .model-title {
            color: var(--orange) !important;
        }
        
        .swagger-ui .model-toggle::after {
            background-color: var(--orange) !important;
        }
        
        .swagger-ui .topbar {
            display: none !important;
        }
        
        .swagger-ui .scheme-container {
            background: rgba(0,0,0,0.3) !important;
            box-shadow: none !important;
            border: 1px solid var(--gray) !important;
            border-radius: 8px !important;
            margin: 20px 0 !important;
        }
        
        .swagger-ui .auth-btn-wrapper {
            padding: 20px !important;
        }
        
        .footer {
            background: var(--black);
            border-top: 1px solid var(--gray);
            padding: 30px 40px;
            margin-top: 50px;
            text-align: center;
        }
        
        .footer-content {
            max-width: 1400px;
            margin: 0 auto;
            color: #888;
            font-size: 14px;
        }
        
        .footer a {
            color: var(--orange);
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--black);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--orange);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #ff8533;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo-title">
                <div class="logo">API</div>
                <div class="title-section">
                    <h1>🚀 Intranet2.0 API Documentation <span class="version-badge">v2.0.0</span></h1>
                    <p>Interactive API documentation for Intranet2.0 services and endpoints</p>
                </div>
            </div>
        </div>
    </header>
    
    <main class="main-container">
        <div id="swagger-ui"></div>
    </main>
    
    <footer class="footer">
        <div class="footer-content">
            <p>© 2024 Intranet2.0 API. All rights reserved.</p>
            <p>For support contact: <a href="mailto:support@intranet.com">support@intranet.com</a></p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
    <script>
    window.onload = function() {
        // Swagger UI configuration
        const ui = SwaggerUIBundle({
            url: "/openapi.json",
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout",
            docExpansion: 'list',
            defaultModelsExpandDepth: 1,
            defaultModelExpandDepth: 2,
            defaultModelRendering: 'model',
            displayRequestDuration: true,
            filter: true,
            operationsSorter: 'alpha',
            tagsSorter: 'alpha',
            showExtensions: true,
            showCommonExtensions: true,
            tryItOutEnabled: true,
            requestSnippetsEnabled: true,
            persistAuthorization: true,
            displayOperationId: false,
            syntaxHighlight: {
                theme: 'monokai'
            },
            onComplete: function() {
                // Custom initialization after Swagger UI loads
                console.log('Intranet2.0 API Documentation loaded successfully!');
                
                // Add custom classes to enhance styling
                setTimeout(() => {
                    // Style the info container
                    const infoContainer = document.querySelector('.information-container');
                    if (infoContainer) {
                        infoContainer.style.cssText += 'background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important;';
                    }
                    
                    // Style operation blocks
                    const opblocks = document.querySelectorAll('.opblock');
                    opblocks.forEach(opblock => {
                        opblock.style.cssText += 'transition: all 0.3s ease !important;';
                    });
                    
                    // Style buttons
                    const buttons = document.querySelectorAll('.btn');
                    buttons.forEach(btn => {
                        if (!btn.classList.contains('execute')) {
                            btn.style.cssText += 'background: linear-gradient(135deg, #ff6600 0%, #ff8533 100%) !important;';
                        }
                    });
                }, 100);
            }
        });
        
        // Make UI accessible globally
        window.ui = ui;
        
        // Theme toggle functionality
        const style = document.createElement('style');
        style.textContent = `
            .theme-toggle {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: var(--orange);
                color: var(--black);
                border: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                font-size: 20px;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 1000;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
            }
            
            .theme-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 16px rgba(0,0,0,0.4);
            }
        `;
        document.head.appendChild(style);
        
        // Add theme toggle button
        const themeToggle = document.createElement('button');
        themeToggle.className = 'theme-toggle';
        themeToggle.innerHTML = '🎨';
        themeToggle.title = 'Toggle theme colors';
        document.body.appendChild(themeToggle);
        
        let isDarkTheme = true;
        themeToggle.addEventListener('click', function() {
            const root = document.documentElement;
            if (isDarkTheme) {
                // Switch to light theme
                root.style.setProperty('--dark-bg', '#f5f5f5');
                root.style.setProperty('--black', '#ffffff');
                root.style.setProperty('--white', '#333333');
                root.style.setProperty('--gray', '#dddddd');
                document.body.style.background = '#f5f5f5';
                themeToggle.innerHTML = '🌙';
            } else {
                // Switch back to dark theme
                root.style.setProperty('--dark-bg', '#0a0a0a');
                root.style.setProperty('--black', '#000000');
                root.style.setProperty('--white', '#ffffff');
                root.style.setProperty('--gray', '#333333');
                document.body.style.background = '#0a0a0a';
                themeToggle.innerHTML = '🎨';
            }
            isDarkTheme = !isDarkTheme;
        });
    };
    </script>
</body>
</html>
"""

# 3. Endpoint для Swagger UI
@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    async def custom_docs():
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Docs</title>
            <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css">
            <style>
                body { background: #0a0a0a; color: white; }
                .swagger-ui .info .title { color: #ff6600 !important; }
            </style>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
            <script>
                window.onload = () => {
                    SwaggerUIBundle({
                        url: '/openapi.json',
                        dom_id: '#swagger-ui',
                        presets: [SwaggerUIBundle.presets.apis]
                    });
                };
            </script>
        </body>
        </html>
        """)

# async def custom_swagger_ui_html():
#     html = get_swagger_ui_html(
#         openapi_url="/openapi.json",
#         title="🚀 Intranet2.0 API Docs",
#         swagger_ui_parameters={
#             "defaultModelsExpandDepth": 1,
#             "defaultModelExpandDepth": 2,
#             "defaultModelRendering": "model",
#             "displayRequestDuration": True,
#             "docExpansion": "list",
#             "filter": True,
#             "maxDisplayedTags": 20,
#             "operationsSorter": "alpha",
#             "tagsSorter": "alpha",
#             "showExtensions": True,
#             "showCommonExtensions": True,
#             "tryItOutEnabled": True,
#             "requestSnippetsEnabled": True,
#             "persistAuthorization": True,
#             "displayOperationId": False,
#             "deepLinking": True,
#             "syntaxHighlight": {
#                 "theme": "monokai"
#             },
#             "tryItOutEnabled": True,
#             "displayRequestDuration": True,
#             "requestSnippetsEnabled": True,
#             # Убрана опция темы, так как она конфликтует с кастомными стилями
#         }
#     )

#     # Добавляем кастомный HTML заголовок перед основным контентом
#     custom_header = """
#     <div style="
#         background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
#         padding: 20px;
#         margin-bottom: 30px;
#         border-radius: 8px;
#         border-left: 6px solid #ff6600;
#     ">
#         <h1 style="color: #ff6600; margin: 0 0 10px 0;">🚀 Intranet2.0 API Documentation</h1>
#         <p style="color: #ffffff; margin: 0; font-size: 16px;">
#             Welcome to the Intranet2.0 API documentation. Explore available endpoints, test requests, 
#             and integrate with our services.
#         </p>
#     </div>
#     """
    
#     # Добавляем стили в head
#     html = html.replace('</head>', CUSTOM_STYLE + '</head>')
    
#     # Добавляем кастомный заголовок после открывающего тега body
#     html = html.replace('<body>', f'<body><div class="swagger-ui"><div class="wrapper">{custom_header}')
    
#     return HTMLResponse(content=html)

    # return get_swagger_ui_html(
    #     openapi_url="/openapi.json",  # ссылка на нашу схему
    #     title="My API - Swagger UI",
    #     oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    #     swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    #     swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    #     swagger_ui_parameters={
    #         "defaultModelsExpandDepth": -1,
    #         "docExpansion": "none",
    #         "filter": True,
    #         "displayRequestDuration": True,
    #         "tryItOutEnabled": True,
    #     }
    # )
