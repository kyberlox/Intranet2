from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from PIL import Image
from io import BytesIO
import os
import asyncio

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

# Конфигурация сжатия
MAX_UNCOMPRESSED_SIZE_KB = 250    # Не сжимать файлы меньше этого размера
LARGE_FILE_THRESHOLD_KB = 1024    # Порог для "жёсткого" сжатия
LARGE_FILE_TARGET_KB = 512        # Целевой размер для больших файлов

async def compress_image(file_path: str) -> BytesIO:
    """Умное сжатие с учетом конфигурации"""
    file_size_kb = os.path.getsize(file_path) / 1024
    
    with Image.open(file_path) as img:
        buffer = BytesIO()
        
        # Определяем параметры сжатия
        if file_size_kb > LARGE_FILE_THRESHOLD_KB:
            quality = 40  # Жёсткое сжатие для больших файлов
        else:
            quality = 70  # Нормальное качество
            
        # Сохраняем в оптимальном формате
        if img.format == 'PNG' and img.mode in ('RGBA', 'LA'):
            img.save(buffer, format='PNG', optimize=True)
        else:
            img.convert('RGB').save(buffer, format='JPEG', quality=quality, optimize=True)
            
        # Досжатие, если не уложились в лимит для больших файлов
        if file_size_kb > LARGE_FILE_THRESHOLD_KB:
            while buffer.tell() / 1024 > LARGE_FILE_TARGET_KB and quality > 20:
                quality -= 5
                buffer.seek(0)
                buffer.truncate()
                img.convert('RGB').save(buffer, format='JPEG', quality=quality, optimize=True)
        
        buffer.seek(0)
        return buffer

@compress_router.get("/{filename}")
async def get_compressed_image(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    file_size_kb = os.path.getsize(file_path) / 1024
    
    # 1. Возврат без сжатия для маленьких файлов
    if file_size_kb <= MAX_UNCOMPRESSED_SIZE_KB:
        return FileResponse(file_path)
    
    try:
        # 2. Асинхронное сжатие
        buffer = await asyncio.to_thread(compress_image, file_path)
        
        return Response(
            content=buffer.getvalue(),
            media_type="image/jpeg",
            headers={
                "X-Compression-Mode": "turbo" if file_size_kb > LARGE_FILE_THRESHOLD_KB else "normal",
                "X-Original-Size": f"{file_size_kb:.1f}KB",
                "X-Compressed-Size": f"{buffer.tell()/1024:.1f}KB"
            }
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")