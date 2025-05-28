from pymongo import MongoClient
import os
from dotenv import load_dotenv

from bson.objectid import ObjectId

load_dotenv()

user = os.getenv('user')
pswd = os.getenv('pswd')

# MongoDB connection
client = MongoClient(
    host="mongodb",
    port=27017,
    username=user,
    password=pswd,
    authSource="admin"
)

client.admin.command('ismaster')

db = client["file_storage"]
files_collection = db["files"]
user_photo_collection = db["user_photo"]



class FileModel:
    def __init__(self, id=""):
        if id is not None:
            if type(id) == type(ObjectId("a" * 24)):
                id = id
            elif type(id) == type(str()) and id != '':
                id = ObjectId(id)
            self.id = id



    # блок для файлов
    def add(self, file_data):
        file_id = files_collection.insert_one(file_data).inserted_id
        return file_id

    def go_archive(self):
        return files_collection.update_one({"_id": self.id}, { "$set": { "is_archive" : False } })

    def remove(self):
        #удалить сам файл
        return files_collection.delete_one({"b24_id": self.id})

    def find_by_id(self):
        return files_collection.find_one({"_id": self.id})

    def need_update(self):
        return files_collection.find_one({"_id": self.id})

    def find_by_art_id(self):
        return files_collection.find_one({"article_id": self.id})

    def find_by_b24_id(self):
        return files_collection.find_one({"b24_id": self.id})

    def find_all_by_art_id(self):
        return files_collection.find({"article_id": self.id})



    # блок для аватарок
    def add_user_photo(self, file_data):
        file_id = user_photo_collection.insert_one(file_data).inserted_id
        return file_id

    def go_user_photo_archive(self):
        return user_photo_collection.update_one({"_id": self.id}, { "$set": { "is_archive" : False } })

    def remove_user_photo(self):
        return user_photo_collection.delete_one(self.id)

    def find_user_photo_by_id(self):
        return user_photo_collection.find_one({"_id": self.id})
    
    def find_user_photo_by_uuid(self, uuid):
        return user_photo_collection.find_one({"uuid": uuid})
