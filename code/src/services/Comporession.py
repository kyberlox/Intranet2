from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, FileResponse
import os
import asyncio
import pyvips
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import logging

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

MAX_WORKERS = 4
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

async def _turbo_compress(img_path: str) -> BytesIO:
    """Асинхронное сжатие с улучшенной обработкой ошибок"""
    def _sync_compress():
        try:
            # Проверка существования файла
            if not os.path.exists(img_path):
                logging.error(f"File not found: {img_path}")
                return None
                
            # Проверка размера файла
            if os.path.getsize(img_path) == 0:
                logging.error(f"Empty file: {img_path}")
                return None

            img = pyvips.Image.new_from_file(img_path, access='sequential')
            if img is None:
                logging.error(f"Failed to load image: {img_path}")
                return None

            buffer = BytesIO()
            file_size_kb = os.path.getsize(img_path) / 1024
            quality = 30 if file_size_kb > 1024 else 70

            img.webpsave_buffer(
                buffer,
                Q=quality,
                strip=True,
                smart_subsample=True,
                reduction_effort=4
            )
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            logging.error(f"Compression failed for {img_path}: {str(e)}")
            return None

    try:
        buffer = await asyncio.get_event_loop().run_in_executor(executor, _sync_compress)
        if buffer is None:
            raise ValueError("Compression returned None")
        return buffer
    except Exception as e:
        logging.error(f"Async compression error: {str(e)}")
        raise

@compress_router.get("/{filename}")
async def get_compressed_image(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    try:
        # 1. Проверка существования файла
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # 2. Проверка размера файла
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        # 3. Возврат без сжатия для маленьких файлов
        if file_size <= 250 * 1024:  # 250KB
            return FileResponse(file_path)

        # 4. Асинхронное сжатие
        buffer = await _turbo_compress(file_path)
        if buffer is None:
            raise HTTPException(status_code=500, detail="Compression failed")

        # 5. Проверка буфера перед использованием
        if not hasattr(buffer, 'getvalue'):
            raise ValueError("Invalid buffer object")

        return Response(
            content=buffer.getvalue(),
            media_type="image/webp",
            headers={"X-Compression": "turbo" if file_size > 1024*1024 else "normal"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")