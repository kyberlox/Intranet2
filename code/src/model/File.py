from src.base.mongodb import FileModel
from src.base.B24 import B24

from bson.objectid import ObjectId
import requests
import os

STORAGE_PATH = "./files_db"

class File:
    def __init__(self, id=None):
        self.id = id



    def download_file(self, url):
        try:
            # Отправляем GET-запрос к URL
            response = requests.get(f"https://portal.emk.ru{url}", stream=True)
            response.raise_for_status()  # Проверяем, нет ли ошибок

            filename = response.headers#["content-disposition"]
            print(filename)

            filename_parts = filename.split('.')
            file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

            # Генерируем уникальное имя файла
            unique_name = str(ObjectId()) + file_ext
            file_path = os.path.join(STORAGE_PATH, unique_name)

            # Сохраняем файл
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            content_type = response.headers.get('Content-Type', 'unknown')

            return {
                "original_name": filename,
                "stored_name": unique_name,
                "content_type": content_type,
                "file_url": f"/api/files/{unique_name}"  # Прямой URL
            }

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при скачивании файла: {e}")
            return None

    def download(self, inf_id, art_id, property):
        #получить ссылку с битрикса
        download_links = B24().get_file(inf_id, art_id, property)

        result = []
        #скачать
        for download_link in download_links:
            print(download_link)
            file_data = self.download_file(download_link)

            #загрузить в mongo
            result.append( FileModel().add(file_data) )

        #вывести данные
        return result



    def getURl(self):
        pass
