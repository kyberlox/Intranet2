from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from PIL import Image
from io import BytesIO
import os

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

# Ваши настройки конфигурации
MAX_UNCOMPRESSED_SIZE_KB = 250      # Не сжимать файлы меньше этого размера
LARGE_FILE_THRESHOLD_KB = 1024      # Порог для "жёсткого" сжатия
LARGE_FILE_TARGET_KB = 512          # Целевой размер для больших файлов

def compress_image(input_path: str) -> BytesIO:
    """Сжимает изображение согласно вашим настройкам"""
    file_size_kb = os.path.getsize(input_path) / 1024
    
    with Image.open(input_path) as img:
        output_buffer = BytesIO()
        original_format = img.format
        
        # 1. Возвращаем как есть для маленьких файлов
        if file_size_kb <= MAX_UNCOMPRESSED_SIZE_KB:
            img.save(output_buffer, format=original_format)
            output_buffer.seek(0)
            return output_buffer
        
        # 2. Определяем параметры сжатия
        if file_size_kb > LARGE_FILE_THRESHOLD_KB:
            # Жёсткое сжатие для больших файлов
            quality = 40
            target_format = 'JPEG'
        else:
            # Обычное сжатие
            quality = 70
            target_format = 'JPEG' if original_format != 'PNG' else original_format
        
        # 3. Конвертируем PNG без прозрачности в JPEG
        if original_format == 'PNG' and img.mode not in ('RGBA', 'LA'):
            img = img.convert('RGB')
            target_format = 'JPEG'
        
        # 4. Процесс сжатия
        while True:
            output_buffer.seek(0)
            output_buffer.truncate()
            img.save(output_buffer, format=target_format, quality=quality, optimize=True)
            
            current_size_kb = output_buffer.tell() / 1024
            
            # Условия выхода:
            # - Уложились в размер
            # - Достигли минимального качества
            # - Для больших файлов: достигли целевого размера
            if (current_size_kb <= MAX_UNCOMPRESSED_SIZE_KB or 
                quality <= 10 or 
                (file_size_kb > LARGE_FILE_THRESHOLD_KB and current_size_kb <= LARGE_FILE_TARGET_KB)):
                break
                
            quality = max(10, quality - 5)
        
        output_buffer.seek(0)
        return output_buffer

@compress_router.get("/{filename}")
def get_compressed_image(filename: str):
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