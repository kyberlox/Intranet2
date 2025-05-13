from src.base.mongodb import FileModel
from src.base.B24 import B24

from bson.objectid import ObjectId
import requests
import os

from fastapi import APIRouter, Body, UploadFile, HTTPException

file_router = APIRouter(prefix="/file", tags=["Файлы"])

STORAGE_PATH = "./files_db"

class File:
    def __init__(self, id=None):
        self.id = id

    def download_by_URL(self, url, path):
        response = requests.get(url)
        with open(path, 'wb') as file:
            file.write(response.content)
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

            #ТУТ НУЖНО ПРОВЕРИТЬ НЕОБХОДИМОСТЬ ДОБАВЛЕНИЯ ФАЙЛА

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

    def need_update_file(self,  art_id, files_id):
        # print('1)', files_id, 'файлы, которые нужно добавить', art_id)
        result = FileModel(art_id).find_all_by_art_id()
        DB_files_id = []
        DB_files_path = {}
        if result is None: # если в бд нет такого файла
            return files_id 
        else:
            # цикло для сбора данных с БД
            for res in result: # выдергиваем все b24_id из монго по art_id 
                file = res["b24_id"]
                DB_files_id.append(file)
                DB_files_path[file] = f'{STORAGE_PATH}/{res["stored_name"]}'

            # цикл для проверки если в DB_files_id есть файлы, которых нет в files_id
            for file in DB_files_id:
                if file not in files_id:
                    FileModel(file).remove() #если лишний b24_id -> удалить запись в mongo и сам файл -> #не нужно добавлять
                    os.remove(DB_files_path[file])
                    # print('лишний файл в БД', file, art_id)
                else:
                    files_id.remove(file) # удаляем из входящего списка все файлы которые уже есть в DB_files_id

            # print('2)', files_id, 'файлы, которые нужно добавить', art_id)

            return files_id # вернет пустой список если все файлы уже есть в БД, в обратном случае вернет только те файлы, которых в БД нет
    
    def get_files(self):
        file_data = FileModel(id=self.id).find_all_by_art_id()

        file_list = []
        
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")
        else:
            for file in file_data:
                file_info = {}
                file_info["id"] = str(file["_id"])
                file_info["url"] = file["file_url"]
                file_info["original_name"] = file["original_name"]
                file_info["content_type"] = file["content_type"]
                file_list.append(file_info)
            return file_list

@file_router.post("/upload")
async def upload_file(file: UploadFile):
    try:
        # Получаем расширение файла
        filename_parts = file.filename.split('.')
        file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

        # Генерируем уникальное имя файла
        unique_name = str(ObjectId()) + file_ext
        file_path = os.path.join(STORAGE_PATH, unique_name)

        # Сохраняем файл на диск
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Сохраняем метаданные
        file_data = {
            "original_name": file.filename,
            "stored_name": unique_name,
            "content_type": file.content_type,
            "file_url": f"/api/files/{unique_name}"  # Прямой URL
        }

        inserted_id = FileModel().add(file_data)

        return {
            "id": str(inserted_id),
            "file_url": file_data["file_url"],
            "original_name": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@file_router.get("/info/{file_id}")
async def get_file_info(file_id: str):
    try:
        if not ObjectId.is_valid(file_id):
            raise HTTPException(status_code=400, detail="Invalid file ID")

        file_data = FileModel(id = ObjectId(file_id)).find_by_id()

        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        return {
            "id": str(file_data["_id"]),
            "url": file_data["file_url"],
            "original_name": file_data["original_name"],
            "content_type": file_data["content_type"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@file_router.get("/info/article_id/{article_id}")
async def get_file_by_article(article_id: int):
    try:
        file_data = File(id=article_id).get_files()

        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        return file_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@file_router.get("/info/b24_id/{b24_id}")
async def get_file_by_b24(b24_id: str):
    try:
        file_data = FileModel(id = b24_id).find_by_b24_id()

        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        return {
            "id": str(file_data["_id"]),
            "url": file_data["file_url"],
            "original_name": file_data["original_name"],
            "content_type": file_data["content_type"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@file_router.delete("/{file_id}")
async def delete_file(file_id: str):
    file_data = FileModel(id = ObjectId(file_id)).find_by_id()
    if not file_data:
        raise HTTPException(404, detail="File not found")

    try:
        os.remove(os.path.join(STORAGE_PATH, file_data["stored_name"]))
        FileModel(id = ObjectId(file_id)).remove()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))


