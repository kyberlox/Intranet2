from fastapi import FastAPI, APIRouter, Body, Request, UploadFile, HTTPException, Response, Request
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks #, Cookie, Header
from fastapi.responses import Response, JSONResponse#, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request, HTTPException, status
from fastapi.routing import APIRoute



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
from datetime import datetime

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

b24_docs_routs = [
    "/api/users_depart"
]


for route in app.routes:
    print(route, route.path)
    if isinstance(route, APIRoute) and route.path in b24_docs_routs:
        print("SWDFGHJKL:", route)
        if hasattr(route, 'tags'):
            if "Битрикс24" not in route.tags:
                route.tags.append("Битрикс24")
                print(route.tags, route.path)


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

    

    # for open_link in open_links:
    #     if open_link in request.url.path:
    #         return await call_next(request)

            # try:
            #     #return call_next(request)
            #     print('тут')
            #     return await call_next(request)
            # except:
            #     return JSONResponse(
            #         status_code = status.HTTP_401_UNAUTHORIZED,
            #         content = log.warning_message(message="Error when trying to follow the link without authorization")
            #     )



    # Проверяем, является ли текущий путь публичным
    for open_link in open_links:
        if open_link in request.url.path:
            return await call_next(request)
    
    # Проверяем авторизацию для всех остальных /api эндпоинтов
    if request.url.path.startswith("/api"):
        # Создаем экземпляр сервиса авторизации
        auth_service = AuthService()
        
        # Получаем session_id из куков или заголовков
        session_id = request.cookies.get("session_id")
        
        if not session_id:
            # Проверяем заголовок Authorization с префиксом Bearer
            auth_header = request.headers.get("session_id")
            if auth_header and auth_header.startswith("Bearer "):
                session_id = auth_header[7:]
        
        if not session_id:
            log.warning_message(message="Authorization cookies or headers missing")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "message": "Authorization required. Please login first.",
                    "auth_url": await auth_service.get_auth_url()
                }
            )
        
        try:
            # Проверяем и обновляем сессию при необходимости
            session_data = auth_service.validate_and_refresh_session(session_id)
            
            if not session_data:
                log.warning_message(message="Invalid or expired session")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "status": "error",
                        "message": "Session expired or invalid. Please login again.",
                        "auth_url": await auth_service.get_auth_url()
                    }
                )
            
            # Проверяем, что access_token еще валиден
            access_token_expires_at = datetime.fromisoformat(
                session_data.get("access_token_expires_at")
            )
            now = datetime.now()
            
            if now > access_token_expires_at:
                # Попытка обновить токен
                refreshed = await auth_service.refresh_access_token(
                    session_data.get("refresh_token")
                )
                
                if not refreshed:
                    log.warning_message(message="Failed to refresh access token")
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "status": "error",
                            "message": "Authentication failed. Please login again.",
                            "auth_url": await auth_service.get_auth_url()
                        }
                    )
                
                # Обновляем данные сессии
                session_data["access_token"] = refreshed["access_token"]
                session_data["access_token_expires_at"] = refreshed["access_token_expires_at"]
                session_data["member_id"] = refreshed["member_id"]
                
                if "refresh_token" in refreshed:
                    session_data["refresh_token"] = refreshed["refresh_token"]
                    session_data["refresh_token_expires_at"] = refreshed["refresh_token_expires_at"]
                
                # Сохраняем обновленную сессию
                auth_service.redis.save_session(
                    key=session_id,
                    data=session_data,
                    ttl=int(auth_service.session_ttl.total_seconds())
                )
            
            # Добавляем информацию о пользователе в request.state для использования в эндпоинтах
            request.state.user_id = session_data.get("user_id")
            request.state.user_info = session_data.get("user_info")
            request.state.session_id = session_id
            request.state.access_token = session_data.get("access_token")
            
            # Логируем успешную аутентификацию (опционально)
            log.info_message(f"User {session_data.get('user_id')} accessed {request.url.path}")
            
        except Exception as e:
            log.error_message(f"Authentication error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status": "error",
                    "message": "Authentication error occurred.",
                    "auth_url": await auth_service.get_auth_url()
                }
            )
    
    # Обрабатываем запрос
    response = await call_next(request)
    
    # После обработки запроса можем обновить куки сессии, если нужно
    if request.url.path.startswith("/api"):
        # Проверяем, есть ли session_id в state (если пользователь авторизован)
        if hasattr(request.state, 'session_id'):
            # Обновляем время последней активности в Redis
            session_id = request.state.session_id
            session_data = auth_service.redis.get_session(session_id)
            
            if session_data:
                now = datetime.now()
                session_data["last_activity"] = now.isoformat()
                
                # Применяем скользящее окно: продлеваем сессию если с последней активности прошло больше N минут
                last_activity = datetime.fromisoformat(session_data["last_activity"])
                if now > last_activity + auth_service.session_sliding_window:
                    session_data["session_expires_at"] = (now + auth_service.session_ttl).isoformat()
                    
                    auth_service.redis.save_session(
                        key=session_id,
                        data=session_data,
                        ttl=int(auth_service.session_ttl.total_seconds())
                    )
                    
                    # Обновляем куки у клиента
                    response.set_cookie(
                        key="session_id",
                        value=session_id,
                        httponly=True,
                        secure=True,  # Использовать только с HTTPS
                        samesite="lax",
                        max_age=int(auth_service.session_ttl.total_seconds())
                    )
                    # response.set_cookie(
                    #     key="has",
                    #     value=session_id,
                    #     httponly=True,
                    #     secure=True,  # Использовать только с HTTPS
                    #     samesite="lax",
                    #     max_age=int(auth_service.session_ttl.total_seconds())
                    # )
    
    
    return response



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
from typing import Any, Dict, Optional
from html import escape

HAS_MARKDOWN2=True



# Кастомные стили
CUSTOM_CSS = """
<style>
    /* === ОБНОВЛЁННЫЕ ЦВЕТОВЫЕ ПЕРЕМЕННЫЕ === */
    :root {
        /* Акцентные цвета (оранжевые) */
        --accent: #f5821f;
        --accent-light: #ff9a42;
        --accent-dark: #d6690b;
        
        /* Текст - ВСЕ БЕЛЫЙ для максимальной читаемости */
        --text-primary: #ffffff;           /* Основной текст - чистый белый */
        --text-secondary: #ffffff;         /* Вторичный текст - тоже белый */
        --text-muted: #ffffff;             /* Приглушенный текст - белый с прозрачностью */
        
        /* Фоны */
        --bg-main: rgb(35, 35, 35);        /* Ещё светлее основной фон */
        --bg-block: #2d2d2d;               /* Более светлый фон блоков */
        --bg-card: #363636;                /* Самый светлый фон для карточек */
        
        /* Границы */
        --border-color: #f5821f;
        --border-light: #505050;           /* Светлые границы */
        --border-soft: #444444;
        
        /* Статусные цвета */
        --success: #4caf50;
        --warning: #ff9800;
        --error: #f44336;
        --info: #2196f3;
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
        color: var(--text-primary) !important;
    }

    .swagger-ui .wrapper {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 20px !important;
        background-color: var(--bg-main) !important;
    }

    /* === ВЕРХНЯЯ ПАНЕЛЬ === */
    .swagger-ui .topbar {
        background-color: var(--bg-block) !important;
        border-bottom: 2px solid var(--border-color) !important;
        padding: 15px 0 !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
    }

    .swagger-ui .topbar-wrapper .link {
        color: var(--accent) !important;
        font-size: 1.5em !important;
        font-weight: bold !important;
    }

    /* === ОПИСАНИЯ В SWAGGER UI - ВСЁ БЕЛОЕ! === */
    
    /* Основные описания */
    .swagger-ui .info .description *,
    .swagger-ui .info .description,
    .swagger-ui .opblock .opblock-summary-description *,
    .swagger-ui .opblock .opblock-summary-description,
    .swagger-ui .opblock .opblock-summary-description p,
    .swagger-ui .opblock .opblock-summary-description li,
    .swagger-ui .opblock .opblock-summary-description span,
    .swagger-ui .opblock .opblock-summary-description div,
    .swagger-ui .opblock .opblock-summary-description strong,
    .swagger-ui .opblock .opblock-summary-description em {
        color: var(--text-primary) !important;  /* БЕЛЫЙ! */
    }

    /* Параграфы в описаниях */
    .swagger-ui .info .description p,
    .swagger-ui .opblock .opblock-summary-description p {
        color: var(--text-primary) !important;
        margin: 1em 0 !important;
        line-height: 1.6 !important;
    }

    /* Списки в описаниях - КРИТИЧНО ВАЖНО! */
    .swagger-ui .info .description ul,
    .swagger-ui .info .description ol,
    .swagger-ui .opblock .opblock-summary-description ul,
    .swagger-ui .opblock .opblock-summary-description ol {
        color: var(--text-primary) !important;
        margin: 1em 0 1em 2em !important;
    }

    .swagger-ui .info .description li,
    .swagger-ui .opblock .opblock-summary-description li {
        color: var(--text-primary) !important;
        margin: 0.5em 0 !important;
        line-height: 1.5 !important;
        list-style-type: disc !important;
    }

    /* Элементы списков (маркеры) */
    .swagger-ui .info .description li::marker,
    .swagger-ui .opblock .opblock-summary-description li::marker {
        color: var(--accent) !important;
    }

    /* Заголовки в описаниях */
    .swagger-ui .info .description h1,
    .swagger-ui .info .description h2,
    .swagger-ui .info .description h3,
    .swagger-ui .info .description h4,
    .swagger-ui .info .description h5,
    .swagger-ui .info .description h6,
    .swagger-ui .opblock .opblock-summary-description h1,
    .swagger-ui .opblock .opblock-summary-description h2,
    .swagger-ui .opblock .opblock-summary-description h3,
    .swagger-ui .opblock .opblock-summary-description h4,
    .swagger-ui .opblock .opblock-summary-description h5,
    .swagger-ui .opblock .opblock-summary-description h6 {
        color: var(--accent) !important;
        font-weight: 600 !important;
        margin: 1.5em 0 0.8em 0 !important;
        padding-bottom: 0.3em !important;
        border-bottom: 1px solid var(--border-light) !important;
    }

    /* Жирный текст в описаниях */
    .swagger-ui .info .description strong,
    .swagger-ui .opblock .opblock-summary-description strong {
        color: var(--accent) !important;
        font-weight: 600 !important;
    }

    /* Курсив в описаниях */
    .swagger-ui .info .description em,
    .swagger-ui .opblock .opblock-summary-description em {
        color: var(--text-primary) !important;
        font-style: italic !important;
        opacity: 0.9 !important;
    }

    /* Ссылки в описаниях */
    .swagger-ui .info .description a,
    .swagger-ui .opblock .opblock-summary-description a {
        color: var(--accent-light) !important;
        text-decoration: none !important;
        border-bottom: 1px dotted var(--accent) !important;
        transition: all 0.2s ease !important;
    }

    .swagger-ui .info .description a:hover,
    .swagger-ui .opblock .opblock-summary-description a:hover {
        border-bottom-style: solid !important;
        color: var(--accent) !important;
    }

    /* === ЗАГОЛОВОК ИНФОРМАЦИОННОГО БЛОКА === */
    .swagger-ui .info .title {
        color: var(--accent) !important;
        font-size: 2.5em !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
        border-bottom: 2px solid var(--border-color) !important;
        padding-bottom: 15px !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
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
    }

    /* === БЛОКИ ОПЕРАЦИЙ (ENDPOINTS) === */
    .swagger-ui .opblock {
        background-color: var(--bg-block) !important;
        border: 1px solid var(--border-light) !important;
        border-left: 4px solid var(--accent) !important;
        border-radius: 8px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }

    /* Методы HTTP */
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

    /* Путь и описание эндпоинта */
    .swagger-ui .opblock .opblock-summary-path {
        color: var(--text-primary) !important;
        font-size: 1.1em !important;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
        margin-left: 10px !important;
        font-weight: 500 !important;
    }

    /* Описание эндпоинта - теперь отдельный блок */
    .swagger-ui .opblock .opblock-summary-description {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
        padding: 15px !important;
        margin-top: 10px !important;
        font-size: 0.95em !important;
        line-height: 1.6 !important;
        max-height: 300px !important;
        overflow-y: auto !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
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
    }

    /* === ПОЛЯ ВВОДА И СЕЛЕКТОРЫ === */
    .swagger-ui input[type="text"],
    .swagger-ui input[type="password"],
    .swagger-ui input[type="email"],
    .swagger-ui input[type="number"],
    .swagger-ui select,
    .swagger-ui textarea {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 4px !important;
        padding: 10px !important;
        font-size: 0.95em !important;
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

    /* === БЛОКИ КОДА (Markdown -> HTML) === */
    /* Inline код */
    .swagger-ui .info .description code:not(pre samp),
    .swagger-ui .opblock .opblock-summary-description code:not(pre samp) {
        background-color: rgba(245, 130, 31, 0.15) !important;
        color: var(--accent-light) !important;
        padding: 0.2em 0.4em !important;
        border-radius: 3px !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace !important;
        font-size: 0.9em !important;
        border: 1px solid rgba(245, 130, 31, 0.3) !important;
    }

    /* Блоки кода в <samp> тегах */
    .swagger-ui .info .description pre,
    .swagger-ui .opblock .opblock-summary-description pre {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 6px !important;
        padding: 16px !important;
        margin: 1.2em 0 !important;
        overflow-x: auto !important;
        position: relative !important;
    }

    /* Красивая левая полоска для блоков кода */
    .swagger-ui .info .description pre::before,
    .swagger-ui .opblock .opblock-summary-description pre::before {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        bottom: 0 !important;
        width: 4px !important;
        background: linear-gradient(to bottom, var(--accent), var(--accent-light)) !important;
        border-radius: 6px 0 0 6px !important;
    }

    /* Сам текст кода внутри <samp> */
    .swagger-ui .info .description pre samp,
    .swagger-ui .opblock .opblock-summary-description pre samp {
        display: block !important;
        background-color: transparent !important;
        color: var(--text-primary) !important;
        padding: 0 !important;
        margin: 0 !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace !important;
        font-size: 0.9em !important;
        line-height: 1.5 !important;
        white-space: pre !important;
        word-break: normal !important;
        word-wrap: normal !important;
        overflow-x: visible !important;
    }

    /* Стили для HTTP подсветки */
    .http-method {
        color: var(--accent-light) !important;
        font-weight: bold !important;
        text-shadow: 0 0 1px rgba(245, 130, 31, 0.5) !important;
    }

    .http-path {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }

    .http-header {
        color: #4caf50 !important;
        font-style: italic !important;
    }

    .http-url {
        color: #64b5f6 !important;
        text-decoration: underline !important;
        text-decoration-color: rgba(100, 181, 246, 0.4) !important;
    }

    /* === СКРОЛЛБАРЫ === */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-block);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 5px;
        border: 2px solid var(--bg-main);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-light);
    }

    .swagger-ui section h3 {
        color: #ffffff;
        font-family: sans-serif;
    }

    .swagger-ui section h2 {
        color: #ffffff;
        font-family: sans-serif;
    }

    .swagger-ui section h1 {
        color: #ffffff;
        font-family: sans-serif;
    }

    .swagger-ui .opblock-description-wrapper p {
        color: #ffffff;
        font-family: sans-serif;
    }

    /* Специальный скроллбар для блоков кода */
    .swagger-ui .info .description pre::-webkit-scrollbar,
    .swagger-ui .opblock .opblock-summary-description pre::-webkit-scrollbar {
        height: 8px !important;
    }

    .swagger-ui .info .description pre::-webkit-scrollbar-track,
    .swagger-ui .opblock .opblock-summary-description pre::-webkit-scrollbar-track {
        background: var(--bg-block) !important;
        border-radius: 4px !important;
        margin: 0 4px !important;
    }

    .swagger-ui .info .description pre::-webkit-scrollbar-thumb,
    .swagger-ui .opblock .opblock-summary-description pre::-webkit-scrollbar-thumb {
        background: linear-gradient(to right, var(--accent), var(--accent-light)) !important;
        border-radius: 4px !important;
        border: 2px solid var(--bg-card) !important;
    }

    /* === ТЕМНЫЕ ЭЛЕМЕНТЫ SWAGGER UI === */
    /* Секции с деталями запроса */
    .swagger-ui .opblock .opblock-section-header {
        background-color: var(--bg-card) !important;
        border-bottom: 1px solid var(--border-light) !important;
    }

    .swagger-ui .opblock .opblock-section-header h4 {
        color: var(--text-primary) !important;
    }

    /* Вкладки (табы) */
    .swagger-ui .tab {
        color: var(--text-secondary) !important;
        border-bottom: 2px solid transparent !important;
    }

    .swagger-ui .tab:hover {
        background-color: rgba(245, 130, 31, 0.1) !important;
        color: var(--accent) !important;
    }

    .swagger-ui .tab.active {
        border-bottom-color: var(--accent) !important;
        color: var(--accent) !important;
        font-weight: bold !important;
    }

    /* === ДОПОЛНИТЕЛЬНЫЕ УЛУЧШЕНИЯ === */
    
    /* Делаем фон описаний API ещё светлее */
    .swagger-ui .info {
        background-color: var(--bg-block) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 10px !important;
        padding: 25px !important;
        margin: 20px 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }

    /* Выделяем маркеры списков акцентным цветом */
    .swagger-ui .info .description ul li::before {
        content: "•" !important;
        color: var(--accent) !important;
        font-size: 1.2em !important;
        margin-right: 8px !important;
        vertical-align: middle !important;
    }

    /* Разделители между пунктами в списках */
    .swagger-ui .info .description li {
        border-left: 2px solid rgba(245, 130, 31, 0.2) !important;
        padding-left: 10px !important;
        margin-left: -10px !important;
    }

    /* Особое выделение для блоков с примерами */
    .swagger-ui .opblock .opblock-summary-description h3 {
        background: linear-gradient(90deg, rgba(245, 130, 31, 0.1), transparent) !important;
        padding: 8px 15px !important;
        border-radius: 6px !important;
        margin-top: 20px !important;
    }
    /* === СТИЛИ ДЛЯ ОБРАБОТАННОГО MARKDOWN === */

    /* Заголовки в описаниях */
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
        margin: 1em 0 0.5em 0 !important;
        padding-bottom: 0.3em !important;
        border-bottom: 1px solid var(--border-light) !important;
    }

    /* Параграфы */
    .swagger-ui .info .description p,
    .swagger-ui .opblock .opblock-summary-description p {
        color: var(--text-primary) !important;
        margin: 0.8em 0 !important;
        line-height: 1.6 !important;
    }

    /* Списки */
    .swagger-ui .info .description ul,
    .swagger-ui .opblock .opblock-summary-description ul {
        color: var(--text-primary) !important;
        margin: 0.8em 0 0.8em 1.5em !important;
        padding-left: 0 !important;
    }

    .swagger-ui .info .description li,
    .swagger-ui .opblock .opblock-summary-description li {
        color: var(--text-primary) !important;
        margin: 0.4em 0 !important;
        line-height: 1.5 !important;
        list-style-type: disc !important;
    }

    /* Жирный текст */
    .swagger-ui .info .description strong,
    .swagger-ui .opblock .opblock-summary-description strong {
        color: var(--accent) !important;
        font-weight: 600 !important;
    }

    /* Курсив */
    .swagger-ui .info .description em,
    .swagger-ui .opblock .opblock-summary-description em {
        font-style: italic !important;
        opacity: 0.9 !important;
    }

    /* Inline код */
    .swagger-ui .info .description code.inline-code,
    .swagger-ui .opblock .opblock-summary-description code.inline-code {
        background-color: rgba(245, 130, 31, 0.15) !important;
        color: var(--accent-light) !important;
        padding: 0.2em 0.4em !important;
        border-radius: 3px !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace !important;
        font-size: 0.9em !important;
        border: 1px solid rgba(245, 130, 31, 0.3) !important;
    }

    /* Блоки кода, созданные JavaScript */
    .code-block-container {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
        margin: 1em 0 !important;
        overflow: hidden !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }

    .code-header {
        background: linear-gradient(90deg, rgba(245, 130, 31, 0.1), rgba(245, 130, 31, 0.05)) !important;
        border-bottom: 1px solid var(--border-light) !important;
        padding: 10px 15px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
    }

    .language-badge {
        background-color: var(--accent) !important;
        color: var(--bg-main) !important;
        font-size: 0.75em !important;
        font-weight: bold !important;
        padding: 4px 10px !important;
        border-radius: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .copy-code-btn {
        background-color: rgba(245, 130, 31, 0.2) !important;
        color: var(--accent) !important;
        border: 1px solid rgba(245, 130, 31, 0.3) !important;
        border-radius: 6px !important;
        padding: 6px 12px !important;
        font-size: 0.8em !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        transition: all 0.2s ease !important;
    }

    .copy-code-btn:hover {
        background-color: rgba(245, 130, 31, 0.3) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(245, 130, 31, 0.2) !important;
    }

    .code-block-container pre {
        background-color: var(--bg-block) !important;
        margin: 0 !important;
        padding: 16px !important;
        overflow-x: auto !important;
    }

    .code-block-container code {
        display: block !important;
        color: var(--text-primary) !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace !important;
        font-size: 0.9em !important;
        line-height: 1.5 !important;
        white-space: pre !important;
    }

    /* Подсветка HTTP */
    .http-method-highlight {
        color: var(--accent) !important;
        font-weight: bold !important;
    }

    .http-path {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
</style>

<script>
    // === ОСНОВНАЯ ФУНКЦИЯ ОБРАБОТКИ MARKDOWN ===

    function initMarkdownProcessing() {
        console.log("🚀 Инициализирую обработку Markdown...");
        
        // Обрабатываем сразу при загрузке
        processAllMarkdown();
        
        // Наблюдатель за изменениями DOM
        setupMutationObserver();
        
        // Обработчик кликов
        document.addEventListener('click', handleSwaggerClick);
    }

    function processAllMarkdown() {
        console.log("🔍 Ищу элементы с Markdown...");
        
        // 1. Основное описание API
        const infoElement = document.querySelector('.swagger-ui .info .description');
        if (infoElement) {
            console.log("Найдено основное описание");
            processElementMarkdown(infoElement);
        }
        
        // 2. Описания всех эндпоинтов
        const endpointDescriptions = document.querySelectorAll('.swagger-ui .opblock .opblock-summary-description');
        console.log(`Найдено описаний эндпоинтов: ${endpointDescriptions.length}`);
        
        endpointDescriptions.forEach((desc, index) => {
            if (desc.textContent && (desc.textContent.includes('[CODE_BLOCK') || desc.textContent.includes('###'))) {
                console.log(`Обрабатываю описание ${index + 1}`);
                processElementMarkdown(desc);
            }
        });
        
        // 3. Все элементы с классом markdown
        const markdownElements = document.querySelectorAll('.swagger-ui .markdown, .swagger-ui .renderedMarkdown');
        markdownElements.forEach(el => {
            if (el.textContent && el.textContent.includes('[CODE_BLOCK')) {
                processElementMarkdown(el);
            }
        });
        
        console.log("✅ Обработка завершена");
    }

    function processElementMarkdown(element) {
        if (!element || !element.textContent) return;
        
        const originalText = element.textContent;
        
        // Проверяем, нужно ли обрабатывать
        if (!originalText.includes('[CODE_BLOCK') && 
            !originalText.includes('### ') && 
            !originalText.includes('## ') && 
            !originalText.includes('# ') &&
            !originalText.includes('**')) {
            return; // Нет Markdown разметки
        }
        
        console.log("📝 Обрабатываю элемент:", originalText.substring(0, 100) + "...");
        
        const html = convertMarkdownToHtml(originalText);
        element.innerHTML = html;
        
        // Инициализируем кнопки копирования в новых блоках кода
        initCopyButtons();
    }

    function convertMarkdownToHtml(text) {
        if (!text) return '';
        
        let html = text;
        
        // 1. Обрабатываем блоки кода [CODE_BLOCK language="..."]...[/CODE_BLOCK]
        const codeBlockRegex = /\[CODE_BLOCK\s+language="([^"]+)"\]([\s\S]*?)\[\/CODE_BLOCK\]/g;
        
        html = html.replace(codeBlockRegex, function(match, language, codeContent) {
            console.log(`Найден блок кода с языком: ${language}`);
            
            // Очищаем код
            codeContent = codeContent.trim();
            
            // Определяем отображаемое имя языка
            let langDisplay = language.toUpperCase();
            if (language === 'text' || language === '') {
                // Автоматически определяем HTTP
                const firstLine = codeContent.split('\\n')[0];
                const httpMethods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'];
                const isHttp = httpMethods.some(method => 
                    firstLine.toUpperCase().includes(method.toUpperCase())
                );
                
                if (isHttp) {
                    langDisplay = 'HTTP';
                    language = 'http';
                } else {
                    langDisplay = 'CODE';
                }
            }
            
            // Экранируем HTML в коде
            const escapedCode = codeContent
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
            
            // Подсвечиваем HTTP методы если это HTTP
            let highlightedCode = escapedCode;
            if (language === 'http') {
                highlightedCode = highlightHttpMethods(escapedCode);
            }
            
            // Создаем уникальный ID для блока
            const blockId = 'code-block-' + Math.random().toString(36).substr(2, 9);
            
            return `
            <div id="${blockId}" class="code-block-container" data-language="${language}">
                <div class="code-header">
                    <span class="language-badge">${langDisplay}</span>
                    <button class="copy-code-btn" data-target="${blockId}">
                        <span class="copy-icon">📋</span>
                        <span class="copy-text">Копировать</span>
                    </button>
                </div>
                <pre><code class="language-${language}">${highlightedCode}</code></pre>
            </div>
            `;
        });
        
        // 2. Обрабатываем заголовки
        html = html.replace(/^###\s+(.*)$/gim, '<h3 class="markdown-h3">$1</h3>');
        html = html.replace(/^##\s+(.*)$/gim, '<h2 class="markdown-h2">$1</h2>');
        html = html.replace(/^#\s+(.*)$/gim, '<h1 class="markdown-h1">$1</h1>');
        
        // 3. Обрабатываем жирный текст (**текст**)
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        // 4. Обрабатываем курсив (*текст*)
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        
        // 5. Обрабатываем списки (начинающиеся с -)
        // Сначала находим все строки со списками
        const lines = html.split('\\n');
        let inList = false;
        let listHtml = '';
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            
            if (line.startsWith('- ')) {
                if (!inList) {
                    inList = true;
                    listHtml += '<ul class="markdown-list">';
                }
                const itemText = line.substring(2);
                listHtml += `<li class="markdown-list-item">${itemText}</li>`;
            } else {
                if (inList) {
                    inList = false;
                    listHtml += '</ul>';
                }
                listHtml += line + '\\n';
            }
        }
        
        if (inList) {
            listHtml += '</ul>';
        }
        
        html = listHtml;
        
        // 6. Обрабатываем inline код (`code`)
        html = html.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
        
        // 7. Заменяем двойные переносы на параграфы
        html = html.replace(/\\n\\n/g, '</p><p class="markdown-p">');
        html = '<p class="markdown-p">' + html + '</p>';
        
        // 8. Убираем пустые параграфы
        html = html.replace(/<p class="markdown-p"><\/p>/g, '');
        
        // 9. Заменяем одиночные переносы на <br>
        html = html.replace(/\\n/g, '<br>');
        
        return html;
    }

    function highlightHttpMethods(codeHtml) {
        const httpMethods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'];
        let highlighted = codeHtml;
        
        httpMethods.forEach(method => {
            const regex = new RegExp(`\\b(${method})\\b`, 'gi');
            highlighted = highlighted.replace(regex, '<span class="http-method-highlight">$1</span>');
        });
        
        // Подсвечиваем пути после HTTP методов
        highlighted = highlighted.replace(
            /(<span class="http-method-highlight">[^<]+<\/span>)\s+([^\s<]+)/g,
            '$1 <span class="http-path">$2</span>'
        );
        
        return highlighted;
    }

    // === ФУНКЦИИ ДЛЯ КНОПОК КОПИРОВАНИЯ ===

    function initCopyButtons() {
        document.querySelectorAll('.copy-code-btn').forEach(button => {
            // Убираем старые обработчики
            button.replaceWith(button.cloneNode(true));
        });
        
        document.querySelectorAll('.copy-code-btn').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const blockId = this.getAttribute('data-target');
                const codeBlock = document.getElementById(blockId);
                
                if (!codeBlock) return;
                
                const codeElement = codeBlock.querySelector('code');
                const text = codeElement ? codeElement.textContent : '';
                
                navigator.clipboard.writeText(text).then(() => {
                    const originalHTML = this.innerHTML;
                    this.innerHTML = '<span class="copy-icon">✓</span><span class="copy-text">Скопировано!</span>';
                    this.style.background = 'rgba(76, 175, 80, 0.3)';
                    
                    setTimeout(() => {
                        this.innerHTML = originalHTML;
                        this.style.background = '';
                    }, 2000);
                }).catch(err => {
                    console.error('Ошибка копирования:', err);
                    this.innerHTML = '<span class="copy-icon">❌</span><span class="copy-text">Ошибка</span>';
                    this.style.background = 'rgba(244, 67, 54, 0.3)';
                    
                    setTimeout(() => {
                        this.innerHTML = '<span class="copy-icon">📋</span><span class="copy-text">Копировать</span>';
                        this.style.background = '';
                    }, 2000);
                });
            });
        });
    }

    // === НАБЛЮДАТЕЛЬ И ОБРАБОТЧИКИ СОБЫТИЙ ===

    function setupMutationObserver() {
        const observer = new MutationObserver(function(mutations) {
            let shouldProcess = false;
            
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                    shouldProcess = true;
                }
            });
            
            if (shouldProcess) {
                setTimeout(() => {
                    processAllMarkdown();
                }, 100);
            }
        });
        
        const swaggerContainer = document.querySelector('.swagger-ui');
        if (swaggerContainer) {
            observer.observe(swaggerContainer, {
                childList: true,
                subtree: true,
                attributes: false,
                characterData: false
            });
        }
    }

    function handleSwaggerClick(e) {
        // Если кликнули на эндпоинт
        if (e.target.closest('.opblock-tag') || 
            e.target.closest('.opblock-summary') ||
            e.target.closest('.expand-operation')) {
            setTimeout(() => {
                processAllMarkdown();
            }, 300);
        }
    }

    // === ФУНКЦИЯ ФИЛЬТРАЦИИ ПО ТЕГАМ ===
    function filterTagsByHash() {
        if (window.location.hash.includes('24')) {
            const tagSections = document.querySelectorAll('.opblock-tag-section');
            tagSections.forEach((section) => {
                if (section.children[0] && section.children[0].getAttribute('data-tag') !== 'Битрикс24') {
                    section.style.display = 'none';
                } else {
                    section.style.display = 'block';
                }
            });
        } else {
            // Показываем все разделы, если нет фильтрации
            const tagSections = document.querySelectorAll('.opblock-tag-section');
            tagSections.forEach((section) => {
                section.style.display = 'block';
            });
        }
    }

    // === СТИЛИ ДЛЯ MARKDOWN ===
    const markdownStyles = `
        <style>
            .markdown-h1 { color: #f5821f; font-size: 1.8em; margin: 1em 0 0.5em 0; font-weight: bold; }
            .markdown-h2 { color: #f5821f; font-size: 1.5em; margin: 1em 0 0.5em 0; font-weight: bold; }
            .markdown-h3 { color: #f5821f; font-size: 1.3em; margin: 1em 0 0.5em 0; font-weight: bold; }
            .markdown-p { color: #ffffff; margin: 0.5em 0; line-height: 1.5; color: #ffffff; }
            .markdown-list { margin: 0.5em 0 0.5em 1.5em; color: #ffffff; }
            .markdown-list-item { margin: 0.3em 0; line-height: 1.4; color: #ffffff; }
            .inline-code { background: rgba(245, 130, 31, 0.2); padding: 2px 6px; border-radius: 4px; font-family: monospace; color: #ff9a42; }
            strong { color: #f5821f; font-weight: bold; }
            em { font-style: italic; opacity: 0.9; }
            
            .code-block-container { 
                background: #2d2d2d; 
                border: 1px solid #404040; 
                border-radius: 8px; 
                margin: 1em 0; 
                overflow: hidden; 
            }
            .code-header { 
                background: linear-gradient(90deg, rgba(245,130,31,0.1), rgba(245,130,31,0.05)); 
                border-bottom: 1px solid #404040; 
                padding: 8px 12px; 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
            }
            .language-badge { 
                background: #f5821f; 
                color: #000; 
                font-size: 0.75em; 
                font-weight: bold; 
                padding: 3px 8px; 
                border-radius: 4px; 
                text-transform: uppercase; 
            }
            .copy-code-btn { 
                background: rgba(245,130,31,0.2); 
                color: #f5821f; 
                border: 1px solid rgba(245,130,31,0.3); 
                border-radius: 4px; 
                padding: 4px 8px; 
                font-size: 0.8em; 
                cursor: pointer; 
                display: flex; 
                align-items: center; 
                gap: 4px; 
                transition: all 0.2s; 
            }
            .copy-code-btn:hover { 
                background: rgba(245,130,31,0.3); 
                transform: translateY(-1px); 
            }
            .code-block-container pre { 
                margin: 0; 
                padding: 12px; 
                overflow-x: auto; 
                background: #242424; 
            }
            .code-block-container code { 
                display: block; 
                color: #ffffff; 
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; 
                font-size: 0.9em; 
                line-height: 1.4; 
                white-space: pre; 
            }
            .http-method-highlight { color: #f5821f; font-weight: bold; }
            .http-path { color: #ffffff; }
        </style>
    `;

    // === ЗАПУСК ВСЕГО ПРИ ЗАГРУЗКЕ ===
    document.addEventListener('DOMContentLoaded', function() {
        // Добавляем стили
        document.head.insertAdjacentHTML('beforeend', markdownStyles);
        
        // Запускаем обработку с небольшой задержкой для полной загрузки Swagger UI
        setTimeout(() => {
            initMarkdownProcessing();
            
            // Применяем фильтрацию по хэшу при загрузке
            filterTagsByHash();
            
            // Проверяем начальный хэш
            if (window.location.hash.includes('24')) {
                const test = document.querySelectorAll('.opblock-tag-section');
                test.forEach((e) => {
                    if (e.children[0] && e.children[0].getAttribute('data-tag') !== 'Битрикс24') {
                        e.style.display = 'none';
                    } else {
                        e.style.display = 'block';
                    }
                });
            }
        }, 1000);
        
        // Также пробуем каждые 500ms на случай если Swagger грузится медленно
        let attempts = 0;
        const checkInterval = setInterval(() => {
            attempts++;
            if (document.querySelector('.swagger-ui .info') || attempts > 10) {
                clearInterval(checkInterval);
                if (attempts <= 10) {
                    initMarkdownProcessing();
                    
                    // Применяем фильтрацию по хэшу
                    filterTagsByHash();
                }
            }
        }, 500);
    });

    // === ОБРАБОТЧИК ИЗМЕНЕНИЯ ХЭША ===
    window.addEventListener('hashchange', () => {
        filterTagsByHash();
        
        // Также повторная обработка markdown при изменении хэша
        setTimeout(processAllMarkdown, 300);
    });

    // Экспортируем функции для отладки
    window.processMarkdown = processAllMarkdown;
    window.convertMarkdown = convertMarkdownToHtml;
    window.filterTagsByHash = filterTagsByHash;
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
    openapi_schema = convert_markdown_in_schema_safe(openapi_schema)
    
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

def markdown_to_plain(text: str) -> str:
    """
    Простое преобразование Markdown в текст БЕЗ HTML.
    Блоки кода помечаем специальными метками.
    """
    if not text:
        return text
    
    result = []
    lines = text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Блок кода ```
        if line.strip().startswith('```'):
            # Начало блока кода
            language = line.strip()[3:].strip() or "text"
            code_lines = []
            
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            
            # Пропускаем закрывающий ```
            i += 1
            
            # Собираем код
            code_content = '\n'.join(code_lines).strip()
            
            # Определяем язык (особенно HTTP)
            if language == "text":
                first_line = code_content.split('\n')[0] if '\n' in code_content else code_content
                if any(method.upper() in first_line.upper() for method in ['GET', 'POST', 'PUT', 'DELETE']):
                    language = "http"
            
            # Добавляем специальную метку для JS
            result.append(f'[CODE_BLOCK language="{language}"]{code_content}[/CODE_BLOCK]')
            continue
        
        # Обычный текст
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def convert_markdown_in_schema_safe(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Безопасное преобразование Markdown БЕЗ HTML.
    """
    import copy
    
    def process_value(value):
        if isinstance(value, dict):
            return {k: process_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [process_value(item) for item in value]
        elif isinstance(value, str):
            if value:  # Преобразуем только непустые строки
                return markdown_to_plain(value)
            return value
        else:
            return value
    
    return process_value(copy.deepcopy(schema))