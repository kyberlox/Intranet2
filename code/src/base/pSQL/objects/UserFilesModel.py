from ..models.UserFiles import UserFiles
from .App import get_db

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Фотографий пользователей")

db_gen = get_db()
database = next(db_gen)

class UserFilesModel():
    def __init__(self, id=None, user_id=None, name=None, b24_url=None, active=True):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.b24_url = b24_url
        self.active = active

    def add_user_photo(self ):
        if self.user_id is None:
            return {'err' : 'No user_id'}

        if self.name is None:
            return {'err' : 'No name'}

        from .UserModel import UserModel

        existing_user = UserModel(Id=self.user_id).find_by_id()
        if existing_user and existing_user['active'] is True:
            new_usfile = UserFiles(name = self.name, b24_url=self.b24_url, active=self.active, user_id=int(self.user_id))
            database.add(new_usfile)
            database.commit()
        
        return new_usfile.id

    #Пока они mongo - переделай в psql
    def go_user_photo_archive(self):
        return user_photo_collection.update_one({"_id": self.id}, { "$set": { "is_archive" : False } })

    def remove_user_photo(self):
        # return user_photo_collection.delete_one(self.id)
        return user_photo_collection.update_one({"_id": self.id}, {"$set": {"is_archive" : True}})

    def find_user_photo_by_id(self):
        return user_photo_collection.find_one({"_id": self.id})
    
    def find_user_photo_by_uuid(self, uuid):
        return user_photo_collection.find_one({"uuid": uuid})