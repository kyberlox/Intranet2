from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, Response
from PIL import Image
from io import BytesIO
import os

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

# Конфигурация по умолчанию
DEFAULT_CONFIG = {
    "max_uncompressed_kb": 300,      # Не сжимать файлы меньше этого размера
    "large_file_threshold_kb": 1500,  # Порог для повышенного сжатия
    "target_resolution": (357, 204),  # Ширина, высота (None - сохранять оригинал)
    "normal_quality": 85,             # Качество для обычных файлов (1-100)
    "high_quality": 65,               # Качество для больших файлов
    "min_quality": 30,                # Минимальное качество при досжатии
    "force_jpeg": True                # Всегда конвертировать в JPEG (кроме PNG с прозрачностью)
}

def compress_image(
    input_path: str,
    config: dict = DEFAULT_CONFIG
) -> BytesIO:
    """Умное сжатие с конфигурируемыми параметрами"""
    file_size_kb = os.path.getsize(input_path) / 1024
    
    with Image.open(input_path) as img:
        # 1. Уменьшение разрешения (если задано в конфиге)
        if config["target_resolution"]:
            img.thumbnail(config["target_resolution"])
        
        output_buffer = BytesIO()
        original_format = img.format
        
        # 2. Возврат без сжатия для маленьких файлов
        if file_size_kb <= config["max_uncompressed_kb"]:
            img.save(output_buffer, format=original_format)
            output_buffer.seek(0)
            return output_buffer
        
        # 3. Определение параметров сжатия
        if file_size_kb > config["large_file_threshold_kb"]:
            quality = config["high_quality"]
        else:
            quality = config["normal_quality"]
        
        # 4. Выбор формата
        if not config["force_jpeg"] and original_format == 'PNG' and img.mode in ('RGBA', 'LA'):
            target_format = 'PNG'
            params = {'format': target_format, 'compress_level': 6}
        else:
            target_format = 'JPEG'
            params = {'format': target_format, 'quality': quality, 'optimize': True}
        
        # 5. Процесс сжатия с контролем размера
        while True:
            output_buffer.seek(0)
            output_buffer.truncate()
            img.save(output_buffer, **params)
            
            current_size_kb = output_buffer.tell() / 1024
            
            # Условия выхода:
            if (current_size_kb <= config["max_uncompressed_kb"] or 
                quality <= config["min_quality"]):
                break
                
            quality = max(config["min_quality"], quality - 5)
            params['quality'] = quality
        
        output_buffer.seek(0)
        return output_buffer

@compress_router.get("/{filename}")
def get_compressed_image(
    filename: str,
    quality: int = Query(None, ge=10, le=100, description="Качество сжатия (10-100)"),
    width: int = Query(None, ge=100, description="Ширина результата"),
    height: int = Query(None, ge=100, description="Высота результата")
):
    """Эндпоинт с настройками качества через query-параметры"""
    file_path = os.path.join(STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    try:
        # Создаем конфиг на основе параметров запроса
        config = DEFAULT_CONFIG.copy()
        if quality:
            config.update({
                "normal_quality": quality,
                "high_quality": max(30, quality - 20)
            })
        if width and height:
            config["target_resolution"] = (width, height)
        
        compressed_image = compress_image(file_path, config)
        
        return Response(
            content=compressed_image.getvalue(),
            media_type="image/jpeg",
            headers={
                "X-Resolution": f"{config['target_resolution'][0]}x{config['target_resolution'][1]}",
                "X-Quality": str(quality if quality else config['normal_quality'])
            }
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")
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