from ..models.UserFiles import UserFiles
from .App import select, func

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Фотографий пользователей")


USER_STORAGE_PATH = "./files_db/user_photo"

class UserFilesModel():
    def __init__(self, id=None, user_id=None, name=None, b24_url=None, active=True):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.b24_url = b24_url
        self.active = active
        self.URL = f"/api/user_files/{self.name}"

    async def add_user_photo(self, session):
        try:
            if self.user_id is None:
                LogsMaker().info_message(f"Ошибка в функции add_user_photo UserFiles: No user_id")
                return False

            if self.name is None:
                LogsMaker().info_message(f"Ошибка в функции add_user_photo UserFiles: No name")
                return False

                
            self.name = await self.generate_name(session=session, file_name=self.name)
            self.URL = f"/api/user_files/{self.name}"

            from .UserModel import UserModel
            user_model = UserModel(Id=self.user_id)
            existing_user = await user_model.find_by_id(session)
            if existing_user and existing_user['active'] is True:
                # Проверка есть ли у пользователя аватарка
                stmt_photo = select(UserFiles).where(
                    UserFiles.user_id == self.user_id, 
                    UserFiles.active == True
                )
                result_photo = await session.execute(stmt_photo)
                user_photo_exists = result_photo.scalar_one_or_none()
                
                # Если уже есть - заменить
                if user_photo_exists:
                    # Проверить, вдруг это тоже самое
                    if user_photo_exists.b24_url == self.b24_url:
                        return False
                    else:  # Если другая
                        # Текущую актуальную - в архив
                        self.id = user_photo_exists.id
                        await self.go_user_photo_archive(session)
                
                #ищем доступный айдишник
                stmt_max = select(func.max(UserFiles.id))
                result_max = await session.execute(stmt_max)
                max_id = result_max.scalar() or 0
                new_id = max_id + 1

                # Создаем новую запись
                new_usfile = UserFiles(
                    id=new_id,
                    name=self.name, 
                    b24_url=self.b24_url, 
                    active=self.active, 
                    user_id=int(self.user_id), 
                    URL=self.URL
                )
                w_photo = {
                    'id':new_id,
                    'name':self.name, 
                    'b24_url':self.b24_url, 
                    'active':self.active, 
                    'user_id':int(self.user_id), 
                    'URL':self.URL
                }
                session.add(new_usfile)
                await session.commit()
                return w_photo
            else: 
                LogsMaker().info_message(f"Ошибка в функции add_user_photo UserFiles: User not found or inactive")
                return False
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в add_user_photo при добавлении фото для пользователя {self.user_id}: {e}")

    async def go_user_photo_archive(self, session):
        try:
            stmt = select(UserFiles).where(UserFiles.id == self.id)
            result = await session.execute(stmt)
            existing_photo = result.scalar_one_or_none()
            
            if existing_photo:
                existing_photo.active = False
                await session.commit()
                return LogsMaker().info_message(f"Фото пользователя с id = {self.id} успешно отправлено в архив")
            return LogsMaker().info_message(f"Фото пользователя с id = {self.id} не найдено")
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в go_user_photo_archive при архивировании фото {self.id}: {e}")

    async def remove_user_photo(self, session, file_data: dict):
        """
        Удаляет файл из папки user_photo и в БД таблицы User меняет значение
        колонки photo_file_id на None
        """
        from ..models.User import User
        import os
        try:
            stmt = select(UserFiles).where(UserFiles.id == self.id)
            result = await session.execute(stmt)
            existing_photo = result.scalar_one_or_none()
            
            if existing_photo:
                # Удаляем физический файл
                unique_name = file_data['name']
                file_path = os.path.join(USER_STORAGE_PATH, unique_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:  
                    LogsMaker().warning_message(f"Файл {file_path} не найден")

                # Удаляем запись из базы
                await session.delete(existing_photo)
                # Удаляем запись из базы User
                stmt = select(User).where(User.photo_file_id == self.id)
                result = await session.execute(stmt)
                existing_user = result.scalar_one_or_none()
                existing_user.photo_file_id = None
                await session.commit()
                return LogsMaker().info_message(f"Фото пользователя с id = {self.id} успешно удалено")

            return LogsMaker().info_message(f"Фото пользователя с id = {self.id} не найдено")
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка в remove_user_photo при удалении фото {self.id}: {e}")

    async def find_user_photo_by_id(self, session):
        try:
            stmt = select(UserFiles).where(
                UserFiles.id == self.id, 
                UserFiles.active == True
            )
            result = await session.execute(stmt)
            res = result.scalar_one_or_none()
            if res:
                user_photo_inf = res.__dict__

                return user_photo_inf
            return None
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_user_photo_by_id при поиске фото {self.id}: {e}")

    async def find_user_photo_by_uuid(self, session, uuid: int):
        try:
            stmt = select(UserFiles).where(UserFiles.user_id == uuid)
            result = await session.execute(stmt)
            user_photo_inf = result.scalar_one_or_none()
            return user_photo_inf
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в find_user_photo_by_uuid при поиске фото пользователя {uuid}: {e}")

    async def generate_name(self, session, file_name: str):
        try:
            # name формируется по принципу {user_id}_{порядковый номер файла для пользователя}.{формат файла}
            file_format = file_name.split(".")[-1]
            
            # Проверим есть к чему крепить файл
            if self.user_id is not None:
                stmt_exists = select(UserFiles).where(UserFiles.user_id == self.user_id)
                result_exists = await session.execute(stmt_exists)
                user_exists = result_exists.first()
                
                # Если нет - будет первым
                if not user_exists:
                    return f"{self.user_id}_1.{file_format}"
                
                # Если у пользователя есть файлы - определим порядковый номер
                stmt_max = select(func.max(UserFiles.name)).where(
                    UserFiles.user_id == self.user_id
                )
                result_max = await session.execute(stmt_max)
                max_num = result_max.scalar_one_or_none()

                # Извлекаем номер из имени файла
                if max_num:
                    current_num = int(max_num.split('_')[-1].split('.')[0])
                    next_num = current_num + 1
                else:
                    next_num = 1

                return f"{self.user_id}_{next_num}.{file_format}"
            else:
                return None
                
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка в generate_name при генерации имени файла для пользователя {self.user_id}: {e}")