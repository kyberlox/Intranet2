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

from PIL import Image, ImageOps
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

'''
#Сжатие картинок
@app.middleware("http")
async def compress_images_middleware(request: Request, call_next):
    # 1. Получаем исходный ответ
    response = await call_next(request)
    
    # 2. Проверяем, нужно ли сжимать (только JPEG/PNG/WEBP)
    content_type = response.headers.get("content-type", "").lower()
    if not any(content_type.startswith(f"image/{fmt}") for fmt in ["jpeg", "png", "webp"]):
        return response
    
    # 3. Читаем тело ответа
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    
    # 4. Оптимизируем изображение
    try:
        with io.BytesIO(body) as input_buf, io.BytesIO() as output_buf:
            # Открываем изображение с коррекцией ориентации
            img = ImageOps.exif_transpose(Image.open(input_buf))
            
            # Определяем параметры сжатия
            width, height = img.size
            accept_header = request.headers.get("accept", "").lower()
            pixel_count = width * height
            
            # Выбираем формат (WebP при поддержке клиентом)
            if "webp" in accept_header:
                target_format = "WEBP"
                quality = 75
                extra_args = {"method": 6}  # Максимальное сжатие
            elif img.format == "PNG" and img.mode in ("RGBA", "LA"):
                target_format = "PNG"
                quality = 85
                extra_args = {"compress_level": 9}
            else:
                target_format = "JPEG"
                quality = 80
                extra_args = {"progressive": True, "subsampling": "4:2:0"}
            
            # Ресайз для больших изображений (макс. 1920px)
            max_dimension = 1024 if pixel_count < 250000 else 1920
            if max(width, height) > max_dimension:
                new_width = min(width, max_dimension)
                new_height = int(height * (new_width / width))
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Конвертируем цветовой профиль для JPEG/WEBP
            if target_format in ("JPEG", "WEBP") and img.mode != "RGB":
                img = img.convert("RGB")
            
            # Применяем сжатие
            img.save(
                output_buf,
                format=target_format,
                quality=quality,
                optimize=True,
                **extra_args
            )
            
            compressed_body = output_buf.getvalue()
            
            # Возвращаем результат если сжатие успешно
            if len(compressed_body) < len(body):
                return Response(
                    content=compressed_body,
                    status_code=response.status_code,
                    headers={
                        **dict(response.headers),
                        "content-length": str(len(compressed_body)),
                        "x-image-optimized": "true",
                        "x-original-size": str(len(body)),
                        "x-compressed-size": str(len(compressed_body))
                    },
                    media_type=f"image/{target_format.lower()}"
                )
    
    except Exception as e:
        print(f"[Image Compression Error] {str(e)}")
    
    # 5. Возвращаем оригинал при ошибках
    return Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )
'''



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

