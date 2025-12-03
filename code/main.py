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
    title="Intranet2.0 API DOCS",
    version="2.0.0",
    docs_url=None,#"/api/docs",
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

#templates = Jinja2Templates(directory="./src/services/templates") 

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
import markdown2



# Встроенный CSS стиль
# Кастомные стили
CUSTOM_CSS = """
<style>
    /* === ОСНОВНЫЕ ПЕРЕМЕННЫЕ И СБРОС === */
    :root {
        --accent: #f5821f;
        --accent-light: #ff9a42;
        --accent-dark: #d6690b;
        --text-primary: #d3d3d3;
        --text-secondary: #A5A5A5;
        --bg-main: rgb(19, 19, 19);
        --bg-block: #1b1b1b;
        --border-color: #f5821f;
        --border-light: #333333;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --info: #3b82f6;
    }

    /* === ОСНОВНОЙ ФОН И ТЕКСТ === */
    body {
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif !important;
        margin: 0 !important;
    }

    /* === КОНТЕЙНЕР SWAGGER UI === */
    .swagger-ui {
        background-color: var(--bg-main) !important;
        font-family: inherit !important;
    }

    .swagger-ui .wrapper {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 20px !important;
    }

    /* === ВЕРХНЯЯ ПАНЕЛЬ (TOP BAR) === */
    .swagger-ui .topbar {
        background-color: var(--bg-block) !important;
        border-bottom: 2px solid var(--border-color) !important;
        padding: 15px 0 !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5) !important;
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
        color: var(--accent) !important;
        font-size: 1.5em !important;
        font-weight: bold !important;
        text-decoration: none !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }

    .swagger-ui .topbar-wrapper .link::before {
        content: "📚";
        font-size: 1.3em;
    }

    /* === ЗАГОЛОВОК ИНФОРМАЦИОННОГО БЛОКА === */
    .swagger-ui .info .title {
        color: var(--accent) !important;
        font-size: 2.5em !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
        border-bottom: 2px solid var(--border-color) !important;
        padding-bottom: 15px !important;
    }

    .swagger-ui .info .title small {
        background-color: var(--accent) !important;
        color: var(--bg-main) !important;
        padding: 3px 10px !important;
        border-radius: 12px !important;
        font-size: 0.6em !important;
        margin-left: 15px !important;
        vertical-align: middle !important;
    }

    .swagger-ui .info .description p,
    .swagger-ui .info .description li {
        color: var(--text-primary) !important;
        line-height: 1.6 !important;
    }

    .swagger-ui .info .description h1,
    .swagger-ui .info .description h2,
    .swagger-ui .info .description h3,
    .swagger-ui .info .description h4 {
        color: var(--accent) !important;
        margin-top: 1.5em !important;
        border-left: 4px solid var(--accent) !important;
        padding-left: 10px !important;
    }

    /* === ТЕГИ (ГРУППЫ ЭНДПОИНТОВ) === */
    .swagger-ui .opblock-tag {
        color: var(--accent) !important;
        font-size: 1.3em !important;
        font-weight: 600 !important;
        background-color: var(--bg-block) !important;
        border: 1px solid var(--border-light) !important;
        border-left: 4px solid var(--accent) !important;
        border-radius: 8px !important;
        padding: 15px 20px !important;
        margin: 20px 0 !important;
        transition: all 0.3s ease !important;
    }

    .swagger-ui .opblock-tag:hover {
        background-color: #222222 !important;
        transform: translateX(5px) !important;
        cursor: pointer !important;
    }

    /* === БЛОКИ ОПЕРАЦИЙ (ENDPOINTS) === */
    .swagger-ui .opblock {
        background-color: var(--bg-block) !important;
        border: 1px solid var(--border-light) !important;
        border-left: 4px solid var(--accent) !important;
        border-radius: 8px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s ease !important;
    }

    .swagger-ui .opblock:hover {
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4) !important;
        transform: translateY(-2px) !important;
        border-left-color: var(--accent-light) !important;
    }

    .swagger-ui .opblock .opblock-summary {
        padding: 15px !important;
    }

    /* === МЕТОДЫ HTTP (GET, POST, ETC) === */
    .swagger-ui .opblock .opblock-summary-method {
        background-color: var(--accent) !important;
        color: var(--bg-main) !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        min-width: 70px !important;
        text-align: center !important;
        padding: 6px 0 !important;
        font-size: 0.9em !important;
        border: none !important;
    }

    /* Цвета для разных HTTP методов */
    .swagger-ui .opblock.opblock-get .opblock-summary-method {
        background-color: var(--accent) !important; /* GET - оранжевый */
    }
    .swagger-ui .opblock.opblock-post .opblock-summary-method {
        background-color: var(--success) !important; /* POST - зеленый */
    }
    .swagger-ui .opblock.opblock-put .opblock-summary-method {
        background-color: var(--warning) !important; /* PUT - желтый */
    }
    .swagger-ui .opblock.opblock-delete .opblock-summary-method {
        background-color: var(--error) !important; /* DELETE - красный */
    }
    .swagger-ui .opblock.opblock-patch .opblock-summary-method {
        background-color: var(--info) !important; /* PATCH - синий */
    }

    /* === ПУТЬ И ОПИСАНИЕ ЭНДПОИНТА === */
    .swagger-ui .opblock .opblock-summary-path {
        color: var(--text-primary) !important;
        font-size: 1.1em !important;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
        margin-left: 10px !important;
        font-weight: 500 !important;
    }

    .swagger-ui .opblock .opblock-summary-description {
        color: var(--text-secondary) !important;
        font-size: 0.9em !important;
        margin-top: 5px !important;
    }

    /* === КНОПКИ === */
    .swagger-ui .btn {
        background-color: var(--accent) !important;
        color: var(--bg-main) !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        padding: 8px 16px !important;
        font-size: 0.9em !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    .swagger-ui .btn:hover {
        background-color: var(--accent-light) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(245, 130, 31, 0.2) !important;
    }

    .swagger-ui .btn.execute {
        min-width: 80px !important;
    }

    /* === ПОЛЯ ВВОДА И СЕЛЕКТОРЫ === */
    .swagger-ui input[type="text"],
    .swagger-ui input[type="password"],
    .swagger-ui input[type="email"],
    .swagger-ui input[type="number"],
    .swagger-ui select,
    .swagger-ui textarea {
        background-color: var(--bg-block) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 4px !important;
        padding: 10px !important;
        font-size: 0.95em !important;
    }

    .swagger-ui input:focus,
    .swagger-ui select:focus,
    .swagger-ui textarea:focus {
        border-color: var(--accent) !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(245, 130, 31, 0.2) !important;
    }

    /* === ПАРАМЕТРЫ === */
    .swagger-ui .parameters-col_name {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }

    .swagger-ui .parameter__type {
        color: var(--accent) !important;
        font-weight: bold !important;
    }

    .swagger-ui .parameter__name {
        color: var(--text-secondary) !important;
    }

    /* === ОТВЕТЫ (RESPONSES) === */
    .swagger-ui .response-col_status {
        color: var(--accent) !important;
        font-weight: bold !important;
    }

    .swagger-ui .response-col_description {
        color: var(--text-secondary) !important;
    }

    /* === МОДЕЛИ ДАННЫХ === */
    .swagger-ui section.models {
        background-color: var(--bg-block) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
    }

    .swagger-ui .model-title {
        color: var(--accent) !important;
        font-weight: bold !important;
    }

    .swagger-ui .model {
        color: var(--text-secondary) !important;
    }

    /* === ТАБЛИЦЫ === */
    .swagger-ui table thead tr th,
    .swagger-ui table thead tr td {
        background-color: var(--bg-block) !important;
        color: var(--accent) !important;
        border-bottom: 2px solid var(--border-color) !important;
    }

    .swagger-ui table tbody tr {
        background-color: var(--bg-block) !important;
    }

    .swagger-ui table tbody tr td {
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--border-light) !important;
    }

    /* === ПАНЕЛЬ АВТОРИЗАЦИИ === */
    .swagger-ui .scheme-container {
        background-color: var(--bg-block) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        margin: 20px 0 !important;
        padding: 15px !important;
    }

    /* === СКРОЛЛБАР (CUSTOM) === */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-main);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-light);
    }

    /* === ДОПОЛНИТЕЛЬНЫЕ УЛУЧШЕНИЯ === */
    .swagger-ui .info .description .markdown code,
    .swagger-ui .opblock-description-wrapper .markdown code {
        background-color: var(--bg-block) !important;
        color: var(--accent) !important;
        border: 1px solid var(--border-light) !important;
        padding: 2px 5px !important;
        border-radius: 3px !important;
        font-family: monospace !important;
    }

    .swagger-ui .info .description,
    .swagger-ui .opblock .opblock-summary-description,
    .swagger-ui .model .model .property .description,
    .swagger-ui .parameter__description,
    .swagger-ui .response .response .description {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif !important;
        line-height: 1.6 !important;
        color: var(--text-primary) !important;
    }

    /* Заголовки */
    .swagger-ui .info .description h1,
    .swagger-ui .info .description h2,
    .swagger-ui .info .description h3,
    .swagger-ui .info .description h4,
    .swagger-ui .opblock .opblock-summary-description h1,
    .swagger-ui .opblock .opblock-summary-description h2,
    .swagger-ui .opblock .opblock-summary-description h3,
    .swagger-ui .opblock .opblock-summary-description h4 {
        color: var(--accent) !important;
        font-weight: 600 !important;
        margin: 1.5em 0 0.8em 0 !important;
        padding-bottom: 0.3em !important;
        border-bottom: 1px solid var(--border-light) !important;
    }

    .swagger-ui .info .description h1 {
        font-size: 2em !important;
        border-bottom-width: 2px !important;
        border-bottom-color: var(--accent) !important;
    }

    .swagger-ui .info .description h2 {
        font-size: 1.5em !important;
    }

    /* Параграфы и текст */
    .swagger-ui .info .description p {
        margin: 1em 0 !important;
        color: var(--text-primary) !important;
    }

    .swagger-ui .info .description strong {
        color: var(--accent) !important;
        font-weight: 600 !important;
    }

    .swagger-ui .info .description em {
        font-style: italic !important;
        color: var(--text-secondary) !important;
    }

    /* Списки */
    .swagger-ui .info .description ul,
    .swagger-ui .info .description ol {
        margin: 1em 0 1em 2em !important;
        color: var(--text-primary) !important;
    }

    .swagger-ui .info .description li {
        margin: 0.5em 0 !important;
        line-height: 1.5 !important;
    }

    .swagger-ui .info .description ul li {
        list-style-type: disc !important;
    }

    .swagger-ui .info .description ol li {
        list-style-type: decimal !important;
    }

    /* Блоки кода (inline) */
    .swagger-ui .info .description code,
    .swagger-ui .opblock .opblock-summary-description code {
        background-color: var(--bg-block) !important;
        color: var(--accent) !important;
        padding: 0.2em 0.4em !important;
        border-radius: 3px !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace !important;
        font-size: 0.9em !important;
        border: 1px solid var(--border-light) !important;
    }

    /* Блоки кода (fenced code blocks) */
    .swagger-ui .info .description pre,
    .swagger-ui .opblock .opblock-summary-description pre {
        background-color: var(--bg-block) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 6px !important;
        padding: 16px !important;
        margin: 1em 0 !important;
        overflow-x: auto !important;
    }

    .swagger-ui .info .description pre code,
    .swagger-ui .opblock .opblock-summary-description pre code {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        color: var(--text-primary) !important;
        font-size: 0.9em !important;
        line-height: 1.5 !important;
    }

    /* Подсветка синтаксиса (если установлен pygments) */
    .swagger-ui .info .description .highlight,
    .swagger-ui .opblock .opblock-summary-description .highlight {
        background-color: var(--bg-block) !important;
        border-radius: 6px !important;
        padding: 1px !important;
    }

    /* Таблицы */
    .swagger-ui .info .description table,
    .swagger-ui .opblock .opblock-summary-description table {
        border-collapse: collapse !important;
        margin: 1em 0 !important;
        width: 100% !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 6px !important;
        overflow: hidden !important;
    }

    .swagger-ui .info .description table th,
    .swagger-ui .opblock .opblock-summary-description table th {
        background-color: rgba(245, 130, 31, 0.1) !important;
        color: var(--accent) !important;
        font-weight: 600 !important;
        padding: 12px !important;
        text-align: left !important;
        border-bottom: 2px solid var(--border-light) !important;
    }

    .swagger-ui .info .description table td,
    .swagger-ui .opblock .opblock-summary-description table td {
        padding: 10px 12px !important;
        border-bottom: 1px solid var(--border-light) !important;
        color: var(--text-primary) !important;
    }

    .swagger-ui .info .description table tr:last-child td,
    .swagger-ui .opblock .opblock-summary-description table tr:last-child td {
        border-bottom: none !important;
    }

    /* Цитаты */
    .swagger-ui .info .description blockquote,
    .swagger-ui .opblock .opblock-summary-description blockquote {
        margin: 1em 0 !important;
        padding: 0.5em 1em !important;
        border-left: 4px solid var(--accent) !important;
        background-color: rgba(245, 130, 31, 0.05) !important;
        color: var(--text-secondary) !important;
        font-style: italic !important;
        border-radius: 0 4px 4px 0 !important;
    }

    /* Горизонтальные линии */
    .swagger-ui .info .description hr,
    .swagger-ui .opblock .opblock-summary-description hr {
        height: 1px !important;
        background-color: var(--border-light) !important;
        border: none !important;
        margin: 2em 0 !important;
    }

    /* Списки задач (task lists) */
    .swagger-ui .info .description .task-list-item,
    .swagger-ui .opblock .opblock-summary-description .task-list-item {
        list-style-type: none !important;
        margin-left: -1.5em !important;
    }

    .swagger-ui .info .description .task-list-item-checkbox,
    .swagger-ui .opblock .opblock-summary-description .task-list-item-checkbox {
        margin-right: 0.5em !important;
    }

    /* Зачеркнутый текст */
    .swagger-ui .info .description del,
    .swagger-ui .opblock .opblock-summary-description del {
        color: var(--text-secondary) !important;
        text-decoration: line-through !important;
    }

    /* Ссылки */
    .swagger-ui .info .description a,
    .swagger-ui .opblock .opblock-summary-description a {
        color: var(--accent) !important;
        text-decoration: none !important;
        border-bottom: 1px dotted var(--accent) !important;
        transition: all 0.2s ease !important;
    }

    .swagger-ui .info .description a:hover,
    .swagger-ui .opblock .opblock-summary-description a:hover {
        border-bottom-style: solid !important;
        color: var(--accent-light) !important;
    }

    /* Иконки для списков */
    .swagger-ui .info .description ul li:before {
        color: var(--accent) !important;
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
        print("[DEBUG] Возвращаю закешированную схему.")
        return app.openapi_schema
    
    print("[DEBUG] Генерирую новую кастомную OpenAPI схему...")
    openapi_schema = get_openapi(
        title="Intranet2.0 API Docs",
        version="2.0.0",
        description="""
        Добро пожаловать!
            Добро пожаловать!
        Тут проедставлена документация к ресурсам REST API, реализованного с помощью Python3 Fastapi, для внутреннего функционирования веб-сервиса Intranet2.0!

        Особенности проекта:
            - Модульная структура
            - Аснхронность
            - Взаимодействие 3х Баз Данных
        """,
        routes=app.routes,
        openapi_version="3.0.3"  # Убедитесь, что тут 3.0.3!
    )
    
    # ВАЖНО: Напечатайте начало схемы для проверки
    import json
    schema_preview = json.dumps(openapi_schema, indent=2, ensure_ascii=False)[:500]
    print(f"[DEBUG] Первые 500 символов схемы:\n{schema_preview}")

    # Преобразуем Markdown описания в HTML
    openapi_schema = convert_markdown_in_schema(openapi_schema)
    
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
    # 1. Получаем объект HTMLResponse от стандартной функции
    response_obj = get_swagger_ui_html(
        openapi_url="/api/openapi.json",
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
            "syntaxHighlight": {"theme": "monokai"},
            "tryItOutEnabled": True,
            "displayRequestDuration": True,
            "requestSnippetsEnabled": True,
        }
    )
    
    # 2. Извлекаем тело HTML как строку
    html_content = response_obj.body.decode("utf-8")
    
    # 3. Добавляем кастомный заголовок
    custom_header = """
    <div style="
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        padding: 20px;
        margin-bottom: 30px;
        border-radius: 8px;
        border-left: 6px solid #ff6600;
    ">
        <h1 style="color: #ff6600; margin: 0 0 10px 0;">🚀 Intranet2.0 API Documentation</h1>
        <p style="color: #ffffff; margin: 0; font-size: 16px;">
            Welcome to the Intranet2.0 API documentation. Explore available endpoints, test requests, 
            and integrate with our services.
        </p>
    </div>
    """
    
    # 4. Вставляем кастомный заголовок в HTML (используйте вашу логику)
    # Вариант A: Замена через re.sub (как у вас)
    modified_html = re.sub(
        r'(<div class="swagger-ui"><div class="wrapper">)',
        r'\1' + custom_header,
        html_content
    )
    
    # ИЛИ Вариант B: Более простой способ через replace
    # modified_html = html_content.replace(
    #     '<div class="swagger-ui"><div class="wrapper">',
    #     '<div class="swagger-ui"><div class="wrapper">' + custom_header
    # )
    
    # 5. Добавляем кастомные стили в head
    modified_html = modified_html.replace('</head>', CUSTOM_CSS + '</head>')
    
    # 6. Возвращаем новый объект HTMLResponse с модифицированным содержимым
    return HTMLResponse(content=modified_html)

def markdown_to_html(text: str) -> str:
    """Преобразует Markdown в HTML с поддержкой GitHub-стиля."""
    if not text or not HAS_MARKDOWN2:
        return text
    
    try:
        # Используем markdown2 с расширениями для GitHub-стиля
        html = markdown2.markdown(
            text,
            extras=[
                "fenced-code-blocks",    # Блоки кода с ```
                "code-friendly",         # Не преобразовывать подчеркивания в em/strong
                "tables",                # Поддержка таблиц
                "break-on-newline",      # Разрывы строк
                "cuddled-lists",         # Списки без пустых строк
                "task_list",             # Списки задач [x]
                "strike",                # Зачеркнутый текст
                "highlight",             # == Подсветка синтаксиса (нужен pygments)
            ]
        )
        return html.strip()
    except Exception as e:
        print(f"⚠️  Ошибка преобразования Markdown: {e}")
        return text

def process_description(obj: Any) -> Any:
    """Рекурсивно обрабатывает все описания в объекте."""
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if key in ["description", "summary", "title"] and isinstance(value, str):
                # Преобразуем Markdown в HTML для полей описания
                result[key] = markdown_to_html(value)
            else:
                result[key] = process_description(value)
        return result
    elif isinstance(obj, list):
        return [process_description(item) for item in obj]
    else:
        return obj

def convert_markdown_in_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Конвертирует все Markdown описания в OpenAPI схеме в HTML."""
    if not HAS_MARKDOWN2:
        return schema
    
    print("🔄 Преобразую Markdown описания в HTML...")
    return process_description(schema)