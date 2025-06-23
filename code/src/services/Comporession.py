from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from PIL import Image
from io import BytesIO
import os

compress_router = APIRouter(prefix="/compress_image", tags=["Компрессия изображений"])
STORAGE_PATH = "./files_db"
os.makedirs(STORAGE_PATH, exist_ok=True)

# Конфигурация разрешения
TARGET_WIDTH = 357
TARGET_HEIGHT = 204

def resize_image(input_path: str) -> BytesIO:
    """Только изменяет разрешение без сжатия"""
    with Image.open(input_path) as img:
        # Сохраняем исходный формат
        original_format = img.format
        
        # Изменяем размер с сохранением пропорций
        img.thumbnail((TARGET_WIDTH, TARGET_HEIGHT))
        
        # Сохраняем в исходном формате
        output_buffer = BytesIO()
        img.save(output_buffer, format=original_format)
        output_buffer.seek(0)
        
        return output_buffer

@compress_router.get("/{filename}")
def get_resized_image(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    try:
        # Проверяем, что это изображение
        with Image.open(file_path) as img:
            original_format = img.format.lower() if img.format else 'jpeg'
        
        # Изменяем разрешение
        resized_image = resize_image(file_path)
        
        return Response(
            content=resized_image.getvalue(),
            media_type=f"image/{original_format}",
            headers={
                "X-Original-Resolution": f"{img.width}x{img.height}",
                "X-Target-Resolution": f"{TARGET_WIDTH}x{TARGET_HEIGHT}"
            }
        )
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")