from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
import os
from io import BytesIO
from typing import Optional
from PIL import Image
import asyncio
import pyvips  # Убедитесь, что установлен (pip install pyvips)

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])

# Конфигурация (возвращаем старые параметры)
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)
MAX_UNCOMPRESSED_SIZE_KB = 250  # Не сжимаем файлы меньше этого размера
LARGE_FILE_THRESHOLD_KB = 1024   # Порог для "жёсткого" сжатия (1 МБ)
LARGE_FILE_TARGET_KB = 512       # Целевой размер для больших файлов

async def _turbo_compress(img_path: str) -> BytesIO:
    """Асинхронное сжатие через pyvips"""
    def _sync_compress():
        try:
            img = pyvips.Image.new_from_file(img_path)
            buffer = BytesIO()
            
            # Динамическое качество
            file_size_kb = os.path.getsize(img_path) / 1024
            quality = 30 if file_size_kb > 1024 else 70
            
            img.webpsave_buffer(buffer, Q=quality, strip=True)
            buffer.seek(0)
            return buffer
        except Exception as e:
            raise RuntimeError(f"Compression failed: {str(e)}")

@compress_router.get("/{filename}")
async def get_compressed_image(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_size_kb = os.path.getsize(file_path) / 1024
    
    # 1. Возврат без сжатия для маленьких файлов
    if file_size_kb <= 250:
        return FileResponse(file_path)
    
    try:
        # 2. Асинхронное сжатие
        buffer = await _turbo_compress(file_path)
        
        return Response(
            content=buffer.getvalue(),
            media_type="image/webp"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))