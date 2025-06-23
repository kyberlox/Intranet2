from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import os
import asyncio
import pyvips
from typing import List
import logging

router = APIRouter(prefix="/compress", tags=["Компрессия"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

# Настройки сжатия
TARGET_QUALITY = 70  # Баланс скорость/качество
MAX_WIDTH = 1920     # Максимальная ширина (для уменьшения разрешения)

def _compress_vips(image_path: str) -> bytes:
    """Синхронное сжатие через libvips (очень быстрое)"""
    try:
        image = pyvips.Image.new_from_file(image_path)
        
        # Уменьшаем разрешение для больших изображений
        if image.width > MAX_WIDTH:
            image = image.resize(MAX_WIDTH / image.width)
        
        return image.webpsave_buffer(Q=TARGET_QUALITY)
    except Exception as e:
        logging.error(f"Ошибка сжатия {image_path}: {e}")
        raise

async def compress_image(image_path: str) -> Response:
    """Асинхронная обёртка для сжатия"""
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    try:
        # Запускаем в отдельном потоке (не блокируем event loop)
        compressed_data = await asyncio.to_thread(_compress_vips, image_path)
        return Response(
            content=compressed_data,
            media_type="image/webp",
            headers={"X-Compressed": "true"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@router.post("/batch")
async def compress_batch(filenames: List[str]) -> List[Response]:
    """Параллельная обработка 300+ фото"""
    tasks = []
    for filename in filenames:
        file_path = os.path.join(STORAGE_PATH, filename)
        tasks.append(compress_image(file_path))
    
    return await asyncio.gather(*tasks)