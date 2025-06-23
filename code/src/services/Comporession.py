from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, FileResponse
import os
import asyncio
import pyvips
from io import BytesIO
import logging
from pathlib import Path

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
Path(STORAGE_PATH).mkdir(exist_ok=True)

# Настройки сжатия
MAX_UNCOMPRESSED_SIZE_KB = 250
LARGE_FILE_THRESHOLD_KB = 1024
LARGE_FILE_TARGET_KB = 512

async def _turbo_compress(img_path: str) -> BytesIO:
    """Надежная асинхронная компрессия с полной диагностикой"""
    try:
        # Проверка файла перед обработкой
        if not os.path.isfile(img_path):
            logging.error(f"File not found or is directory: {img_path}")
            return None
            
        file_size = os.path.getsize(img_path)
        if file_size == 0:
            logging.error(f"Empty file: {img_path}")
            return None

        # Чтение файла с проверкой
        try:
            img = pyvips.Image.new_from_file(img_path)
            if img is None:
                logging.error(f"pyvips failed to load image: {img_path}")
                return None
        except pyvips.Error as e:
            logging.error(f"pyvips error with {img_path}: {str(e)}")
            return None

        # Определение параметров сжатия
        file_size_kb = file_size / 1024
        is_large = file_size_kb > LARGE_FILE_THRESHOLD_KB
        quality = 30 if is_large else 70
        target_format = "webp"

        # Сжатие с обработкой ошибок
        try:
            buffer = BytesIO()
            img.webpsave_buffer(
                buffer,
                Q=quality,
                strip=True,
                smart_subsample=True,
                reduction_effort=4
            )
            buffer.seek(0)
            
            # Проверка размера после сжатия
            compressed_size = len(buffer.getvalue()) / 1024
            if is_large and compressed_size > LARGE_FILE_TARGET_KB:
                logging.warning(f"Recompressing {img_path} (size: {compressed_size:.1f}KB)")
                buffer = BytesIO()
                img.webpsave_buffer(buffer, Q=20)
                buffer.seek(0)
                
            return buffer
        except Exception as e:
            logging.error(f"Compression failed for {img_path}: {str(e)}")
            return None
            
    except Exception as e:
        logging.critical(f"Unexpected error in _turbo_compress: {str(e)}")
        return None

@compress_router.get("/{filename}")
async def get_compressed_image(filename: str):
    """Эндпоинт с полной обработкой ошибок"""
    try:
        file_path = os.path.join(STORAGE_PATH, filename)
        
        # 1. Проверка существования файла
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")
            
        # 2. Проверка размера файла
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        # 3. Возврат без сжатия для маленьких файлов
        if file_size <= MAX_UNCOMPRESSED_SIZE_KB * 1024:
            return FileResponse(file_path)

        # 4. Асинхронное сжатие
        buffer = await _turbo_compress(file_path)
        if buffer is None:
            raise HTTPException(status_code=500, detail="Image processing failed")

        # 5. Возврат результата
        return Response(
            content=buffer.getvalue(),
            media_type="image/webp",
            headers={
                "X-Compression-Mode": "turbo" if file_size > LARGE_FILE_THRESHOLD_KB*1024 else "normal",
                "X-Original-Size": str(file_size),
                "X-Compressed-Size": str(len(buffer.getvalue()))
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Critical error in endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")