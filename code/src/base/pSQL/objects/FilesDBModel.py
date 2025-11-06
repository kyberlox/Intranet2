from ..models.FilesDB import FilesDB
from .App import select #get_db

import os

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Файлов")

# db_gen = get_db()
# database = next(db_gen)

STORAGE_PATH = "./files_db"

class FilesDBModel():
    def __init__(self, id=None, article_id=None, name=None, original_name = "", b24_url=None, active=True, is_preview = False, content_type = "", file_url = ""):
        self.id = id
        self.article_id = article_id

        self.name = name
        self.original_name = original_name
        self.b24_url = b24_url
        self.active = active
        self.is_preview = is_preview
        self.content_type = content_type
        self.file_url = file_url

        from ..models.FileModel import FileModel
        self.FileModel = FileModel
    
    async def add(self, session, file_data: dict = None):
        try:
            if self.article_id is None:
                return {'err': 'No article_id'}

            if self.name is None:
                return {'err': 'No name'}

            from .ArticleModel import ArticleModel
            article_model = ArticleModel(Id=self.article_id)
            existing_art = await article_model.find_by_id(session)
            
            if existing_art:
                new_artfile = self.FilesDB(
                    article_id=int(self.article_id), 
                    name=self.name, 
                    original_name=self.original_name, 
                    b24_url=self.b24_url, 
                    active=self.active, 
                    is_preview=self.is_preview, 
                    content_type=self.content_type, 
                    file_url=self.file_url
                )
                session.add(new_artfile)
                await session.commit()
                
                return new_artfile.id
            else:
                return {'err': 'Article not found'}
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в add при добавлении файла для статьи {self.article_id}: {e}")

    async def go_archive(self, session):
        try:
            stmt = select(self.FilesDB).where(self.FilesDB.id == self.id)
            result = await session.execute(stmt)
            file_record = result.scalar_one_or_none()
            
            if file_record:
                file_record.active = False
                await session.commit()
                return True
            else:
                return LogsMaker().warning_message(f"Файл с id = {self.id} не найден")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в go_archive при архивировании файла {self.id}: {e}")

    async def find_by_id(self, session):
        try:
            if self.id is not None:
                stmt = select(self.FilesDB).where(
                    self.FilesDB.id == self.id, 
                    self.FilesDB.active == True
                )
                result = await session.execute(stmt)
                file_db = result.scalar_one_or_none()
                
                if file_db:
                    return file_db.__dict__
                return None
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_by_id при поиске файла {self.id}: {e}")

    async def find_by_id_all(self, session):
        try:
            if self.id is not None:
                stmt = select(self.FilesDB).where(self.FilesDB.id == self.id)
                result = await session.execute(stmt)
                file_db = result.scalar_one_or_none()
                
                if file_db:
                    return file_db.__dict__
                return None
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_by_id_all при поиске файла {self.id}: {e}")

    async def remove(self, session):
        try:
            file_data = await self.find_by_id_all(session)
            if file_data is not None:
                # Удаляем физический файл
                unique_name = file_data['name']
                file_path = os.path.join(STORAGE_PATH, unique_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:  
                    LogsMaker().warning_message(f"Файл {file_path} не найден")
                
                # Удаляем запись из базы
                stmt = select(self.FilesDB).where(self.FilesDB.id == self.id)
                result = await session.execute(stmt)
                file_record = result.scalar_one_or_none()
                
                if file_record:
                    await session.delete(file_record)
                    await session.commit()
                    LogsMaker().ready_status_message(f"Файл {self.id} удален!")
                    return True
            else:
                return LogsMaker().warning_message(f"Файл {self.id} не найден")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в remove при удалении файла {self.id}: {e}")

    async def need_update(self, session):
        try:
            if self.article_id is not None and self.original_name is not None:
                stmt = select(self.FilesDB).where(
                    self.FilesDB.article_id == self.article_id,
                    self.FilesDB.original_name == self.original_name
                )
                result = await session.execute(stmt)
                file_db = result.scalar_one_or_none()
                
                if file_db:
                    res = file_db.__dict__
                    return False if self.original_name == res['original_name'] else True
                return None
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в need_update для статьи {self.article_id}: {e}")

    async def find_by_art_id(self, session):
        try:
            if self.article_id is not None:
                stmt = select(self.FilesDB).where(
                    self.FilesDB.article_id == self.article_id,
                    self.FilesDB.active == True
                )
                result = await session.execute(stmt)
                files_db = result.scalar_one_or_none()
                
                if files_db:
                    return files_db.__dict__
                return None
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_by_art_id при поиске файлов для статьи {self.article_id}: {e}")

    async def find_all_by_art_id(self, session):
        try:
            if self.article_id is not None:
                stmt = select(self.FilesDB).where(
                    self.FilesDB.article_id == self.article_id,
                    self.FilesDB.active == True
                )
                result = await session.execute(stmt)
                files_db = result.scalars().all()
                
                result_list = []
                for file_db in files_db:
                    res = file_db.__dict__
                    result_list.append(res)
                
                return result_list
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_all_by_art_id при поиске файлов для статьи {self.article_id}: {e}")

    async def generate_name(self, session, file_name: str):
        try:
            # name формируется по принципу {article_id}_{порядковый номер файла для статьи}.{формат файла}
            file_format = file_name.split(".")[-1]
            
            # Проверим есть к чему крепить файл
            if self.article_id is not None:
                stmt_exists = select(self.FilesDB).where(self.FilesDB.article_id == self.article_id)
                result_exists = await session.execute(stmt_exists)
                article_exists = result_exists.first()
                
                # Если нет - будет первым
                if not article_exists:
                    return f"{self.article_id}_1.{file_format}"
                
                # Если у статьи есть файлы - определим порядковый номер
                stmt_max = select(func.max(self.FilesDB.name)).where(
                    self.FilesDB.article_id == self.article_id
                )
                result_max = await session.execute(stmt_max)
                max_num = result_max.scalar_one_or_none()

                # Извлекаем номер из имени файла
                if max_num:
                    current_num = int(max_num.split('_')[-1].split('.')[0])
                    next_num = current_num + 1
                else:
                    next_num = 1

                return f"{self.article_id}_{next_num}.{file_format}"
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в generate_name при генерации имени файла для статьи {self.article_id}: {e}")