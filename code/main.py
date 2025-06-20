from fastapi import FastAPI, APIRouter, Body, Request, UploadFile, HTTPException, Response, Request
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

from src.model.File import File, file_router
from src.services.VCard import vcard_app
from src.services.LogsMaker import LogsMaker

from src.base.SearchModel import UserSearchModel, StructureSearchModel, search_router

from src.base.B24 import B24

from src.services.Auth import AuthService, auth_router



from typing import Awaitable, Callable, Optional

from PIL import Image
import io

import os

import time

import asyncio

app = FastAPI()

app.include_router(users_router, prefix="/api")
app.include_router(depart_router, prefix="/api")
app.include_router(usdep_router, prefix="/api")
app.include_router(section_router, prefix="/api")
app.include_router(article_router, prefix="/api")
app.include_router(file_router, prefix="/api")
app.include_router(vcard_app, prefix="/api")
app.include_router(search_router, prefix="/api")

app.include_router(auth_router, prefix="/api")


app.mount("/api/view/app", StaticFiles(directory="./front_jinja/static"), name="app")

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



# Настройки
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

USER_STORAGE_PATH = "./files_db/user_photo"
os.makedirs(USER_STORAGE_PATH, exist_ok=True)

# Монтируем статику
app.mount("/api/files", StaticFiles(directory=STORAGE_PATH), name="files")
app.mount("/api/user_files", StaticFiles(directory=USER_STORAGE_PATH), name="user_files")



#Проверка авторизации для ВСЕХ запросов
@app.middleware("http")
async def auth_middleware(request: Request, call_next : Callable[[Request], Awaitable[Response]]):
    # Внедряю свою отладку
    log = LogsMaker()

    # Исключаем эндпоинты, которые не требуют авторизации (например, сам эндпоинт авторизации)
    open_links = [
        "/docs",
        "/openapi.json",
        "/api/auth_router",
        "/total_update",
        "/api/files",
        "/api/user_files",
        "test", "get_file", "get_all_files",
        "/api/total_background_task_update",
    ]
    for open_link in open_links:
        if open_link in request.url.path:
            return await call_next(request)

    # Проверяем авторизацию для всех остальных /api эндпоинтов
    if request.url.path.startswith("/api"):
        token = request.cookies.get("Authorization")
        if token is None:
            token = request.headers.get("Authorization")
            if token is None:
                return JSONResponse(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    content = await log.warning_message(message="Authorization cookies or headers missing")
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
                    content = await log.warning_message(message="Invalid token")
                )
                # raise HTTPException(
                #     status_code=status.HTTP_401_UNAUTHORIZED,
                #     detail="Invalid token",
                # )

        except IndexError:
            return JSONResponse(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    content = await log.warning_message(message="Invalid authorization cookies or headers format")
                )
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Invalid authorization cookies format",
            # )

    return await call_next(request)

#Сжатие картинок
def get_compression_settings(original_format: str, accept_header: str, pixel_count: int) -> tuple:
    """Определяет оптимальные параметры сжатия"""
    accept_header = accept_header.lower()
    
    # Для маленьких изображений (иконки) используем менее агрессивное сжатие
    if pixel_count < 250_000:  # ~500x500px
        base_quality = 90
        max_dimension = 1024
    else:
        base_quality = 80
        max_dimension = 1920
    
    # Предпочитаем WebP если клиент поддерживает
    if "webp" in accept_header:
        return "WEBP", {
            "quality": max(75, base_quality - 5),
            "max_dimension": max_dimension,
            "extra_args": {"method": 6}  # Максимальное сжатие
        }
    
    # Для JPEG/PNG выбираем на основе исходного формата
    if original_format == "PNG":
        return "PNG", {
            "quality": base_quality,
            "max_dimension": max_dimension,
            "extra_args": {"compress_level": 9}
        }
    
    # По умолчанию используем JPEG
    return "JPEG", {
        "quality": base_quality,
        "max_dimension": max_dimension,
        "extra_args": {"progressive": True, "subsampling": "4:2:0"}
    }

def calculate_new_size(width: int, height: int, max_dimension: int) -> tuple:
    """Вычисляет новые размеры с сохранением пропорций"""
    if width > height:
        return (max_dimension, int(height * max_dimension / width))
    return (int(width * max_dimension / height), max_dimension)
    
@app.middleware("http")
async def compress_images_middleware(request: Request, call_next):
    # 1. Получаем исходный ответ
    response = await call_next(request)
    
    # 2. Проверяем, нужно ли сжимать
    content_type = response.headers.get("content-type", "").lower()
    if not content_type.startswith(("image/jpeg", "image/png", "image/webp")):
        return response
    
    # 3. Читаем тело ответа
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    
    # 4. Применяем продвинутое сжатие
    try:
        with io.BytesIO(body) as input_buf, io.BytesIO() as output_buf:
            # Открываем и автоматически поворачиваем изображение
            img = ImageOps.exif_transpose(Image.open(input_buf))
            
            # Определяем параметры сжатия
            width, height = img.size
            target_format, compression_params = get_compression_settings(
                img.format,
                request.headers.get("accept", ""),
                width * height
            )
            
            # Применяем ресайз если нужно
            if max(width, height) > compression_params["max_dimension"]:
                new_size = calculate_new_size(width, height, compression_params["max_dimension"])
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Конвертируем в оптимальный цветовой профиль
            if target_format in ("JPEG", "WEBP") and img.mode != "RGB":
                img = img.convert("RGB")
            
            # Сохраняем с оптимальными параметрами
            img.save(
                output_buf,
                format=target_format,
                quality=compression_params["quality"],
                optimize=True,
                **compression_params.get("extra_args", {})
            )
            
            compressed_body = output_buf.getvalue()
            
            # Возвращаем сжатое изображение если удалось уменьшить размер
            if len(compressed_body) < len(body):
                return Response(
                    content=compressed_body,
                    status_code=response.status_code,
                    headers={
                        **dict(response.headers),
                        "content-length": str(len(compressed_body)),
                        "x-image-compressed": "true",
                        "x-compression-ratio": f"{len(compressed_body)/len(body):.2f}"
                    },
                    media_type=f"image/{target_format.lower()}"
                )
    
    except Exception as e:
        print(f"Compression error: {str(e)}")
    
    # 5. Возвращаем оригинал если сжатие не удалось
    return Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )



@app.get("/test/{ID}")
def test(ID):
    return Article(section_id=ID).get_inf()

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

@app.get("/elastic_dump")
def elastic_dump():
    # res = UserSearchModel().dump()
    res = StructureSearchModel().dump()
    return res

@app.get("/elastic_search")
def elastic_search(name: str):
    return UserSearchModel().search_by_name(name)

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
    background_tasks.add_task(Article().uplod)
    return {"status" : "started", "message" : "Загрузка запущена в фоновом режиме!"}



@app.put("/api/total_update")
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



'''
! Особенные запросы
'''

