from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from PIL import Image
from io import BytesIO
import os

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

# Конфигурация
MAX_UNCOMPRESSED_SIZE_KB = 250     # Не сжимать файлы <250KB
LARGE_FILE_THRESHOLD_KB = 1024     # Порог для жёсткого сжатия
LARGE_FILE_TARGET_KB = 512         # Целевой размер для больших файлов
TARGET_RESOLUTION = (357, 204)     # Новое разрешение всех изображений

def compress_image(input_path: str) -> BytesIO:
    """Сжимает изображение с уменьшением разрешения"""
    file_size_kb = os.path.getsize(input_path) / 1024
    
    with Image.open(input_path) as img:
        # 1. Уменьшаем разрешение
        img.thumbnail(TARGET_RESOLUTION)
        
        output_buffer = BytesIO()
        original_format = img.format
        
        # 2. Возвращаем как есть для маленьких файлов
        if file_size_kb <= MAX_UNCOMPRESSED_SIZE_KB:
            img.save(output_buffer, format=original_format)
            output_buffer.seek(0)
            return output_buffer
        
        # 3. Настройки сжатия
        if file_size_kb > LARGE_FILE_THRESHOLD_KB:
            quality = 40  # Жёсткое сжатие
        else:
            quality = 70  # Обычное сжатие
        
        # 4. Формат сохранения
        if original_format == 'PNG' and img.mode in ('RGBA', 'LA'):
            target_format = 'PNG'
            params = {'format': target_format, 'compress_level': 6}
        else:
            target_format = 'JPEG'
            params = {'format': target_format, 'quality': quality, 'optimize': True}
        
        # 5. Процесс сжатия
        while True:
            output_buffer.seek(0)
            output_buffer.truncate()
            img.save(output_buffer, **params)
            
            current_size_kb = output_buffer.tell() / 1024
            
            # Условия выхода:
            if (current_size_kb <= MAX_UNCOMPRESSED_SIZE_KB or 
                quality <= 10 or 
                (file_size_kb > LARGE_FILE_THRESHOLD_KB and current_size_kb <= LARGE_FILE_TARGET_KB)):
                break
                
            quality = max(10, quality - 5)
            params['quality'] = quality
        
        output_buffer.seek(0)
        return output_buffer

@compress_router.get("/{filename}")
def get_compressed_image(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    try:
        compressed_image = compress_image(file_path)
        return Response(
            content=compressed_image.getvalue(),
            media_type="image/jpeg",
            headers={"X-Resolution": f"{TARGET_RESOLUTION[0]}x{TARGET_RESOLUTION[1]}"}
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")
    file_path = os.path.join(STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    try:
        # Проверка что это изображение
        with Image.open(file_path) as img:
            original_format = img.format.upper() if img.format else 'JPEG'
    except:
        raise HTTPException(400, "Invalid image file")
    
    # Получаем сжатое изображение
    compressed_image = compress_image(file_path)
    
    # Определяем Content-Type
    content_type = f"image/{original_format.lower()}" if original_format != 'JPEG' else 'image/jpeg'
    
    return Response(
        content=compressed_image.getvalue(),
        media_type=content_type,
        headers={"Content-Disposition": f"inline; filename=compressed_{filename}"}
    )