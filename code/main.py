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
from fastapi.responses import HTMLResponse
import re


# Встроенный CSS стиль
# Кастомные стили
CUSTOM_CSS = """
<style>
    /* Основные переменные */
    :root {
        --primary: #ff6600;
        --primary-light: #ff8533;
        --primary-dark: #cc5200;
        --bg-dark: #0a0a0a;
        --bg-darker: #050505;
        --bg-black: #000000;
        --text-white: #ffffff;
        --text-gray: #cccccc;
        --text-dark: #333333;
        --border-color: #333333;
        --border-light: #444444;
        --success: #00cc66;
        --warning: #ffaa00;
        --error: #ff3333;
        --info: #3399ff;
    }

    /* Общие стили */
    body {
        background-color: var(--bg-dark) !important;
        color: var(--text-white) !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Заменяем стандартные стили Swagger */
    .swagger-ui {
        background-color: var(--bg-dark) !important;
        font-family: inherit !important;
    }

    /* Верхняя панель */
    .swagger-ui .topbar {
        background: linear-gradient(135deg, var(--bg-black) 0%, var(--bg-darker) 100%) !important;
        border-bottom: 3px solid var(--primary) !important;
        padding: 15px 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    }

    .swagger-ui .topbar-wrapper {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 0 20px !important;
        display: flex !important;
        align-items: center !important;
    }

    .swagger-ui .topbar-wrapper svg {
        display: none !important;
    }

    .swagger-ui .topbar-wrapper .link {
        color: var(--primary) !important;
        font-size: 24px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }

    .swagger-ui .topbar-wrapper .link::before {
        content: "🚀";
        font-size: 28px;
    }

    .swagger-ui .topbar-wrapper .link::after {
        content: "Intranet2.0 API v2.0.0";
    }

    /* Заголовок */
    .swagger-ui .info .title {
        color: var(--primary) !important;
        font-size: 36px !important;
        font-weight: bold !important;
        margin-bottom: 15px !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
    }

    .swagger-ui .info .title::after {
        content: " v2.0.0";
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        color: var(--bg-black);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin-left: 15px;
        vertical-align: middle;
    }

    /* Теги (группы endpoints) */
    .swagger-ui .opblock-tag {
        color: var(--text-white) !important;
        font-size: 24px !important;
        font-weight: 600 !important;
        border-bottom: 3px solid var(--primary) !important;
        padding: 20px 0 15px 0 !important;
        margin: 40px 0 20px 0 !important;
        background: none !important;
    }

    .swagger-ui .opblock-tag:hover {
        background: rgba(255, 102, 0, 0.1) !important;
        cursor: pointer;
    }

    /* Блоки операций */
    .swagger-ui .opblock {
        background: var(--bg-black) !important;
        border: 1px solid var(--border-color) !important;
        border-left: 6px solid var(--primary) !important;
        border-radius: 10px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.3s ease !important;
    }

    .swagger-ui .opblock:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35) !important;
        border-color: var(--primary-light) !important;
    }

    /* Методы HTTP */
    .swagger-ui .opblock .opblock-summary-method {
        background: var(--primary) !important;
        color: var(--bg-black) !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        min-width: 90px !important;
        text-align: center !important;
        padding: 8px 0 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(255, 102, 0, 0.3) !important;
    }

    /* Цвета для разных методов */
    .swagger-ui .opblock.opblock-get .opblock-summary-method {
        background: var(--primary) !important;
    }

    .swagger-ui .opblock.opblock-post .opblock-summary-method {
        background: var(--success) !important;
    }

    .swagger-ui .opblock.opblock-put .opblock-summary-method {
        background: var(--warning) !important;
    }

    .swagger-ui .opblock.opblock-delete .opblock-summary-method {
        background: var(--error) !important;
    }

    .swagger-ui .opblock.opblock-patch .opblock-summary-method {
        background: var(--info) !important;
    }

    /* Путь endpoint */
    .swagger-ui .opblock .opblock-summary-path {
        color: var(--text-white) !important;
        font-size: 18px !important;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
        font-weight: 500 !important;
        margin-left: 15px !important;
    }

    /* Описание endpoint */
    .swagger-ui .opblock .opblock-summary-description {
        color: var(--text-gray) !important;
        font-size: 14px !important;
        margin-top: 10px !important;
    }

    /* Кнопки */
    .swagger-ui .btn {
        background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
        color: var(--bg-black) !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 8px rgba(255, 102, 0, 0.3) !important;
    }

    .swagger-ui .btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(255, 102, 0, 0.4) !important;
    }

    .swagger-ui .btn.execute {
        min-width: 100px !important;
    }

    /* Поля ввода */
    .swagger-ui input[type="text"],
    .swagger-ui input[type="password"],
    .swagger-ui input[type="email"],
    .swagger-ui input[type="number"],
    .swagger-ui select,
    .swagger-ui textarea {
        background: rgba(0, 0, 0, 0.7) !important;
        color: var(--text-white) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        padding: 12px 15px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }

    .swagger-ui input:focus,
    .swagger-ui select:focus,
    .swagger-ui textarea:focus {
        border-color: var(--primary) !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(255, 102, 0, 0.2) !important;
    }

    /* Параметры */
    .swagger-ui .parameters-col_name {
        color: var(--text-white) !important;
        font-weight: 500 !important;
    }

    .swagger-ui .parameter__type {
        color: var(--primary) !important;
        font-weight: bold !important;
    }

    /* Ответы */
    .swagger-ui .response-col_status {
        color: var(--primary) !important;
        font-weight: bold !important;
    }

    /* Модели */
    .swagger-ui .model-title {
        color: var(--primary) !important;
        font-weight: bold !important;
    }

    /* Панель авторизации */
    .swagger-ui .scheme-container {
        background: rgba(0, 0, 0, 0.5) !important;
        box-shadow: none !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        margin: 20px 0 !important;
        padding: 20px !important;
    }

    /* Таблицы */
    .swagger-ui table thead tr th,
    .swagger-ui table thead tr td {
        background: var(--bg-black) !important;
        color: var(--text-white) !important;
        border-bottom: 2px solid var(--primary) !important;
    }

    .swagger-ui table tbody tr td {
        color: var(--text-gray) !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    /* Вкладки */
    .swagger-ui .tab {
        border-bottom: 3px solid transparent !important;
        padding: 10px 20px !important;
    }

    .swagger-ui .tab:hover {
        background: rgba(255, 102, 0, 0.1) !important;
    }

    .swagger-ui .tab.active {
        border-bottom-color: var(--primary) !important;
        color: var(--primary) !important;
        font-weight: bold !important;
    }

    /* Скрываем ненужные элементы */
    .swagger-ui .download-url-wrapper {
        display: none !important;
    }

    /* Кастомный скроллбар */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-light);
    }

    /* Анимации */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .swagger-ui .opblock {
        animation: fadeIn 0.5s ease-out;
    }

    /* Кастомный заголовок */
    .custom-header {
        background: linear-gradient(135deg, var(--bg-black) 0%, var(--bg-darker) 100%);
        padding: 30px;
        margin: 0 0 30px 0;
        border-radius: 12px;
        border-left: 8px solid var(--primary);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        animation: fadeIn 0.7s ease-out;
    }

    .custom-header h1 {
        color: var(--primary);
        font-size: 32px;
        margin: 0 0 10px 0;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .custom-header h1::before {
        content: "🚀";
        font-size: 36px;
    }

    .custom-header p {
        color: var(--text-gray);
        font-size: 16px;
        line-height: 1.6;
        margin: 0;
    }

    /* Дополнительные улучшения */
    .swagger-ui .info .description {
        color: var(--text-gray) !important;
        font-size: 16px !important;
        line-height: 1.8 !important;
    }

    .swagger-ui .info .description h2,
    .swagger-ui .info .description h3 {
        color: var(--primary) !important;
        margin: 20px 0 10px 0 !important;
    }

    /* Иконки для методов */
    .swagger-ui .opblock-summary-method::before {
        margin-right: 5px;
    }

    .swagger-ui .opblock.opblock-get .opblock-summary-method::before {
        content: "📥 ";
    }

    .swagger-ui .opblock.opblock-post .opblock-summary-method::before {
        content: "➕ ";
    }

    .swagger-ui .opblock.opblock-put .opblock-summary-method::before {
        content: "✏️ ";
    }

    .swagger-ui .opblock.opblock-delete .opblock-summary-method::before {
        content: "🗑️ ";
    }

    .swagger-ui .opblock.opblock-patch .opblock-summary-method::before {
        content: "🔄 ";
    }
</style>

<script>
    // Дополнительный JavaScript для улучшений
    document.addEventListener('DOMContentLoaded', function() {
        // Добавляем кнопку "Наверх"
        const scrollToTopBtn = document.createElement('button');
        scrollToTopBtn.innerHTML = '⬆';
        scrollToTopBtn.title = 'Наверх';
        scrollToTopBtn.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #ff6600, #ff8533);
            color: #000;
            border: none;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            z-index: 1000;
            display: none;
            box-shadow: 0 4px 12px rgba(255, 102, 0, 0.3);
            transition: all 0.3s ease;
        `;
        
        scrollToTopBtn.addEventListener('mouseover', () => {
            scrollToTopBtn.style.transform = 'scale(1.1)';
            scrollToTopBtn.style.boxShadow = '0 6px 16px rgba(255, 102, 0, 0.4)';
        });
        
        scrollToTopBtn.addEventListener('mouseout', () => {
            scrollToTopBtn.style.transform = 'scale(1)';
            scrollToTopBtn.style.boxShadow = '0 4px 12px rgba(255, 102, 0, 0.3)';
        });
        
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        document.body.appendChild(scrollToTopBtn);
        
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollToTopBtn.style.display = 'block';
            } else {
                scrollToTopBtn.style.display = 'none';
            }
        });
        
        // Уведомление о загрузке
        setTimeout(() => {
            const notification = document.createElement('div');
            notification.innerHTML = `
                <div style="
                    position: fixed;
                    top: 80px;
                    right: 20px;
                    background: linear-gradient(135deg, #000, #333);
                    color: #ff6600;
                    padding: 15px 20px;
                    border-radius: 8px;
                    border-left: 4px solid #ff6600;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    z-index: 1000;
                    max-width: 300px;
                    animation: slideIn 0.5s ease-out;
                ">
                    <strong>🎯 Документация загружена!</strong>
                    <div style="margin-top: 5px; font-size: 12px; color: #ccc;">
                        Используйте Try it out для тестирования API
                    </div>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.5s ease-out';
                setTimeout(() => notification.remove(), 500);
            }, 5000);
        }, 1000);
        
        // Добавляем стили для анимаций уведомлений
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    });
</script>
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

# 3. Endpoint для Swagger UI
@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="🚀 Intranet2.0 API Docs",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": 1,
            "defaultModelExpandDepth": 2,
            "defaultModelRendering": "model",
            "displayRequestDuration": True,
            "docExpansion": "list",
            "filter": True,
            "maxDisplayedTags": 20,
            "operationsSorter": "alpha",
            "tagsSorter": "alpha",
            "showExtensions": True,
            "showCommonExtensions": True,
            "tryItOutEnabled": True,
            "requestSnippetsEnabled": True,
            "persistAuthorization": True,
            "displayOperationId": False,
            "deepLinking": True,
            "syntaxHighlight": {
                "theme": "monokai"
            },
            "tryItOutEnabled": True,
            "displayRequestDuration": True,
            "requestSnippetsEnabled": True,
        }
    )
    
    # Добавляем кастомный заголовок
    custom_header = """
    <div class="custom-header">
        <h1>Intranet2.0 API Documentation</h1>
        <p>
            Welcome to the Intranet2.0 API documentation. This interactive documentation allows you to 
            explore all available endpoints, test API requests directly from your browser, and understand 
            how to integrate with our services. Use the <strong>Try it out</strong> buttons to test endpoints 
            with real data.
        </p>
    </div>
    """
    
    # Вставляем кастомный заголовок после wrapper
    html = re.sub(
        r'(<div class="swagger-ui"><div class="wrapper">)',
        r'\1' + custom_header,
        html
    )
    
    # Заменяем стандартные CSS стили
    html = html.replace(
        '<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css">',
        '<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css">\n' + CUSTOM_CSS
    )
    
    # Удаляем стандартную тему, если она есть
    html = re.sub(r'"theme":\s*{[^}]*}', '', html)
    
    return HTMLResponse(content=html)