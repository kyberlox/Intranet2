from src.base.mongodb import FileModel
from src.base.B24 import B24

from bson.objectid import ObjectId
import requests
import os

STORAGE_PATH = "./files_db"

class File:
    def __init__(self, id=None):
        self.id = id

    def download_by_URL(self, url, path):
        response = requests.get(url)
        with open(path, 'wb') as file:
            file.write(response.context)
        return response.headers.get('Content-Type', 'unknown')



    def upload_inf_art(self, inf_id, art_id=None):
        try:
            b24 = B24()
            file_data = b24.get_file(self.id, inf_id)

            filename = file_data["NAME"]
            print(filename)

            filename_parts = filename.split('.')
            file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

            # Генерируем уникальное имя файла
            unique_name = str(ObjectId()) + file_ext
            file_path = os.path.join(STORAGE_PATH, unique_name)

            #Проверяем нет ли такого файла уже в БД

            # Сохраняем файл
            content_type = self.download_by_URL(file_data["DOWNLOAD_URL"], file_path)

            result = {
                "original_name": filename,
                "stored_name": unique_name,
                "content_type": content_type,
                "article_id": art_id,
                "b24_id": self.id,
                "file_url": f"/api/files/{unique_name}"  # Прямой URL
            }

            #записать в mongodb
            inserted_id = FileModel().add(result)

            return {
                "id": str(inserted_id),
                "original_name": filename,
                "stored_name": unique_name,
                "content_type": content_type,
                "article_id": art_id,
                "b24_id": self.id,
                "file_url": f"/api/files/{unique_name}"
            }

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании файла: {e}")
            return None



