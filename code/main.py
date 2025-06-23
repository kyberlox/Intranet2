from fastapi import FastAPI, APIRouter, Body, Request, UploadFile, HTTPException, Response, Request
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

from src.model.File import File, file_router
from src.services.VCard import vcard_app
from src.services.LogsMaker import LogsMaker

from src.base.SearchModel import UserSearchModel, StructureSearchModel, search_router

from src.base.B24 import B24

from src.services.Auth import AuthService, auth_router



from typing import Awaitable, Callable, Optional

from PIL import Image
from io import BytesIO

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
        "/api/compress_image/",
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




def compress_image(input_path: str, max_size_kb: int = 250, preserve_transparency: bool = False) -> BytesIO:
    """
    Сжимает изображение до размера не превышающего max_size_kb в КБ.
    Возвращает BytesIO объект с сжатым изображением.
    
    :param input_path: путь к исходному изображению
    :param max_size_kb: максимальный размер в КБ
    :param preserve_transparency: сохранять ли прозрачность (для PNG)
    :return: BytesIO с сжатым изображением
    """
    with Image.open(input_path) as img:
        original_format = img.format
        output_buffer = BytesIO()
        
        # Если изображение уже достаточно маленькое
        if os.path.getsize(input_path) / 1024 <= max_size_kb:
            img.save(output_buffer, format=original_format)
            output_buffer.seek(0)
            return output_buffer
        
        # Настройки сжатия для разных форматов
        if original_format == 'JPEG':
            quality = 85
            params = {'format': 'JPEG', 'quality': quality, 'optimize': True}
        elif original_format == 'PNG':
            if preserve_transparency and img.mode in ('RGBA', 'LA'):
                # Для PNG с прозрачностью используем оптимизацию
                quality = 90
                params = {'format': 'PNG', 'compress_level': 6, 'optimize': True}
            else:
                # Конвертируем в JPEG если прозрачность не важна
                img = img.convert('RGB')
                quality = 85
                params = {'format': 'JPEG', 'quality': quality, 'optimize': True}
        elif original_format == 'GIF':
            # Для GIF просто сохраняем как есть (сжатие GIF сложнее)
            img.save(output_buffer, format='GIF')
            output_buffer.seek(0)
            return output_buffer
        elif original_format == 'WEBP':
            quality = 80
            params = {'format': 'WEBP', 'quality': quality, 'method': 6}
        else:
            # Для других форматов пробуем сохранить как JPEG
            img = img.convert('RGB')
            quality = 85
            params = {'format': 'JPEG', 'quality': quality, 'optimize': True}
        
        # Процесс сжатия с итеративным уменьшением качества
        while True:
            output_buffer.seek(0)
            output_buffer.truncate()
            
            img.save(output_buffer, **params)
            
            size_kb = output_buffer.tell() / 1024
            if size_kb <= max_size_kb or quality <= 10:
                break
                
            # Уменьшаем качество
            quality_step = 5 if size_kb / max_size_kb < 2 else 15
            quality = max(10, quality - quality_step)
            params['quality'] = quality
        
        output_buffer.seek(0)
        return output_buffer

def _optimized_compress(image: Image.Image, original_format: str, max_size_kb: int = 250) -> BytesIO:
    """Ускоренная версия сжатия без итеративного подбора качества."""
    buffer = BytesIO()
    format_params = {
        "JPEG": {"format": "JPEG", "quality": 85, "optimize": True},
        "PNG": {"format": "PNG", "compress_level": 6},
        "WEBP": {"format": "WEBP", "quality": 80, "method": 4}
    }
    
    params = format_params.get(original_format, {"format": "JPEG", "quality": 75})
    image.save(buffer, **params)
    
    if buffer.tell() / 1024 > max_size_kb and original_format in ("JPEG", "WEBP"):
        # Жёсткое сжатие, если не уложились в размер
        buffer.seek(0)
        buffer.truncate()
        params["quality"] = max(30, params.get("quality", 75) - 25)
        image.save(buffer, **params)
    
    buffer.seek(0)
    return buffer

@app.get("/api/compress_image/{filename}")
async def get_compressed_image(
    filename: str, 
    preserve_transparency: Optional[bool] = False
):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    # Быстрая проверка файла
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Загрузка изображения в память один раз
        with Image.open(file_path) as img:
            original_format = img.format.upper() if img.format else "JPEG"
            file_size_kb = os.path.getsize(file_path) / 1024
            
            if file_size_kb <= 250:
                return FileResponse(file_path)
            
            # Конвертация формата, если нужно
            if original_format == "PNG" and not preserve_transparency:
                img = img.convert("RGB")
                original_format = "JPEG"
            
            # Асинхронное сжатие
            buffer = await asyncio.to_thread(
                _optimized_compress, 
                img, 
                original_format
            )
            
            return Response(
                content=buffer.getvalue(),
                media_type=f"image/{original_format.lower()}",
                headers={"Content-Disposition": f"inline; filename=compressed_{filename}"}
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")

'''
@app.get("/api/compress_image/{filename}")
async def get_compressed_image(filename: str, preserve_transparency: Optional[bool] = False):
    # Базовый путь к папке с изображениями (измените на свой)
    file_path = os.path.join(STORAGE_PATH, filename)
    
    # Проверяем существование файла
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Проверяем, что это изображение
    try:
        with Image.open(file_path) as img:
            original_format = img.format.upper() if img.format else None
    except:
        raise HTTPException(status_code=400, detail="File is not a valid image")
    
    # Проверяем размер файла
    file_size_kb = os.path.getsize(file_path) / 1024
    
    if file_size_kb <= 250:
        # Возвращаем как есть, если размер меньше 250 КБ
        return FileResponse(file_path)
    else:
        # Сжимаем изображение
        compressed_image = compress_image(file_path, preserve_transparency=preserve_transparency)
        
        # Определяем Content-Type
        content_type = f"image/{original_format.lower()}" if original_format else "image/jpeg"
        if original_format == 'JPEG':
            content_type = 'image/jpeg'
        elif original_format == 'PNG':
            content_type = 'image/png'
        elif original_format == 'GIF':
            content_type = 'image/gif'
        elif original_format == 'WEBP':
            content_type = 'image/webp'
        
        # Возвращаем сжатое изображение
        return Response(
            content=compressed_image.getvalue(),
            media_type=content_type,
            headers={"Content-Disposition": f"inline; filename=compressed_{filename}"}
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

