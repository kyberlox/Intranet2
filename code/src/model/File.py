#from ..base.mongodb import FileModel
from ..base.pSQL.objects.UserFilesModel import UserFilesModel
from ..base.pSQL.objects.FilesDBModel import FilesDBModel

from ..base.B24 import B24
from .Section import Section

from fastapi import FastAPI, UploadFile
from fastapi import File as webFile

from bson.objectid import ObjectId
import requests

from fastapi import APIRouter, Body, UploadFile, HTTPException

import os
from dotenv import load_dotenv

import asyncio
import aiofiles

from src.services.LogsMaker import LogsMaker

from typing import Dict

load_dotenv()

DOMAIN = os.getenv('HOST')

STORAGE_PATH = "./files_db"
USER_STORAGE_PATH = "./files_db/user_photo"



file_router = APIRouter(prefix="/file", tags=["Файлы"])

# Хранилище для отслеживания прогресса
UPLOAD_PROGRESS: Dict[int, float] = {}

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
            filename = ""
            if art_id is None:
                return {'err' : "Con not add file without art_id"}
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
                    unique_name = FilesDBModel(article_id=art_id).generate_name(filename)
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
                    unique_name = FilesDBModel(article_id=art_id).generate_name(filename)
                    file_path = os.path.join(STORAGE_PATH, unique_name)

                    # Сохраняем файл
                    content_type = self.download_by_URL(file_data["DOWNLOAD_URL"], file_path)
                
                # result = {
                #     "original_name": filename,
                #     "name": unique_name,
                #     "content_type": content_type,
                #     "article_id": art_id,
                #     "b24_id": self.b24_id,
                #     "is_archive": False,
                #     "is_preview": is_preview,
                #     "file_url": f"/api/files/{unique_name}"  # Прямой URL
                # }

                #ТУТ НУЖНО ПРОВЕРИТЬ НЕОБХОДИМОСТЬ ДОБАВЛЕНИЯ ФАЙЛА

                #записать в pSQL
                inserted_id = FilesDBModel(
                    article_id=art_id,
                    name=unique_name,
                    original_name = filename,
                    b24_url=self.b24_id,
                    active=True,
                    is_preview = is_preview,
                    content_type = content_type,
                    file_url = f"/api/files/{unique_name}").add()

                return {
                    "id": str(inserted_id),
                    "original_name": filename,
                    "name": unique_name,
                    "content_type": content_type,
                    "article_id": art_id,
                    "b24_id": self.b24_id,
                    "active": False,
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
        # data = {
        #     "original_name": link,
        #     "stored_name": filename,
        #     "content_type": "link",
        #     "article_id": art_id,
        #     "b24_id": self.b24_id,
        #     "is_archive": False,
        #     "is_preview": False,
        #     "file_url": link  # Прямой URL
        # }
            
        #записать в mongodb
        inserted_id = FilesDBModel(
            article_id=art_id,
            name=filename,
            original_name = link,
            b24_url=self.b24_id,
            active=True,
            is_preview = is_preview,
            content_type = "link",
            file_url = link
        ).add(data)

        #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!!!!!
        return link
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def need_update_url_file(self,  art_id, filename):
        # print('1)', files_id, 'файлы, которые нужно добавить', art_id)
        result = FilesDBModel(art_id=art_id).find_all_by_art_id()
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
            unique_name = FilesDBModel(article_id=art_id).generate_name(filename)
            file_path = os.path.join(STORAGE_PATH, unique_name)

            #скачать файл по ссылке
            response = requests.get(f"https://portal.emk.ru{url}")
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            content_type = response.headers.get('Content-Type', 'unknown')

            # result = {
            #             "original_name": filename,
            #             "stored_name": unique_name,
            #             "content_type": content_type,
            #             "article_id": art_id,
            #             "b24_id": self.b24_id,
            #             "is_archive": False,
            #             "is_preview": is_preview,
            #             "file_url": f"/api/files/{unique_name}"  # Прямой URL
            #         }
            
            #записать в psql
            inserted_id = FilesDBModel(
                article_id=art_id,
                name=unique_name,
                original_name = filename,
                b24_url=self.b24_id,
                active=True,
                is_preview = is_preview,
                content_type = content_type,
                file_url = f"/api/files/{unique_name}"
            ).add(data)

            new_url = f"/api/files/{unique_name}"
            
            return f"{DOMAIN}{new_url}"
            
        else: #надо заменить
            self.art_id = art_id
            files = self.get_files_by_art_id()
            for fl in files:
                if fl["original_name"] == filename:
                    #перезаписываем
                    unique_name = fl["name"]
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
            #print(url)
            response = requests.get(url)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            content_type = response.headers.get('Content-Type', 'unknown')

            # result = {
            #             "original_name": filename,
            #             "stored_name": unique_name,
            #             "content_type": content_type,
            #             "article_id": art_id,
            #             "b24_id": self.b24_id,
            #             "is_archive": False,
            #             "is_preview": is_preview,
            #             "file_url": f"/api/files/{unique_name}"  # Прямой URL
            #         }
            
            #записать в psql
            inserted_id = FilesDBModel(
                article_id=art_id,
                name=unique_name,
                original_name = filename,
                b24_url=self.b24_id,
                active=True,
                is_preview = is_preview,
                content_type = content_type,
                file_url = f"/api/files/{unique_name}"
            ).add(data)

            new_url = f"/api/files/{unique_name}"
            
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

    # def need_update_file(self,  art_id, files_id):
    #     # print('1)', files_id, 'файлы, которые нужно добавить', art_id)
    #     result = FilesDBModel(art_id=art_id).find_all_by_art_id()
    #     DB_files_id = []
    #     DB_files_path = {}

    #     if result is None: # если в бд нет такого файла
    #         return files_id 
    #     else:
    #         # цикл для сбора данных с БД
    #         for res in result: # выдергиваем все b24_id из монго по art_id 
    #             fl = res["b24_id"]
    #             DB_files_id.append(fl)
    #             DB_files_path[fl] = f'{STORAGE_PATH}/{res["stored_name"]}'

    #         # цикл для проверки если в DB_files_id есть файлы, которых нет в files_id
    #         for fl in DB_files_id:
    #             if fl not in files_id:
    #                 FileModel(b24_id = fl).go_archive() #если лишний b24_id -> удалить запись в mongo и сам файл -> #не нужно добавлять
    #                 #os.remove(DB_files_path[fl])
    #                 # print('лишний файл в БД', file, art_id)
    #             else:
    #                 files_id.remove(fl) # удаляем из входящего списка все файлы которые уже есть в DB_files_id

    #         # print('2)', files_id, 'файлы, которые нужно добавить', art_id)

    #         return files_id # вернет пустой список если все файлы уже есть в БД, в обратном случае вернет только те файлы, которых в БД нет
    

    def get_file(self):
        file_data = FilesDBModel(id=self.id).find_by_id()
        
        if file_data is not None:
            return file_data
        else:
            raise HTTPException(status_code=404, detail="File not found")
        
            

    def get_files_by_art_id(self):
        file_data = FilesDBModel(art_id=int(self.art_id)).find_all_by_art_id()
        file_list = []
        
        if not file_data:
            raise HTTPException(status_code=404, detail="Files not found")
        else:
            for fl in file_data:
                if fl["active"]:
                    file_info = {}
                    file_info["id"] = str(fl["id"])
                    file_info["original_name"] = fl["original_name"]
                    file_info["name"] = fl["name"]
                    file_info["content_type"] = fl["content_type"]

                    #файлы делятся по категориям
                    if "image" in fl["content_type"]:
                        file_info["type"] = "image"
                    elif "video" in fl["content_type"]:
                        file_info["type"] = "video"
                    elif "link" in fl["content_type"]:
                        file_info["type"] = "video_embed"
                    else:
                        file_info["type"] = "documentation"

                    file_info["article_id"] = fl["article_id"]
                    file_info["b24_id"] = fl["b24_id"]
                    file_info["file_url"] = fl["file_url"]
                    file_info["active"] = fl["active"]
                    file_info["is_preview"] = fl["is_preview"]

                    file_list.append(file_info)

            

            return file_list

    def delete_by_art_id(self):
        files_data = self.get_files_by_art_id()
        if files_data is not None and files_data != []:
            for file_data in files_data:
                #удалить по id файла
                self.id = file_data['id']
                FilesDBModel(id = self.id).remove()

    def get_files_by_section_id(self, section_id):
        #беру список atr_id
        arts_id = Section(id = section_id).find_by_id()['arts_id']

        files = dict()
        if arts_id != []:
            for art_id in arts_id:
                self.art_id = art_id
                art_files = self.get_files_by_art_id()

                files[art_id] = art_files
        
        return files

    # def need_update_link(self):
    #     pass

    # def get_link_as_file(self):
    #     pass

    # def update_data(self, data : dict):
    #     #получить данные
    #     file_data = FilesDBModel(id=self.id).find_by_id()
    #     #file_data["id"] = str(file_data["_id"])
    #     file_data.pop("_id")
        
    #     #заменить данные
    #     for key in data.keys():
    #         if key != "id":
    #             file_data[key] = data[key]

    #     #сохранить изменения
    #     result = FilesDBModel(id=self.id).update_data(file_data)
        
    #     return result


    def get_users_photo(self):
        #переделать с учетом is_archive
        file_data = UserFilesModel(id=self.id).find_user_photo_by_id()
        
        if not file_data or not file_data["active"]:
            raise HTTPException(status_code=404, detail="File not found")
        else:
            file_info = dict()
            file_info["id"] = file_data["id"]
            file_info["name"] = file_data["name"]
            file_info["uuid"] = file_data["user_id"]
            file_info["URL"] = file_data["URL"]
            file_info["b24_url"] = file_data["b24_url"]
            file_info["active"] = file_data["active"]

            return file_info

    def dowload_user_photo(self, url, name):
        # в будущем name исправить на айди фото ( photo_file_id )
        img_path = f"{USER_STORAGE_PATH}/{name}"

        with requests.get(url, stream=True) as r:
            with open(img_path, "wb") as f:
                f.write(r.content)
        
        return True

    def add_user_img(self, b24_url : str, uuid : str):
        #скачать файл
        try:
            #собрать данные
            name = url.split("/")[-1]
            #создать запись
            w_photo = UserFilesModel().add_user_photo(
                user_id=None,
                name=name,
                b24_url=b24_url,
                active=True
            ) #вернет False, если пытаться скачать актуальную фотку ещё раз

            print(w_photo, type(w_photo))

            if w_photo is not False:
                #скачать файл
                print(b24_url, w_photo['name'])
                result = self.dowload_user_photo(url=b24_url, name=w_photo['name'])
            
            return w_photo
        except Exception as e:
                    return LogsMaker().error_message(e)
    
    def delete_user_img(self):
        file_data = UserFilesModel(id = self.id).find_user_photo_by_id()
        if not file_data:
            raise HTTPException(404, detail="File not found")
        
        try:
            UserFilesModel(id = self.id).remove_user_photo()
            return {"status": "to_archive"}
        except Exception as e:
            # raise HTTPException(500, detail=str(e))
            return LogsMaker().error_message(e)
    


    # Блок создания индексов
    def index_files(self):
        pass
        #return FileModel().create_index_files()

    def index_user_photo(self):
        pass
        #return FileModel().create_index_user_photo()



    async def editor_add_file(self, file : webFile):
        #!!!!!!!внедрить проверки
        
        # Генерируем уникальное имя файла
        # filename = file.filename
        # filename_parts = filename.split('.')
        # file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''
        # unique_name = str(ObjectId()) + file_ext
        unique_name = FilesDBModel(article_id=self.art_id).generate_name(file.filename)
        file_path = os.path.join(STORAGE_PATH, unique_name)

        # Инициализируем upload_id и прогресс
        upload_id = int(self.art_id)
        UPLOAD_PROGRESS[upload_id] = 0

        try:
            # Получаем размер файла для расчета прогресса
            file.file.seek(0, 2)  # Перемещаемся в конец файла
            file_size = file.file.tell()  # Получаем размер
            file.file.seek(0)  # Возвращаемся в начало
            
            # Читаем и сохраняем файл с отслеживанием прогресса
            total_written = 0
            chunk_size = 1024 * 1024  # 1MB chunks
            
            # Обычная загрузка файла
            # with file.file:
            #     contents = file.file.read()
            #     async with aiofiles.open(file_path, "wb") as f:
            #         await f.write(contents)

            # Асинхронная загрузка с мониторингом прогресса
            async with aiofiles.open(file_path, "wb") as f:
                while True:
                    # Читаем чанк данных
                    chunk = file.file.read(chunk_size)
                    if not chunk:
                        break
                    
                    # Записываем чанк в файл
                    await f.write(chunk)
                    total_written += len(chunk)
                    
                    # Обновляем прогресс
                    if file_size > 0:
                        progress = (total_written / file_size) * 100
                        UPLOAD_PROGRESS[upload_id] = progress
                        print(f"Upload progress for {upload_id}: {progress:.1f}%")  # Для отладки

            # Загрузка завершена успешно
            UPLOAD_PROGRESS[upload_id] = 100

            # Даем время WebSocket отправить финальный прогресс
            await asyncio.sleep(0.5)

            # Удаляем прогресс из хранилища после успешной загрузки
            if upload_id in UPLOAD_PROGRESS:
                del UPLOAD_PROGRESS[upload_id]

            # file_info = {
            #     "original_name": filename,
            #     "stored_name": unique_name,
            #     "content_type": str(file.content_type),
            #     "article_id": int(self.art_id),
            #     "b24_id": None,
            #     "is_archive": False,
            #     "is_preview" : False,
            #     "file_url": f"/api/files/{unique_name}"
            # }

            #записать в pSQL
            inserted_id = FilesDBModel(
                article_id=int(self.art_id),
                name=unique_name,
                original_name = file.filename,
                b24_url=None,
                active=True,
                is_preview = False,
                content_type = str(file.content_type),
                file_url = f"/api/files/{unique_name}"
            ).add()

            file_info = FilesDBModel(id = inserted_id).find_by_id()
            return file_info
        
        except Exception as e:
            # В случае ошибки
            UPLOAD_PROGRESS[upload_id] = -1  # -1 означает ошибку
            await asyncio.sleep(1)
            if upload_id in UPLOAD_PROGRESS:
                del UPLOAD_PROGRESS[upload_id]
            raise e
    
    def editor_del_file(self ):
        file_data = FilesDBModel(id = self.id).find_by_id()
        if not file_data:
            raise HTTPException(404, detail="File not found")
        
        try:
            FilesDBModel(id = self.id).remove()
            return {"status": "deleted"}
        except Exception as e:
            # raise HTTPException(500, detail=str(e))
            return LogsMaker().error_message(e)

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

@file_router.post("/upload/{art_id}")
async def upload_file(file: UploadFile, art_id : int):
    try:
        # Получаем расширение файла
        filename_parts = file.filename.split('.')
        file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

        # Генерируем уникальное имя файла
        unique_name = FilesDBModel(article_id=art_id).generate_name(file.filename)
        file_path = os.path.join(STORAGE_PATH, unique_name)

        # Сохраняем файл на диск
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Сохраняем метаданные
        # file_data = {
        #     "original_name": file.filename,
        #     "name": unique_name,
        #     "content_type": file.content_type,
        #     "file_url": f"/api/files/{unique_name}"  # Прямой URL
        # }

        # inserted_id = FilesDBModel().add(file_data)

        # return {
        #     "id": str(inserted_id),
        #     "file_url": file_data["file_url"],
        #     "original_name": file.filename
        # }
        #записать в pSQL
        inserted_id = FilesDBModel(
            article_id=int(art_id),
            name=unique_name,
            original_name = file.filename,
            b24_url=None,
            active=True,
            is_preview = False,
            content_type = str(file.content_type),
            file_url = f"/api/files/{unique_name}"
        ).add()

        file_info = FilesDBModel(id = inserted_id).find_by_id()
        return file_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@file_router.get("/info/{file_id}")
async def get_file_info(file_id: str):
    try:

        file_data = FilesDBModel(id = file_id).find_by_id()

        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        return file_data
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

@file_router.get("/info/section_id/{section_id}")
async def get_file_article(section_id: int):
    try:
        file_data = File().get_files_by_section_id(section_id = section_id)

        if not file_data:
            raise HTTPException(status_code=404, detail="Files not found")

        return file_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @file_router.get("/info/b24_id/{b24_id}")
# async def get_file_by_b24(b24_id: str):
#     try:
#         file_data = FilesDBModel(id = b24_id).find_by_b24_id()

#         if not file_data:
#             raise HTTPException(status_code=404, detail="File not found")

#         return {
#             "id": file_data["id"],
#             "url": file_data["file_url"],
#             "original_name": file_data["original_name"],
#             "content_type": file_data["content_type"]
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@file_router.delete("/{file_id}")
async def delete_file(file_id: str):
    #изменить статус
    file_data = FilesDBModel(id = file_id).find_by_id()
    if not file_data:
        raise HTTPException(404, detail="File not found")
    
    try:
        FilesDBModel(id = file_id).remove()
        return {"status": "deleted"}
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

@file_router.put("/{file_id}")
async def put_file(file_id : str, data = Body()):
    new_file_data = FilesDBModel(id = file_id).update_data(data)

    return new_file_data




@file_router.post("/get_user_photo/{uuid}")
async def get_user_photo(uuid : str):
    return FilesDBModel().find_user_photo_by_uuid(uuid)

@file_router.get("/get_user_photo/{file_id}")
async def get_user_photo(file_id: str):
    return FilesDBModel(id = file_id).find_user_photo_by_id(uuid)

@file_router.post("/add_user_photo/{b24_url}/{uuid}")
async def add_user_photo(b24_url : str, uuid : str):
    return File().add_user_photo(b24_url, uuid)

@file_router.delete("/delete_user_photo/{file_id}")
async def delete_user_photo(file_id: str):
    File().delete_user_img()