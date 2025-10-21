from ..models.UserFiles import UserFiles
from .App import get_db

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Фотографий пользователей")

db_gen = get_db()
database = next(db_gen)

USER_STORAGE_PATH = "./files_db/user_photo"

class UserFilesModel():
    def __init__(self, id=None, user_id=None, name=None, b24_url=None, active=True):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.b24_url = b24_url
        self.active = active
        self.URL = f"/api/user_files/{self.name}"

    def add_user_photo(self ):
        if self.user_id is None:
            return {'err' : 'No user_id'}

        if self.name is None:
            return {'err' : 'No name'}
        self.name = self.generate_name(self.name)
        self.URL = f"/api/user_files/{self.name}"

        from .UserModel import UserModel
        existing_user = UserModel(Id=self.user_id).find_by_id()
        if existing_user and existing_user['active'] is True:
            #проверка есть ли пользователя автарка
            user_photo_exists = database.query(UserFiles).filter(UserFiles.user_id == self.user_id, UserFiles.active == True).first()
            #если уже есть - заменить
            if user_photo_exists:
                #проверить, вдруг это тоже самое
                if user_photo_exists.b24_url == self.b24_url:
                    return False
                else: #если другая
                    #текущую актуальную - в архив
                    self.id = user_photo_exists.id
                    self.go_user_photo_archive()
            #если нет - просто создать
            new_usfile = UserFiles(name = self.name, b24_url=self.b24_url, active=self.active, user_id=int(self.user_id), URL=self.URL)
            database.add(new_usfile)
            database.commit()
        
        return new_usfile.__dict__

    #Пока они mongo - переделай в psql
    def go_user_photo_archive(self):
        try:
            existing_photo = database.query(UserFiles).filter(UserFiles.id == self.id).first()
            if existing_photo:
                existing_photo.active = False 
                database.commit()
                return LogsMaker().info_message(f"Фото пользователя с id = {self.id} успешно изъято из архива")
            return LogsMaker().info_message(f"Фото пользователя с id = {self.id} не найдено")
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка при изъятии из архива фотки пользователя с id = {self.id}")
            
        # return user_photo_collection.update_one({"_id": self.id}, { "$set": { "is_archive" : False } })

    def remove_user_photo(self):
        # return user_photo_collection.delete_one(self.id)
        try:
            existing_photo = database.query(UserFiles).filter(UserFiles.id == self.id).first()
            if existing_photo:
                unique_name = file_data['name']
                file_path = os.path.join(USER_STORAGE_PATH, unique_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:  
                    LogsMaker().warning_message("File not found.")

                #удалить запись
                result = database.delete(existing_photo)
                database.commit()
                return LogsMaker().info_message(f"Фото пользователя с id = {self.id} успешно отправлено в архив")

            return LogsMaker().info_message(f"Фото пользователя с id = {self.id} не найдено")
            
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Ошибка при отправлении в архив фотки пользователя с id = {self.id}")
        # return user_photo_collection.update_one({"_id": self.id}, {"$set": {"is_archive" : True}})

    def find_user_photo_by_id(self):
        user_photo_inf = database.query(UserFiles).filter(UserFiles.id == self.id, UserFiles.active == True).first()
        return user_photo_inf
        # return user_photo_collection.find_one({"_id": self.id})
    
    def find_user_photo_by_uuid(self, uuid):
        user_photo_inf = database.query(UserFiles).filter(UserFiles.user_id == uuid).first()
        return user_photo_inf
        # return user_photo_collection.find_one({"uuid": uuid})
    
    def generate_name(self, file_name):
        #name формируется по принципу {user_id}_{порядковый номер файля для пользователя}.{формат файла}
        file_format = file_name.split(".")[-1]
        
        #проверим есть к чему крепить файл
        if self.user_id is not None:
            user_exists = database.query(UserFiles).filter(UserFiles.user_id == self.user_id).first()
            
            #если нет - будет первым
            if not user_exists:
                return f"{self.user_id}_1.{file_format}"
            #если у элемента есть файлы - определим порядковый номер
            # Получаем максимальный текущий номер
            max_num = database.query(func.max(UserFiles.name)).filter(
                UserFiles.user_id == self.user_id
            ).scalar()

            # Извлекаем номер из имени файла
            if max_num:
                current_num = int(max_num.split('_')[-1].split('.')[0])
                next_num = current_num + 1
            else:
                next_num = 1

            return f"{self.user_id}_{next_num}.{file_format}"
        else:
            return None