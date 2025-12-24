
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

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

import asyncio
import aiohttp
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


        # if id is not None:
        #     if type(id) == type(ObjectId("a"*24)):
        #         id = id
        #     elif type(id) == type(str()) and id != '':
        #         id = ObjectId(id)
        self.id = id
        self.art_id = art_id
        self.b24_id = b24_id

    async def download_by_URL(self, url, path, session):
        # if "https://portal.emk.ru" in url:
        #     response = requests.get(url)
        # else:
        #     response = requests.get(f"https://portal.emk.ru{url}")
        # with open(path, 'wb') as file:
        #     file.write(response.content)
        # return response.headers.get('Content-Type', 'unknown')
        if not url.startswith("https://portal.emk.ru"):
            url = f"https://portal.emk.ru{url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    # Используем aiofiles для асинхронной записи файла
                    async with aiofiles.open(path, 'wb') as f:
                        await f.write(await response.read())
                    return response.headers.get('Content-Type', 'unknown')
                else:
                    LogsMaker().error_message(f"Ошибка загрузки в upload_by_URL: статус {response.status}")
                    return None

    async def upload_inf_art(self, session, art_id=None, is_preview = False, need_all_method = True, inf_id=None):
        try:
            # b24 = B24()
            #print(f"ID фала = {self.b24_id} | ID инфоблока = {inf_id} | ID статьи = {art_id}")
            filename = ""
            if art_id is None:
                return LogsMaker().warning_message(f"Ошибка в функции upload_inf_art File: No article_id")

            try:
                if need_all_method is True:
                    file_data = await B24().get_all_files(self.b24_id)
                else:
                    file_data = await B24().get_file(self.b24_id, inf_id)
                # file_data = await asyncio.to_thread(b24.get_all_files, self.b24_id)
                # if hasattr(file_data, '_asyncio_future_blocking'):  
                #     file_data = await file_data 
                if "ORIGINAL_NAME" in file_data:
                    filename = file_data["ORIGINAL_NAME"]
                elif "FILE_NAME" in file_data:
                    filename = file_data["FILE_NAME"]
                elif "NAME" in file_data:
                    filename = file_data["NAME"]

                #ТУТ НУЖНО ПРОВЕРИТЬ НЕОБХОДИМОСТЬ ДОБАВЛЕНИЯ ФАЙЛА
                need_update_file = await FilesDBModel(article_id=art_id, original_name=filename).need_update(session=session)
                
                if need_update_file is False:
                    LogsMaker().info_message(f"Уже был такой файл с article_id = {art_id} и original_name = {filename}")
                    return None

                filename_parts = filename.split('.')
                file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''
                
                # Генерируем уникальное имя файла
                unique_name = await FilesDBModel(article_id=art_id).generate_name(file_name=filename, session=session)
                
                file_path = os.path.join(STORAGE_PATH, unique_name)
                
                # Сохраняем файл
                
                
                
                if "DOWNLOAD_URL" in file_data.keys():
                    content_type = await self.download_by_URL(url=file_data["DOWNLOAD_URL"], path=file_path, session=session)
                    url_b24 = file_data["DOWNLOAD_URL"] 
                elif "SRC" in file_data.keys():
                    url_b24 = 'https://portal.emk.ru' + file_data['SRC']
                    content_type = await self.download_by_URL(url=url_b24, path=file_path, session=session)

                # else:
                    

                #     if "ORIGINAL_NAME" in file_data:
                #         filename = file_data["ORIGINAL_NAME"]
                #     elif "FILE_NAME" in file_data:
                #         filename = file_data["FILE_NAME"]
                #     elif "NAME" in file_data:
                #         filename = file_data["NAME"]
                    
                #     #ТУТ НУЖНО ПРОВЕРИТЬ НЕОБХОДИМОСТЬ ДОБАВЛЕНИЯ ФАЙЛА
                #     need_update_file = await FilesDBModel(article_id=art_id, original_name=filename).need_update(session=session)
                    
                #     if need_update_file is False:
                #         LogsMaker().info_message(f"Уже был такой файл с article_id = {art_id} и original_name = {filename}")
                #         return None

                #     filename_parts = filename.split('.')

                #     file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

                #     # Генерируем уникальное имя файла
                #     unique_name = await FilesDBModel(article_id=art_id).generate_name(file_name=filename, session=session)
            
                #     file_path = os.path.join(STORAGE_PATH, unique_name)
                #     # # Сохраняем файл
                #     # url_b24 = file_data["SRC"]
                #     # Сохраняем файл
                #     content_type = await self.download_by_URL(url=file_data["DOWNLOAD_URL"], path=file_path, session=session)
                    
                #     url_b24 = file_data["DOWNLOAD_URL"]
                
                # result = {
                #     # "id": str(inserted_id),
                #     "original_name": filename,
                #     "name": unique_name,
                #     "content_type": content_type,
                #     "article_id": art_id,
                #     "b24_id": url_b24,
                #     "active": False,
                #     "is_preview" : is_preview,
                #     "file_url": f"/api/files/{unique_name}"
                # }
                # print(result)
                
                #записать в pSQL
                inserted_id = await FilesDBModel(
                    article_id=art_id,
                    name=unique_name,
                    original_name = filename,
                    b24_url=url_b24,
                    active=True,
                    is_preview = is_preview,
                    content_type = content_type,
                    file_url = f"/api/files/{unique_name}").add(session=session)


                # result = {
                #     "id": str(inserted_id),
                #     "original_name": filename,
                #     "name": unique_name,
                #     "content_type": content_type,
                #     "article_id": art_id,
                #     "b24_id": url_b24,
                #     "active": False,
                #     "is_preview" : is_preview,
                #     "file_url": f"/api/files/{unique_name}"
                # }
                # print(result)

                return {
                    "id": str(inserted_id),
                    "original_name": filename,

                    "name": unique_name,
                    "content_type": content_type,
                    "article_id": art_id,
                    "b24_id": url_b24,
                    "active": False,
                    "is_preview" : is_preview,
                    "file_url": f"/api/files/{unique_name}"
                }


            except Exception as e:
                LogsMaker().warning_message(f"Фатальная ошибка записи файла: {self.b24_id}, из статьи {art_id}, инфоблока {inf_id}, применение метода Матренина: {need_all_method}, ошибка: {e}")

            
        except requests.exceptions.RequestException as e:
            # print(f"Ошибка при скачивании файла: {e}")

            return LogsMaker().error_message(f"Ошибка при скачивании файла: {e}")

    async def add_link(self, link, art_id, session):
        unique_name = await FilesDBModel(article_id=art_id).generate_name(file_name=link, session=session)
            
        #записать
        inserted_id = await FilesDBModel(
            article_id=art_id,
            name=unique_name,
            original_name = link,
            b24_url=self.b24_id,
            active=True,
            is_preview = False,
            content_type = "link",
            file_url = link
        ).add(session=session)

        #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!!!!!
        return link
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    #НЕ ИСПОЛЬЗУЕМАЯ ФУНКЦИЯ
    async def need_update_url_file(self,  art_id, filename, session):
        # print('1)', files_id, 'файлы, которые нужно добавить', art_id)

        # result = FilesDBModel(art_id=art_id).find_all_by_art_id()
        # DB_files_name = []

        # if result is None: # если в бд нет такой статьи
        #     return True
        # else:
        #     # цикл для сбора данных с БД
        #     for res in result: # выдергиваем все original_name из монго по art_id 
        #         fl = res["original_name"]
        #         DB_files_name.append(fl)

        #     # цикл для проверки если в DB_files_id есть файлы, которых нет в files_id
        #     for fl in DB_files_name:
        #         #print(filename)
        #         #print(fl)
        #         if filename == 'uf.php?attachedId=128481&auth%5Baplogin%5D=1&auth%5Bap%5D=j6122m0ystded5ag&action=show&ncc=1':
        #             return False
        #         elif fl == filename:
        #             return False
        #     return True

        pass


    async def upload_by_URL(self, url, art_id, session, b24_id = None, is_preview = False):
        filename = url.split("/")[-1]
        
        filename_parts = filename.split('.')
        file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

        need_update_file = await FilesDBModel(article_id=art_id, original_name=filename).need_update(session=session)
        #тут надо проверить, нет ли такого файла уже в БД?
        # if await self.need_update_url_file(art_id=art_id, filename=filename, session=session):
        if need_update_file is True:
            # Генерируем уникальное имя файла
            unique_name = await FilesDBModel(article_id=art_id).generate_name(file_name=filename, session=session)
            file_path = os.path.join(STORAGE_PATH, unique_name)

            #скачать файл по ссылке
            async with aiohttp.ClientSession() as sess:
                async with sess.get(url) as response:
                    if response.status == 200:
                        # Используем aiofiles для асинхронной записи файла
                        async with aiofiles.open(file_path, 'wb') as f:
                            await f.write(await response.read())
                        content_type = response.headers.get('Content-Type', 'unknown')
                    else:
                        LogsMaker().error_message(f"Ошибка загрузки в upload_by_URL: статус {response.status}")
                        content_type = None
            
            # content_type = response.headers.get('Content-Type', 'unknown')

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
            inserted_id = await FilesDBModel(
                article_id=art_id,
                name=unique_name,
                original_name = filename,
                b24_url=self.b24_id,
                active=True,
                is_preview = is_preview,
                content_type = content_type,
                file_url = f"/api/files/{unique_name}"
            ).add(session=session)

            new_url = f"/api/files/{unique_name}"
            
            return f"{DOMAIN}{new_url}"
            
        else: #надо заменить
            self.art_id = art_id

            # files = self.get_files_by_art_id()
            files = await FilesDBModel(article_id=self.art_id).find_all_by_art_id(session=session)
            for fl in files:
                if fl["original_name"] == filename:
                    #перезаписываем
                    unique_name = fl["name"]
                    file_path = os.path.join(STORAGE_PATH, unique_name)
                    # response = requests.get(f"{DOMAIN}{url}")
                    # with open(file_path, 'wb') as file:
                    #     file.write(response.content)
                    async with aiohttp.ClientSession() as sess:
                        async with sess.get(url) as response:
                            if response.status == 200:
                                # Используем aiofiles для асинхронной записи файла
                                async with aiofiles.open(file_path, 'wb') as f:
                                    await f.write(await response.read())
                                new_url = fl["file_url"]
                    
                                return f"{DOMAIN}{new_url}"
                            else:
                                LogsMaker().error_message(f"Ошибка загрузки в upload_by_URL: статус {response.status}")
                                return None
                    
                    # new_url = fl["file_url"]
                    
                    # return f"{DOMAIN}{new_url}"

    #НЕ ИСПОЛЬЗУЕМАЯ ФУНКЦИЯ
    async def save_by_URL(self, url, art_id, session, b24_id = None, is_preview = False):
        """
        ЗАМЕНИЛИ ЭТУ ФУНКЦИЮ НА upload_by_URL
        """
        filename = url.split("/")[-1]
        
        filename_parts = filename.split('.')
        file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

        #тут надо проверить, нет ли такого файла уже в БД?

        if await self.need_update_url_file(art_id=art_id, filename=filename, session=session):
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
            inserted_id = await FilesDBModel(
                article_id=art_id,
                name=unique_name,
                original_name = filename,
                b24_url=self.b24_id,
                active=True,
                is_preview = is_preview,
                content_type = content_type,
                file_url = f"/api/files/{unique_name}"
            ).add(file_data=data, session=session)

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

    #НЕ ИСПОЛЬЗУЕМАЯ ФУНКЦИЯ
    async def save_by_URL(self, url, art_id, b24_id = None, is_preview = False):
        pass
    
    async def need_update_file(self,  art_id, files_id, session):
        """
        Принимает список айдишников файлов статьи
        Смотрит какие надо обновить
        Возвращает список айдишников файлов которые надо обновить/добавить
        """
        result = []
        for file_id in files_id:
            res = await FilesDBModel(id=int(file_id)).find_by_id_all(session=session)
            if not res:
                result.append(int(file_id))
            else:
                need_update_file = await FilesDBModel(article_id=art_id, original_name=res[original_name]).need_update(session=session)
                if need_update_file is True:
                    result.append(int(file_id))
        return result
        # # print('1)', files_id, 'файлы, которые нужно добавить', art_id)
        # result = FilesDBModel(art_id=art_id).find_all_by_art_id()
        # DB_files_id = []
        # DB_files_path = {}

        # if result is None: # если в бд нет такого файла
        #     return files_id 
        # else:
        #     # цикл для сбора данных с БД
        #     for res in result: # выдергиваем все b24_id из монго по art_id 
        #         fl = res["b24_id"]
        #         DB_files_id.append(fl)
        #         DB_files_path[fl] = f'{STORAGE_PATH}/{res["stored_name"]}'

        #     # цикл для проверки если в DB_files_id есть файлы, которых нет в files_id
        #     for fl in DB_files_id:
        #         if fl not in files_id:
        #             FileModel(b24_id = fl).go_archive() #если лишний b24_id -> удалить запись в mongo и сам файл -> #не нужно добавлять
        #             #os.remove(DB_files_path[fl])
        #             # print('лишний файл в БД', file, art_id)
        #         else:
        #             files_id.remove(fl) # удаляем из входящего списка все файлы которые уже есть в DB_files_id

        #     # print('2)', files_id, 'файлы, которые нужно добавить', art_id)

            # return files_id # вернет пустой список если все файлы уже есть в БД, в обратном случае вернет только те файлы, которых в БД нет
    
    #НЕ ИСПОЛЬЗУЕМАЯ ФУНКЦИЯ
    async def get_file(self, session):
        file_data = await FilesDBModel(id=self.id).find_file_by_id(session=session)
        
        if file_data is not None:
            return file_data
        else:
            raise HTTPException(status_code=404, detail="File not found")

    async def get_files_by_art_id(self, session):
        file_data = await FilesDBModel(article_id=int(self.art_id)).find_all_by_art_id(session=session)
        file_list = []
        
        if not file_data:
            # raise HTTPException(status_code=404, detail="Files not found")
            return None
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
                    file_info["b24_url"] = fl["b24_url"]
                    file_info["file_url"] = fl["file_url"]
                    file_info["active"] = fl["active"]
                    file_info["is_preview"] = fl["is_preview"]

                    file_list.append(file_info)

            return file_list

    async def delete_by_art_id(self, session):
        try:
            files_data = await FilesDBModel(article_id=self.art_id).find_all_by_art_id(session=session)
            if files_data is not None and files_data != []:
                for file_data in files_data:
                    #удалить по id файла
                    self.id = file_data['id']
                    await FilesDBModel(id = self.id).remove(session=session)
            return True
        except Exception as e:
            return LogsMaker().error_message(f'Ошибка при удалении файлов статьи с id = {self.art_id} delete_by_art_id File: {e}')

    async def change_prev(self, session):
        return await FilesDBModel(id=self.id, article_id=self.art_id).change_prev(session)

    #НЕ ИСПОЛЬЗУЕМАЯ ФУНКЦИЯ
    async def get_files_by_section_id(self, section_id, session):
        #беру список atr_id
        res = await Section(id = section_id).find_by_id(session)
        arts_id = res['arts_id']

        files = dict()
        if arts_id != []:
            for art_id in arts_id:
                self.art_id = art_id

                art_files = await FilesDBModel(article_id=self.art_id).find_all_by_art_id(session=session)

                files[art_id] = art_files
        
        return files



    async def get_users_photo(self, session):
        #переделать с учетом is_archive
        file_data = await UserFilesModel(id=self.id).find_user_photo_by_id(session)
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


    
    async def dowload_user_photo(self, url, name):
        # в будущем name исправить на айди фото ( photo_file_id )
        img_path = f"{USER_STORAGE_PATH}/{name}"
        
        try:
            print(url, img_path)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # Используем aiofiles для асинхронной записи файла
                        async with aiofiles.open(img_path, 'wb') as f:
                            await f.write(await response.read())
                        return True
                    else:
                        LogsMaker().error_message(f"Ошибка загрузки: статус {response.status}")
                        return False
        except Exception as e:
            LogsMaker().error_message(f"Ошибка в dowload_user_photo: {e}")
            return False

    async def add_user_img(self, b24_url : str, uuid : str, session):
        #скачать файл
        try:
            #собрать данные
            name = b24_url.split("/")[-1]
            #создать запись
            w_photo = await UserFilesModel(
                user_id=int(uuid),
                name=name,
                b24_url=b24_url,
                active=True
            ).add_user_photo(session=session) #вернет False, если пытаться скачать актуальную фотку ещё раз

            if w_photo is not False: 
                #скачать файл
                result = await self.dowload_user_photo(url=b24_url, name=w_photo['name'])
                return w_photo
            return False
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в функции add_user_img : {e} ")
    
    async def delete_user_img(self, session):
        """
        Ищет файл
        Удаляет файл из папки user_photo и в БД таблицы User меняет значение
        колонки photo_file_id на None
        """
        file_data = await UserFilesModel(id = self.id).find_user_photo_by_id(session=session)
        if not file_data:
            raise HTTPException(404, detail="File not found")
        
        try:

            await UserFilesModel(id = self.id).remove_user_photo(file_data=file_data, session=session)
            return {"status": "to_archive"}
        except Exception as e:
            # raise HTTPException(500, detail=str(e))
            return LogsMaker().error_message(f"Ошибка в функции delete_user_img : {e} ")
    


    # Блок создания индексов

    async def index_files(self):
        pass
        #return FileModel().create_index_files()

    async def index_user_photo(self):
        pass
        #return FileModel().create_index_user_photo()

    async def editor_add_file(self, file : webFile, session):
        #!!!!!!!внедрить проверки
        
        # Генерируем уникальное имя файла
        # filename = file.filename
        # filename_parts = filename.split('.')
        # file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''
        # unique_name = str(ObjectId()) + file_ext
        unique_name = await FilesDBModel(article_id=self.art_id).generate_name(file_name=file.filename, session=session)
        print(unique_name, 'СМОТРИМ ПОЛУЧАЕМ ЛИ УНИК ИМЯ')
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
            inserted_id = await FilesDBModel(
                article_id=int(self.art_id),
                name=unique_name,
                original_name = file.filename,
                b24_url=None,
                active=True,
                is_preview = False,
                content_type = str(file.content_type),
                file_url = f"/api/files/{unique_name}"
            ).add(session)

            file_info = await FilesDBModel(id = inserted_id).find_file_by_id(session)
            return file_info
        
        except Exception as e:
            # В случае ошибки
            UPLOAD_PROGRESS[upload_id] = -1  # -1 означает ошибку
            await asyncio.sleep(1)
            if upload_id in UPLOAD_PROGRESS:
                del UPLOAD_PROGRESS[upload_id]
            raise e
    

    async def editor_del_file(self, session):
        file_data = await FilesDBModel(id = self.id).find_file_by_id(session)
        if not file_data:
            raise HTTPException(404, detail="File not found")
        
        try:

            await FilesDBModel(id = self.id).remove(session)
            return {"status": "deleted"}
        except Exception as e:
            # raise HTTPException(500, detail=str(e))
            return LogsMaker().error_message(e)


    async def editor_chenge_file(self, file : webFile):
        #найти файл
        #заменить id и отправить предыдущую версию в архив
        #скачать под старым id
        #заменить метданные
        pass
    

    async def set_is_preview(self ):
        #найти статью файла
        #проверить есть ли в ней первью
        #заменить, если есть
        #найти файл сделать его превью
        pass



@file_router.post("/upload/{art_id}")
async def upload_file(file: UploadFile, art_id : int, session: AsyncSession=Depends(get_async_db)):
    try:
        # Получаем расширение файла
        filename_parts = file.filename.split('.')
        file_ext = '.' + filename_parts[-1] if len(filename_parts) > 1 else ''

        # Генерируем уникальное имя файла

        unique_name = await FilesDBModel(article_id=art_id).generate_name(file_name=file.filename, session=session)
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
        inserted_id = await FilesDBModel(
            article_id=int(art_id),
            name=unique_name,
            original_name = file.filename,
            b24_url=None,
            active=True,
            is_preview = False,
            content_type = str(file.content_type),
            file_url = f"/api/files/{unique_name}"
        ).add(session=session)

        file_info = await FilesDBModel(id = inserted_id).find_file_by_id(session=session)
        return file_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@file_router.get("/info/{file_id}")
async def get_file_info(file_id: str, session: AsyncSession=Depends(get_async_db)):
    try:

        file_data = await FilesDBModel(id = file_id).find_file_by_id(session=session)

        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        return file_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@file_router.get("/info/article_id/{article_id}")
async def get_file_article(article_id: int, session: AsyncSession=Depends(get_async_db)):
    try:
        file_data = await File(art_id=article_id).get_files_by_art_id(session=session)

        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        return file_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@file_router.get("/info/section_id/{section_id}")
async def get_file_article(section_id: int, session: AsyncSession=Depends(get_async_db)):
    try:
        file_data = await File().get_files_by_section_id(section_id = section_id, session=session)

        if not file_data:
            raise HTTPException(status_code=404, detail="Files not found")

        return file_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@file_router.delete("/{file_id}")
async def delete_file(file_id: str, session: AsyncSession=Depends(get_async_db)):
    #изменить статус
    file_data = await FilesDBModel(id = file_id).find_file_by_id(session=session)
    if not file_data:
        raise HTTPException(404, detail="File not found")
    
    try:
        await FilesDBModel(id = file_id).remove(session=session)
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
async def put_file(file_id : int, data = Body(), session: AsyncSession=Depends(get_async_db)):
    new_file_data = await FilesDBModel(id = file_id).update_data(data=data, session=session)
    return new_file_data



@file_router.post("/get_user_photo/{uuid}")
async def get_user_photo(uuid : str, session: AsyncSession=Depends(get_async_db)):
    return await UserFilesModel().find_user_photo_by_uuid(uuid=uuid, session=session)

@file_router.get("/get_user_photo/{file_id}")
async def get_user_photo(file_id: int, session: AsyncSession=Depends(get_async_db)):
    return await UserFilesModel(id = file_id).find_user_photo_by_id(session=session)

@file_router.post("/add_user_photo/{b24_url}/{uuid}")
async def add_user_photo(b24_url : str, uuid : str, session: AsyncSession=Depends(get_async_db)):
    return await File().add_user_img(b24_url=b24_url, uuid=uuid, session=session)

@file_router.delete("/delete_user_photo/{file_id}")
async def delete_user_photo(file_id: int, session: AsyncSession=Depends(get_async_db)):
    return await File(id=file_id).delete_user_img(session=session)


@file_router.post("/change_prev/{art_id}/{file_id}")
async def change_prev(file_id : int, art_id : int, session: AsyncSession=Depends(get_async_db)):
    return await File(id=file_id, art_id=art_id).change_prev(session=session)



@file_router.post("/upload_link")
async def create_link(data=Body(), session: AsyncSession = Depends(get_async_db)):
    if "art_id" in data:
        art_id = data["art_id"]
    else:
        return LogsMaker().warning_message(f"Укажите номер статьи")

    # тяну все линки статьи
    current_links = []

    #тяну все, какие должны быть линки 
    if "links" in data:
        links = data["links"]
    else:
        return LogsMaker().warning_message(f"Укажите ссылку")

    #сравниваю
    #если не было - добавить
    #если стало меньше - убрать лишнее

    f_res = []
    for link in links:
        res = await File(b24_id=None).add_link(link=link, art_id=art_id, session=session)
        f_res.append(res)

    return f_res