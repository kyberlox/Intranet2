from ..models.FilesDB import FilesDB
from .App import select, func, delete, update #get_db

import os

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Файлов")


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

        # from ..models.FileModel import FileModel
        # self.FileModel = FileModel
    
    async def add(self, session, file_data: dict = None):
        try:
            if self.article_id is None:
                LogsMaker().warning_message(f"Ошибка в функции add FilesDBModel: No article_id")
                return False

            if self.name is None:
                LogsMaker().warning_message(f"Ошибка в функции add FilesDBModel: No name")
                return False

            from .ArticleModel import ArticleModel
            article_model = ArticleModel(id=int(self.article_id))
            existing_art = await article_model.find_by_id(session=session)

            if not existing_art:
                LogsMaker().warning_message(f"В функции add FilesDBModel: Article not found, создаем шаблон в БД")
                from ..models.Article import Article
                new_art = Article(id=int(self.article_id))
                session.add(new_art)
            # if existing_art:
            new_artfile = FilesDB(
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
            
            await session.flush()
            file_id = new_artfile.id

            await session.commit()
            return file_id
            # else:
            #     from ..models.Article import Article
            #     new_art = Article(id=int(self.article_id))
            #     LogsMaker().warning_message(f"В функции add FilesDBModel: Article not found")
            #     return False
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в add при добавлении файла для статьи {self.article_id}: {e}")

    async def go_archive(self, session):
        try:
            stmt = select(FilesDB).where(FilesDB.id == self.id)
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

    async def find_file_by_id(self, session):
        """
        Ищет только активный файл статьи
        """
        try:
            if self.id is not None:
                stmt = select(FilesDB).where(
                    FilesDB.id == int(self.id), 
                    FilesDB.active == True
                )
                result = await session.execute(stmt)
                file_db = result.scalar_one_or_none()
                
                if file_db:
                    return file_db.__dict__
                return None
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_by_id FilesDBModel при поиске файла {self.id}: {e}")

    async def find_by_id_all(self, session):
        """
        Ищет файл статьи, включая не активные
        """
        try:
            if self.id is not None:
                stmt = select(FilesDB).where(FilesDB.id == int(self.id))
                result = await session.execute(stmt)
                file_db = result.scalar_one_or_none()
                
                if file_db:
                    return file_db.__dict__
                return None
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_by_id_all FilesDBModel при поиске файла {self.id}: {e}")

    async def remove(self, session):
        """
        Удаляет файл из папки files и удаляет запись о файле из БД
        """
        try:
            file_data = await self.find_by_id_all(session)
            if file_data is not None:
                # Удаляем физический файл
                unique_name = file_data['name']
                file_path = os.path.join(STORAGE_PATH, unique_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:  
                    LogsMaker().warning_message(f"Ошибка в find_by_id FilesDBModel: Файл {file_path} не найден")
                
                # Удаляем запись из базы
                stmt = select(FilesDB).where(FilesDB.id == int(self.id))
                result = await session.execute(stmt)
                file_record = result.scalar_one_or_none()
                
                if file_record:
                    await session.delete(file_record)
                    await session.commit()
                    LogsMaker().ready_status_message(f"Ошибка в find_by_id FilesDBModel: Файл {self.id} удален!")
                    return True
                else:
                    LogsMaker().warning_message(f"Ошибка в find_by_id FilesDBModel: Файл {self.id} удален из папки files, но не найден в БД")
                    return True
            else:
                return LogsMaker().warning_message(f"Файл {self.id} не найден")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в remove FilesDBModel при удалении файла {self.id}: {e}")

    async def need_update(self, session):
        try:
            if self.article_id is not None and self.original_name is not None:
                stmt = select(FilesDB).where(
                    FilesDB.article_id == int(self.article_id),
                    FilesDB.original_name == self.original_name
                )
                result = await session.execute(stmt)
                file_db = result.scalar_one_or_none()
                
                if file_db:
                    res = file_db.__dict__
                    return False if self.original_name == res['original_name'] else True
                return True
            else:
                return True
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в need_update FilesDBModel для статьи {self.article_id}: {e}")

    async def find_by_art_id(self, session):
        """
        По айди статьи находит первую фотку
        """
        try:
            if self.article_id is not None:
                stmt = select(FilesDB).where(
                    FilesDB.article_id == int(self.article_id),
                    FilesDB.active == True
                )
                result = await session.execute(stmt)
                files_db = result.scalar_one_or_none()
                
                if files_db:
                    return files_db.__dict__
                return None
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_by_art_id FilesDBModel при поиске файлов для статьи {self.article_id}: {e}")

    async def find_all_by_art_id(self, session):
        """
        По айди статьи находит все фотки
        возвращает список словарей
        """
        try:
            if self.article_id is not None:
                stmt = select(FilesDB).where(
                    FilesDB.article_id == self.article_id,
                    FilesDB.active == True
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
            return LogsMaker().error_message(f"Ошибка в find_all_by_art_id FilesDBModel при поиске файлов для статьи {self.article_id}: {e}")

    async def generate_name(self, session, file_name: str):
        try:
            # name формируется по принципу {article_id}_{порядковый номер файла для статьи}.{формат файла}
            if file_name.startswith(('http://', 'https://')):
                file_format = 'link'
            else:
                file_format = file_name.split(".")[-1]
            
            # Проверим есть к чему крепить файл
            if self.article_id is not None:
                # stmt_exists = select(FilesDB).where(FilesDB.article_id == self.article_id)
                # result_exists = await session.execute(stmt_exists)
                # article_exists = result_exists.scalar_one_or_none()
                
                # # Если нет - будет первым
                # if not article_exists:
                #     return f"{self.article_id}_1.{file_format}"
                
                # Если у статьи есть файлы - определим порядковый номер
                # stmt_max = select(func.max(FilesDB.name)).where(
                #     FilesDB.article_id == self.article_id
                # )
                stmt_max = select(FilesDB.name).where(
                    FilesDB.article_id == int(self.article_id)
                )
                result_max = await session.execute(stmt_max)
                all_names = result_max.scalars().all()
                if all_names == []:
                    next_num = 1 

                else:
                    # Извлекаем номер из имени файла
                    nums = lambda x :  [int(n.split('_')[-1].split('.')[0]) for n in x ]
                    next_num = max(nums(all_names)) + 1
                import random
                return f"{self.article_id}_{random.randint(10000, 99999)}_{next_num}.{file_format}"
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в generate_name при генерации имени файла для статьи {self.article_id}: {e}")
    
    async def change_prev(self, session):
        """
        Проверяет есть ли у статьи фотки.
        Если есть фотки, то у всех is_preview ставит False.
        Ставит is_preview=True на фотку с id = self.id
        """
        try:
            files_exist = await self.find_by_id_all(session)
            if files_exist:
                stmt = update(FilesDB).where(
                    (FilesDB.article_id == self.article_id) & 
                    (FilesDB.is_preview == True)
                ).values(
                    is_preview=False,
                )
                turn_False = await session.execute(stmt)
                
                stmt = update(FilesDB).where(
                    (FilesDB.id == self.id) & 
                    (FilesDB.article_id == self.article_id)
                ).values(
                    is_preview=True,
                )
                turn_True = await session.execute(stmt)

                await session.commit()
                LogsMaker().info_message(f"Файл с id={self.id} успешно назначен на превью у статьи с id={self.article_id}")
                return True
            LogsMaker().warning_message(f"Отсутствуют файлы у статьи с id={self.article_id}, не удалось назнаичть превью")
            return False 
        except Exception as e:
            await session.rollback()
            LogsMaker().error_message(f"Произошла ошибка в функции change_prev, Файл с id={self.id} не назначен на превью у статьи с id={self.article_id}: {e}")
            return False 