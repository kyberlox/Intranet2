from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, FileResponse
import os
import asyncio
import pyvips
from typing import Optional
import logging

# Обязательное именование роутера (как требуется в проекте)
compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])

# Конфигурация (как указано)
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)
TARGET_QUALITY = 70  # Качество сжатия (0-100)

def _compress_image_sync(image_path: str) -> bytes:
    """Синхронное сжатие изображения через pyvips"""
    try:
        image = pyvips.Image.new_from_file(image_path)
        return image.webpsave_buffer(Q=TARGET_QUALITY)
    except Exception as e:
        logging.error(f"Ошибка сжатия {image_path}: {str(e)}")
        raise

@compress_router.get("/{filename}")  # Обязательное именование (как в требованиях)
async def get_compressed_image(
    filename: str,
    preserve_transparency: Optional[bool] = False
):
    """
    Возвращает сжатое изображение.
    Соответствует строгим требованиям проекта:
    - Роутер именуется `compress_router`
    - Префикс `/compress_image`
    - Путь к файлам: `./files_db`
    """
    file_path = os.path.join(STORAGE_PATH, filename)
    
    # Проверка существования файла
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    # Быстрый возврат для маленьких файлов (<250KB)
    if os.path.getsize(file_path) < 250 * 1024:
        return FileResponse(file_path)

    try:
        # Асинхронное сжатие в отдельном потоке
        compressed_data = await asyncio.to_thread(
            _compress_image_sync,
            file_path
        )
        
        return Response(
            content=compressed_data,
            media_type="image/webp",
            headers={
                "Content-Disposition": f"inline; filename=compressed_{filename}",
                "X-Compression-Quality": str(TARGET_QUALITY)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")