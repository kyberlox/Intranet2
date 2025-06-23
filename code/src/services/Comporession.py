from fastapi import FastAPI, APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
import os
from io import BytesIO
from typing import Optional
from PIL import Image
import asyncio

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])

STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)


def _turbo_compress(img: Image.Image, original_format: str, is_large_file: bool = False) -> BytesIO:
    """Сверхбыстрое сжатие с жёсткими настройками для больших файлов."""
    buffer = BytesIO()
    target_format = original_format if original_format != "PNG" else "JPEG"
    
    # Параметры по умолчанию (баланс скорость/качество)
    params = {
        "format": target_format,
        "quality": 30 if is_large_file else 75,
        "optimize": True,
        "progressive": True  # Для JPEG (ускоряет загрузку в браузере)
    }
    
    # Для PNG -> JPEG (если не нужна прозрачность)
    if original_format == "PNG" and img.mode in ("RGBA", "LA"):
        img = img.convert("RGB")
    
    img.save(buffer, **params)
    buffer.seek(0)
    return buffer

@compress_router.get("/{filename}")
async def get_compressed_image(filename: str, preserve_transparency: Optional[bool] = False):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    # 1. Быстрая проверка файла
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # 2. Определяем размер и формат
        file_size_kb = os.path.getsize(file_path) / 1024
        with Image.open(file_path) as img:
            original_format = img.format.upper() if img.format else "JPEG"
            
            # 3. Возвращаем как есть, если файл маленький
            if file_size_kb <= 250:
                return FileResponse(file_path)
            
            # 4. Жёсткое сжатие для больших файлов (>1 МБ)
            is_large_file = file_size_kb > 1024
            buffer = await asyncio.to_thread(
                _turbo_compress,
                img,
                original_format,
                is_large_file
            )
            
            # 5. Форсируем JPEG для больших файлов (если не WEBP)
            if is_large_file and original_format != "WEBP":
                content_type = "image/jpeg"
            else:
                content_type = f"image/{original_format.lower()}"
            
            return Response(
                content=buffer.getvalue(),
                media_type=content_type,
                headers={
                    "Content-Disposition": f"inline; filename=compressed_{filename}",
                    "X-Compression-Mode": "turbo" if is_large_file else "normal"
                }
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")