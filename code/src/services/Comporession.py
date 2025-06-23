from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, FileResponse
import os
import asyncio
import pyvips
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import logging

# Конфигурация
compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

# Оптимальное количество потоков (подбирается экспериментально)
MAX_WORKERS = 4
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

async def _turbo_compress(img_path: str) -> BytesIO:
    """Асинхронное сжатие с контролем памяти"""
    def _sync_compress():
        try:
            img = pyvips.Image.new_from_file(img_path, access='sequential')
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
            return buffer
        except Exception as e:
            logging.error(f"Compression error: {str(e)}")
            raise

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _sync_compress)

@compress_router.get("/{filename}")
async def get_compressed_image(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_size_kb = os.path.getsize(file_path) / 1024
    
    # Быстрый возврат для маленьких файлов
    if file_size_kb <= 250:
        return FileResponse(file_path)
    
    try:
        buffer = await _turbo_compress(file_path)
        return Response(
            content=buffer.getvalue(),
            media_type="image/webp",
            headers={"X-Compression": "turbo" if file_size_kb > 1024 else "normal"}
        )
    except Exception as e:
        logging.error(f"Failed to process {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")