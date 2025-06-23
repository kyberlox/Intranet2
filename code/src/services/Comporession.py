from fastapi import FastAPI, APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
import os
from io import BytesIO
from typing import Optional
from PIL import Image
import asyncio

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])

# Конфигурация
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)
MAX_UNCOMPRESSED_SIZE_KB = 256  # Если меньше - возвращаем как есть
LARGE_FILE_THRESHOLD_KB = 1024  # 1 МБ - порог для "жёсткого" сжатия
LARGE_FILE_TARGET_KB = 512+128      # Целевой размер для больших файлов

def _calculate_quality(file_size_kb: float) -> int:
    """Динамический подбор качества для ускорения сжатия."""
    if file_size_kb <= LARGE_FILE_THRESHOLD_KB:
        return 75
    # Линейно уменьшаем качество для очень больших файлов
    return max(10, 75 - int((file_size_kb - LARGE_FILE_THRESHOLD_KB) / 1000 * 50))

def _turbo_compress(img: Image.Image, original_format: str, file_size_kb: float) -> BytesIO:
    """Оптимизированное сжатие с динамическими параметрами."""
    buffer = BytesIO()
    
    # Определяем целевой формат
    target_format = "JPEG" if original_format == "PNG" else original_format
    
    # Параметры сжатия
    params = {
        "format": target_format,
        "quality": _calculate_quality(file_size_kb),
        "optimize": True,
        "progressive": True
    }
    
    # Конвертация PNG в JPEG (если нет прозрачности)
    if original_format == "PNG" and img.mode in ("RGBA", "LA"):
        img = img.convert("RGB")
    
    img.save(buffer, **params)
    buffer.seek(0)
    
    # Дополнительное сжатие, если не уложились в размер для больших файлов
    if file_size_kb > LARGE_FILE_THRESHOLD_KB and buffer.tell() / 1024 > LARGE_FILE_TARGET_KB:
        buffer = BytesIO()
        params["quality"] = max(10, params["quality"] - 15)
        img.save(buffer, **params)
        buffer.seek(0)
    
    return buffer

@compress_router.get("/{filename}")
async def get_compressed_image(
    filename: str,
    preserve_transparency: Optional[bool] = False
):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    # 1. Проверка существования файла
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # 2. Проверка размера файла
    file_size_kb = os.path.getsize(file_path) / 1024
    
    # 3. Возврат без сжатия для маленьких файлов
    if file_size_kb <= MAX_UNCOMPRESSED_SIZE_KB:
        return FileResponse(file_path)
    
    try:
        # 4. Загрузка и обработка изображения
        with Image.open(file_path) as img:
            original_format = img.format.upper() if img.format else "JPEG"
            
            # 5. Асинхронное сжатие
            buffer = await asyncio.to_thread(
                _turbo_compress,
                img,
                original_format,
                file_size_kb
            )
            
            # 6. Определение Content-Type
            content_type = (
                "image/jpeg" 
                if file_size_kb > LARGE_FILE_THRESHOLD_KB and original_format != "WEBP" 
                else f"image/{original_format.lower()}"
            )
            
            return Response(
                content=buffer.getvalue(),
                media_type=content_type,
                headers={
                    "Content-Disposition": f"inline; filename=compressed_{filename}",
                    "X-Compression-Mode": "turbo" if file_size_kb > LARGE_FILE_THRESHOLD_KB else "normal",
                    "X-Original-Size": f"{file_size_kb:.2f}KB",
                    "X-Compressed-Size": f"{buffer.tell() / 1024:.2f}KB"
                }
            )
    
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")