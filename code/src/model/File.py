from src.base.mongodb import FileModel
from src.base.B24 import B24
from src.services.LogsMaker import LogsMaker

from fastapi import FastAPI, UploadFile
from fastapi import File as webFile

from bson.objectid import ObjectId
import requests
import os

from fastapi import APIRouter, Body, UploadFile, HTTPException

import os
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv('HOST')

STORAGE_PATH = "./files_db"
USER_STORAGE_PATH = "./files_db/user_photo"

file_router = APIRouter(prefix="/file", tags=["Файлы"])

class File:
    def __init__(self, id=None, art_id =None, b24_id=None):

        if id is not None:
            if type(id) == type(ObjectId("a"*24)):
                id = id
            elif type(id) == type(str()) and id != '':
                id = ObjectId(id)
        self.id = id
        self.art_id = art_id
        self.b24_id = b24_id

    def download_by_URL(self, url, path):
        if "https://portal.emk.ru" in url:
            response = requests.get(url)
        else:
            response = requests.get(f"https://portal.emk.ru{url}")
        with open(path, 'wb') as file:
            file.write(response.content)
        return response.headers.get('Content-Type', 'unknown')

    def upload_inf_art(self, art_id=None, is_preview = False, need_all_method = True, inf_id=None):
        try:
            b24 = B24()
            #print(f"ID фала = {self.b24_id} | ID инфоблока = {inf_id} | ID статьи = {art_id}")
            filename = "___"
            try:
                if need_all_method:
                    file_data = b24.get_all_files(self.b24_id)
                    
                    if "ORIGINAL_NAME" in file_data:
                        filename = file_data["ORIGINAL_NAME"]
                    elif "FILE_NAME" in file_data:
                        filename = file_data["FILE_NAME"]
                    elif "NAME" in file_data:
                        filename = file_data["NAME"]

                    filename_parts = filename.split('.')
                    file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

                    # Генерируем уникальное имя файла
                    unique_name = str(ObjectId()) + file_ext
                    file_path = os.path.join(STORAGE_PATH, unique_name)

                    # Сохраняем файл
                    content_type = self.download_by_URL(file_data["SRC"], file_path)


                else:
                    file_data = b24.get_file(self.b24_id, inf_id)

                    if "ORIGINAL_NAME" in file_data:
                        filename = file_data["ORIGINAL_NAME"]
                    elif "FILE_NAME" in file_data:
                        filename = file_data["FILE_NAME"]
                    elif "NAME" in file_data:
                        filename = file_data["NAME"]

                    filename_parts = filename.split('.')
                    file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

                    # Генерируем уникальное имя файла
                    unique_name = str(ObjectId()) + file_ext
                    file_path = os.path.join(STORAGE_PATH, unique_name)

                    # Сохраняем файл
                    content_type = self.download_by_URL(file_data["DOWNLOAD_URL"], file_path)
                
                result = {
                    "original_name": filename,
                    "stored_name": unique_name,
                    "content_type": content_type,
                    "article_id": art_id,
                    "b24_id": self.b24_id,
                    "is_archive": False,
                    "is_preview": is_preview,
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
                    "b24_id": self.b24_id,
                    "is_archive": False,
                    "is_preview" : is_preview,
                    "file_url": f"/api/files/{unique_name}"
                }

            except:
                LogsMaker().warning_message(f"Фатальная ошибка записи файла: {self.b24_id}, из статьи {art_id}, инфоблока {inf_id}, применение метода Матренина: {need_all_method}")

            
        except requests.exceptions.RequestException as e:
            # print(f"Ошибка при скачивании файла: {e}")
            return LogsMaker().error_message(e)



    def add_link(self, link, art_id):
        filename = link.split("/")[-2]
        data = {
            "original_name": link,
            "stored_name": filename,
            "content_type": "link",
            "article_id": art_id,
            "b24_id": self.b24_id,
            "is_archive": False,
            "is_preview": False,
            "file_url": link  # Прямой URL
        }
            
        #записать в mongodb
        inserted_id = FileModel().add(data)

        new_url = data["file_url"]

        #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!!!!!
        return link
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def need_update_url_file(self,  art_id, filename):
        # print('1)', files_id, 'файлы, которые нужно добавить', art_id)
        result = FileModel(art_id=art_id).find_all_by_art_id()
        DB_files_name = []

        if result is None: # если в бд нет такой статьи
            return True 
        else:
            # цикл для сбора данных с БД
            for res in result: # выдергиваем все original_name из монго по art_id 
                fl = res["original_name"]
                DB_files_name.append(fl)

            # цикл для проверки если в DB_files_id есть файлы, которых нет в files_id
            for fl in DB_files_name:
                #print(filename)
                #print(fl)
                if filename == 'uf.php?attachedId=128481&auth%5Baplogin%5D=1&auth%5Bap%5D=j6122m0ystded5ag&action=show&ncc=1':
                    return False
                elif fl == filename:
                    return False
            return True

    def upload_by_URL(self, url, art_id, b24_id = None, is_preview = False):
        filename = url.split("/")[-1]
        
        filename_parts = filename.split('.')
        file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

        #тут надо проверить, нет ли такого файла уже в БД?
        if self.need_update_url_file(art_id, filename):
            # Генерируем уникальное имя файла
            unique_name = str(ObjectId()) + file_ext
            file_path = os.path.join(STORAGE_PATH, unique_name)

            #скачать файл по ссылке
            response = requests.get(f"https://portal.emk.ru{url}")
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            content_type = response.headers.get('Content-Type', 'unknown')

            result = {
                        "original_name": filename,
                        "stored_name": unique_name,
                        "content_type": content_type,
                        "article_id": art_id,
                        "b24_id": self.b24_id,
                        "is_archive": False,
                        "is_preview": is_preview,
                        "file_url": f"/api/files/{unique_name}"  # Прямой URL
                    }
            
            #записать в mongodb
            inserted_id = FileModel().add(result)

            new_url = result["file_url"]
            
            return f"{DOMAIN}{new_url}"
            
        else: #надо заменить
            self.art_id = art_id
            files = self.get_files_by_art_id()
            for fl in files:
                if fl["original_name"] == filename:
                    #перезаписываем
                    unique_name = fl["stored_name"]
                    file_path = os.path.join(STORAGE_PATH, unique_name)
                    response = requests.get(f"{DOMAIN}{url}")
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    
                    new_url = fl["file_url"]
                    
                    return f"{DOMAIN}{new_url}"

    def save_by_URL(self, url, art_id, b24_id = None, is_preview = False):
        filename = url.split("/")[-1]
        
        filename_parts = filename.split('.')
        file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

        #тут надо проверить, нет ли такого файла уже в БД?
        if self.need_update_url_file(art_id, filename):
            # Генерируем уникальное имя файла
            unique_name = str(ObjectId()) + file_ext
            file_path = os.path.join(STORAGE_PATH, unique_name)

            #скачать файл по ссылке
            print(url)
            response = requests.get(url)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            content_type = response.headers.get('Content-Type', 'unknown')

            result = {
                        "original_name": filename,
                        "stored_name": unique_name,
                        "content_type": content_type,
                        "article_id": art_id,
                        "b24_id": self.b24_id,
                        "is_archive": False,
                        "is_preview": is_preview,
                        "file_url": f"/api/files/{unique_name}"  # Прямой URL
                    }
            
            #записать в mongodb
            inserted_id = FileModel().add(result)

            new_url = result["file_url"]
            
            return f"{DOMAIN}{new_url}"
            
        else: #надо заменить
            self.art_id = art_id
            files = self.get_files_by_art_id()
            for fl in files:
                if fl["original_name"] == filename:
                    #перезаписываем
                    unique_name = fl["stored_name"]
                    file_path = os.path.join(STORAGE_PATH, unique_name)
                    response = requests.get(url)
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    
                    new_url = fl["file_url"]
                    
                    return f"{DOMAIN}{new_url}"

    def need_update_file(self,  art_id, files_id):
        # print('1)', files_id, 'файлы, которые нужно добавить', art_id)
        result = FileModel(art_id=art_id).find_all_by_art_id()
        DB_files_id = []
        DB_files_path = {}

        if result is None: # если в бд нет такого файла
            return files_id 
        else:
            # цикл для сбора данных с БД
            for res in result: # выдергиваем все b24_id из монго по art_id 
                fl = res["b24_id"]
                DB_files_id.append(fl)
                DB_files_path[fl] = f'{STORAGE_PATH}/{res["stored_name"]}'

            # цикл для проверки если в DB_files_id есть файлы, которых нет в files_id
            for fl in DB_files_id:
                if fl not in files_id:
                    FileModel(b24_id = fl).go_archive() #если лишний b24_id -> удалить запись в mongo и сам файл -> #не нужно добавлять
                    #os.remove(DB_files_path[fl])
                    # print('лишний файл в БД', file, art_id)
                else:
                    files_id.remove(fl) # удаляем из входящего списка все файлы которые уже есть в DB_files_id

            # print('2)', files_id, 'файлы, которые нужно добавить', art_id)

            return files_id # вернет пустой список если все файлы уже есть в БД, в обратном случае вернет только те файлы, которых в БД нет
    
    def get_file(self):
        file_data = FileModel(id=self.id).find_by_id()
        
        if file_data["is_archive"]:
            raise HTTPException(status_code=404, detail="File not found")
        else:
            file_data["id"] = str(file_data["_id"])
            file_data.pop("_id")
            return file_data

    def get_files_by_art_id(self):
        file_data = FileModel(art_id=int(self.art_id)).find_all_by_art_id()
        file_list = []
        
        if not file_data:
            raise HTTPException(status_code=404, detail="Files not found")
        else:
            for file in file_data:
                if not file["is_archive"]:
                    file_info = {}
                    file_info["id"] = str(file["_id"])
                    file_info["original_name"] = file["original_name"]
                    file_info["stored_name"] = file["stored_name"]
                    file_info["content_type"] = file["content_type"]

                    #файлы делятся по категориям
                    if "image" in file["content_type"]:
                        file_info["type"] = "image"
                    elif "video" in file["content_type"]:
                        file_info["type"] = "video"
                    elif "link" in file["content_type"]:
                        file_info["type"] = "video_embed"
                    else:
                        file_info["type"] = "documentation"

                    file_info["article_id"] = file["article_id"]
                    file_info["b24_id"] = file["b24_id"]
                    file_info["file_url"] = file["file_url"]
                    file_info["is_archive"] = file["is_archive"]
                    file_info["is_preview"] = file["is_preview"]

                    file_list.append(file_info)

            

            return file_list

    def need_update_link(self):
        pass

    def get_link_as_file(self):
        pass



    def get_users_photo(self):
        #переделать с учетом is_archive
        file_data = FileModel(id=self.id).find_user_photo_by_id()
        
        
        if not file_data or file_data["is_archive"]:
            raise HTTPException(status_code=404, detail="File not found")
        else:
            file_info = {}
            file_info["id"] = str(file_data["_id"])
            file_info["name"] = file_data["name"]
            file_info["format"] = file_data["format"]
            file_info["uuid"] = file_data["uuid"]
            file_info["URL"] = file_data["URL"]
            file_info["b24_url"] = file_data["b24_url"]
            file_info["is_archive"] = file_data["is_archive"]
                

            return file_info

    def dowload_user_photo(self, url):
        name = url.split("/")[-1]
        form = name.split(".")[-1]
        img_path = f"{USER_STORAGE_PATH}/{name}"

        with requests.get(url, stream=True) as r:
            with open(img_path, "wb") as f:
                f.write(r.content)
        
        return (name, form)

    def add_user_img(self, b24_url : str, uuid : str):
        #скачать файл
        try:

            name, form = self.dowload_user_photo(b24_url)

            #определить ссылку
            url = f"/api/user_files/{name}"

            #собрать данные
            file_data = {
                "name" : name,
                "format" : form,
                "uuid" : uuid,
                "URL" : url,
                "b24_url" : b24_url,
                "is_archive" : False
            }
            print(file_data, uuid)

            new_id = FileModel().add_user_photo(file_data)

            file_data["id"] = new_id

            return file_data
        except:
            print(uuid)
    
    def delete_user_img(self):
        file_data = FileModel(id = self.id).find_user_photo_by_id()
        if not file_data:
            raise HTTPException(404, detail="File not found")
        
        try:
            FileModel(id = self.id).remove_user_photo()
            return {"status": "to_archive"}
        except Exception as e:
            # raise HTTPException(500, detail=str(e))
            return LogsMaker().error_message(e)
    
    # Блок создания индексов
    def index_files(self):
        return FileModel().create_index_files()

    def index_user_photo(self):
        return FileModel().create_index_user_photo()

    def editor_add_file(self, file : webFile):
        #!!!!!!!внедрить проверки
        
        
        # Генерируем уникальное имя файла
        filename = file.filename
        filename_parts = filename.split('.')
        file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''
        unique_name = str(ObjectId()) + file_ext
        file_path = os.path.join(STORAGE_PATH, unique_name)

        # Если нужно сохранить файл на диск
        #with file.file:
            #contents = file.file.read()
            #with open(file_path, "wb") as f:
                #f.write(contents)

        file_info = {
            "original_name": filename,
            "stored_name": unique_name,
            "content_type": str(file.content_type),
            "article_id": int(self.art_id),
            "b24_id": None,
            "is_archive": False,
            "is_preview" : False,
            "file_url": f"/api/files/{unique_name}"
        }

        inserted_id = FileModel().add(file_info)

        # Проверяем, что inserted_id можно преобразовать в строку
        if hasattr(inserted_id, "__str__"):
            inserted_id_str = str(inserted_id)
        else:
            inserted_id_str = str(inserted_id)  # На крайний случай

        #file_info["id"] = str(inserted_id)
        #return file_info

        return {
            **file_info,
            "id": str(inserted_id)
        }
    
    def editor_chenge_file(self, file : webFile):
        #найти файл
        #заменить id и отправить предыдущую версию в архив
        #скачать под старым id
        #заменить метданные
        pass
    
    def set_is_preview(self ):
        #найти статью файла
        #проверить есть ли в ней первью
        #заменить, если есть
        #найти файл сделать его превью
        pass


        

# @file_router.put("/create_indexes")
# async def create_mongo_indexes():
#     return FileModel().create_indexes()

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
async def get_file_article(article_id: int):
    try:
        file_data = File(art_id=article_id).get_files_by_art_id()

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
    #изменить статус
    file_data = FileModel(id = ObjectId(file_id)).find_by_id()
    if not file_data:
        raise HTTPException(404, detail="File not found")
    
    try:
        FileModel(id = ObjectId(file_id)).remove()
        return {"status": "to_archive"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    """
    file_data = FileModel(id = ObjectId(file_id)).find_by_id()
    if not file_data:
        raise HTTPException(404, detail="File not found")

    try:
        os.remove(os.path.join(STORAGE_PATH, file_data["stored_name"]))
        FileModel(id = ObjectId(file_id)).remove()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    """
    pass



@file_router.post("/get_user_photo/{uuid}")
async def get_user_photo(uuid : str):
    return FileModel().find_user_photo_by_uuid(uuid)

@file_router.get("/get_user_photo/{file_id}")
async def get_user_photo(file_id: str):
    return FileModel(id = ObjectId(file_id)).find_user_photo_by_id(uuid)

@file_router.post("/add_user_photo/{b24_url}/{uuid}")
async def add_user_photo(b24_url : str, uuid : str):
    return File().add_user_photo(b24_url, uuid)

@file_router.delete("/delete_user_photo/{file_id}")
async def delete_user_photo(file_id: str):
    File().delete_user_img()