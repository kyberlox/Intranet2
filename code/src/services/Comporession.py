from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, FileResponse
import os
import asyncio
import pyvips
from io import BytesIO
import logging
from pathlib import Path
from typing import Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
Path(STORAGE_PATH).mkdir(parents=True, exist_ok=True)

# Конфигурация сжатия
MAX_UNCOMPRESSED_SIZE_KB = 250
LARGE_FILE_THRESHOLD_KB = 1024
LARGE_FILE_TARGET_KB = 512

async def _turbo_compress(img_path: str) -> Optional[BytesIO]:
    """Улучшенная функция сжатия с полной диагностикой"""
    try:
        # 1. Проверка существования и доступности файла
        if not os.path.exists(img_path):
            logger.error(f"Файл не найден: {img_path}")
            return None
            
        if not os.access(img_path, os.R_OK):
            logger.error(f"Нет доступа к файлу: {img_path}")
            return None

        # 2. Проверка размера файла
        file_size = os.path.getsize(img_path)
        if file_size == 0:
            logger.error(f"Пустой файл: {img_path}")
            return None

        # 3. Загрузка изображения с проверкой формата
        try:
            img = pyvips.Image.new_from_file(img_path)
            if img is None:
                logger.error(f"Не удалось загрузить изображение: {img_path}")
                return None
        except pyvips.Error as vipserr:
            logger.error(f"Ошибка pyvips при загрузке {img_path}: {str(vipserr)}")
            return None

        # 4. Определение параметров сжатия
        file_size_kb = file_size / 1024
        quality = 30 if file_size_kb > LARGE_FILE_THRESHOLD_KB else 70
        
        # 5. Процесс сжатия
        buffer = BytesIO()
        try:
            img.webpsave_buffer(
                buffer,
                Q=quality,
                strip=True,
                smart_subsample=True,
                reduction_effort=4
            )
            buffer.seek(0)
            
            # 6. Проверка результата сжатия
            if len(buffer.getvalue()) == 0:
                logger.error(f"Пустой результат сжатия: {img_path}")
                return None
                
            return buffer
            
        except Exception as compress_err:
            logger.error(f"Ошибка сжатия {img_path}: {str(compress_err)}")
            return None

    except Exception as e:
        logger.critical(f"Критическая ошибка в _turbo_compress: {str(e)}", exc_info=True)
        return None

@compress_router.get("/{filename}")
async def get_compressed_image(filename: str):
    """Эндпоинт с улучшенной обработкой ошибок"""
    try:
        file_path = os.path.join(STORAGE_PATH, filename)
        logger.info(f"Обработка файла: {file_path}")

        # 1. Проверка файла
        if not os.path.isfile(file_path):
            logger.error(f"Файл не найден: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
            
        if not os.access(file_path, os.R_OK):
            logger.error(f"Нет доступа к файлу: {file_path}")
            raise HTTPException(status_code=403, detail="Access denied")

        # 2. Проверка размера
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            logger.error(f"Пустой файл: {file_path}")
            raise HTTPException(status_code=400, detail="Empty file")

        # 3. Возврат без сжатия для маленьких файлов
        if file_size <= MAX_UNCOMPRESSED_SIZE_KB * 1024:
            logger.info(f"Возврат без сжатия (маленький файл): {file_path}")
            return FileResponse(file_path)

        # 4. Сжатие изображения
        logger.info(f"Начало сжатия: {file_path}")
        buffer = await _turbo_compress(file_path)
        
        if buffer is None:
            logger.error(f"Сжатие не удалось: {file_path}")
            raise HTTPException(status_code=500, detail="Image processing failed")

        # 5. Возврат результата
        compressed_size = len(buffer.getvalue())
        logger.info(f"Успешное сжатие: {file_path} ({file_size} → {compressed_size} bytes)")
        
        return Response(
            content=buffer.getvalue(),
            media_type="image/webp",
            headers={
                "X-Original-Size": str(file_size),
                "X-Compressed-Size": str(compressed_size)
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Непредвиденная ошибка: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")