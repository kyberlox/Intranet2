from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from PIL import Image
from io import BytesIO
import os
import asyncio

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

async def compress_image(file_path: str, max_size_kb: int = 500) -> BytesIO:
    """Простое сжатие через PIL"""
    with Image.open(file_path) as img:
        buffer = BytesIO()
        
        # Автоматический выбор формата
        if img.format == 'PNG' and img.mode in ('RGBA', 'LA'):
            img.save(buffer, format='PNG', optimize=True)
        else:
            img.convert('RGB').save(buffer, format='JPEG', quality=70, optimize=True)
        
        buffer.seek(0)
        return buffer

@compress_router.get("/{filename}")
async def get_compressed_image(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    # Простые проверки
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    file_size = os.path.getsize(file_path)
    
    # Возвращаем как есть для маленьких файлов
    if file_size <= 250 * 1024:  # 250KB
        return FileResponse(file_path)
    
    try:
        buffer = await asyncio.to_thread(compress_image, file_path)
        return Response(
            content=buffer.getvalue(),
            media_type="image/jpeg",
            headers={"X-Compressed": "true"}
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")