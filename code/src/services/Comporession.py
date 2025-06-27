from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from PIL import Image, ImageFilter
from io import BytesIO
import os

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

USER_STORAGE_PATH = "./files_db/user_photo"
os.makedirs(USER_STORAGE_PATH, exist_ok=True)

# Настройки качества
TARGET_WIDTH = 357
TARGET_HEIGHT = 204

YOWAIMO_TARGET_WIDTH = 700
YOWAIMO_TARGET_HEIGHT = 1024

TARGET_USER_WIDTH = 359
TARGET_USER_HEIGHT = 493

QUALITY = 95  # Качество сохранения (1-100)
YOWAIMO_QUALITY = 100
QUALITY_USER = 80

RESAMPLE = Image.LANCZOS  # Лучший алгоритм интерполяции

def resize_image_quality(input_path: str) -> BytesIO:
    """Изменение размера с сохранением качества"""
    with Image.open(input_path) as img:
        # Сохраняем исходный формат и EXIF-данные
        original_format = img.format
        exif = img.info.get('exif')
        
        # Пропорциональное уменьшение с лучшим алгоритмом
        img.thumbnail(
            (TARGET_WIDTH, TARGET_HEIGHT),
            resample=RESAMPLE
        )
        
        # Легкое повышение резкости (опционально)
        img = img.filter(ImageFilter.SHARPEN)
        
        # Сохранение с высоким качеством
        output_buffer = BytesIO()
        save_params = {
            'format': original_format,
            'quality': QUALITY,
            'optimize': True,
            'subsampling': 0,  # Отключаем субдискретизацию для JPEG
            'qtables': 'web_high'  # Используем высококачественные таблицы квантования
        }
        if exif:
            save_params['exif'] = exif
            
        img.save(output_buffer, **save_params)
        output_buffer.seek(0)
        
        return output_buffer

def resize_user_image_quality(input_path: str) -> BytesIO:
    """Изменение размера с сохранением качества"""
    with Image.open(input_path) as img:
        # Сохраняем исходный формат и EXIF-данные
        original_format = img.format
        exif = img.info.get('exif')
        
        # Пропорциональное уменьшение с лучшим алгоритмом
        img.thumbnail(
            (TARGET_USER_WIDTH, TARGET_USER_HEIGHT),
            resample=RESAMPLE
        )
        
        # Легкое повышение резкости (опционально)
        img = img.filter(ImageFilter.SHARPEN)
        
        # Сохранение с высоким качеством
        output_buffer = BytesIO()
        save_params = {
            'format': original_format,
            'quality': QUALITY_USER,
            'optimize': True,
            'subsampling': 0,  # Отключаем субдискретизацию для JPEG
            'qtables': 'web_high'  # Используем высококачественные таблицы квантования
        }
        if exif:
            save_params['exif'] = exif
            
        img.save(output_buffer, **save_params)
        output_buffer.seek(0)
        
        return output_buffer

@compress_router.get("/{filename}")
def get_resized_image(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    try:
        with Image.open(file_path) as img:
            original_format = img.format.lower() if img.format else 'jpeg'
            original_res = f"{img.width}x{img.height}"
        
        resized_image = resize_image_quality(file_path)
        
        return Response(
            content=resized_image.getvalue(),
            media_type=f"image/{original_format}",
            headers={
                "X-Original-Resolution": original_res,
                "X-Target-Resolution": f"{TARGET_WIDTH}x{TARGET_HEIGHT}",
                "X-Quality-Params": f"resample={RESAMPLE}, quality={QUALITY}"
            }
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")

@compress_router.get("/yowai_mo/{filename}")
def get_resized_yowai_mo_image(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    try:
        with Image.open(file_path) as img:
            original_format = img.format.lower() if img.format else 'jpeg'
            original_res = f"{img.width}x{img.height}"
        
        resized_image = resize_image_quality(file_path)
        
        return Response(
            content=resized_image.getvalue(),
            media_type=f"image/{original_format}",
            headers={
                "X-Original-Resolution": original_res,
                "X-Target-Resolution": f"{YOWAIMO_TARGET_WIDTH}x{YOWAIMO_TARGET_HEIGHT}",
                "X-Quality-Params": f"resample={RESAMPLE}, quality={YOWAIMO_QUALITY}"
            }
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")

@compress_router.get("/user/{filename}")
def get_resized_image(filename: str):
    file_path = os.path.join(USER_STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    try:
        with Image.open(file_path) as img:
            original_format = img.format.lower() if img.format else 'jpeg'
            original_res = f"{img.width}x{img.height}"
        
        resized_image = resize_user_image_quality(file_path)
        
        return Response(
            content=resized_image.getvalue(),
            media_type=f"image/{original_format}",
            headers={
                "X-Original-Resolution": original_res,
                "X-Target-Resolution": f"{TARGET_WIDTH}x{TARGET_HEIGHT}",
                "X-Quality-Params": f"resample={RESAMPLE}, quality={QUALITY}"
            }
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")