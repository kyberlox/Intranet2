from pymongo import MongoClient
import os
from dotenv import load_dotenv

from bson.objectid import ObjectId

load_dotenv()

user = os.getenv('user')
pswd = os.getenv('pswd')

STORAGE_PATH = "./files_db"

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
ai_dialogs_collection = db["ai_dialogs"]


class FileModel:
    def __init__(self, id="", art_id = None, b24_id = None):
        if id is not None:
            if type(id) == type(ObjectId("a" * 24)):
                id = id
            elif type(id) == type(str()) and id != '':
                id = ObjectId(id)
            self.id = id
        self.art_id = art_id
        self.b24_id = b24_id

    def create_index_files(self):
        #создаем индексы
        files_collection.create_index(
            [
                ("id", 1),
                ("original_name", 1),
                ("stored_name", 1),
                ("content_type", 1),
                ("article_id", 1),
                ("b24_id", 1),
                ("file_url", 1)
            ],
            background=True
        )
        return {"status": True}

    def create_index_user_photo(self):
        user_photo_collection.create_index(
            [
                ("id", 1),
                ("name", 1),
                ("format", 1),
                ("uuid", 1),
                ("b24_url", 1)
            ],
            background=True
        )
        return {"status": True}
    
    def create_index_ai_dialogs(self):
        ai_dialogs_collection.create_index(
            [
                ("id", 1),
                ("name", 1),
                ("user_uuid", 1),
                ("messages", 1)
            ],
            background=True
        )
        return {"status": True}

    # блок для файлов
    def add(self, file_data):
        file_id = files_collection.insert_one(file_data).inserted_id
        return file_id

    def go_archive(self):
        return files_collection.update_one({"b24_id": self.b24_id}, { "$set": { "is_archive" : False } })

    def remove(self):
        #удалить сам файл
        file_data = files_collection.find_one({"_id": self.id})
        if file_data is not None:
            
            unique_name = file_data['stored_name']
            file_path = os.path.join(STORAGE_PATH, unique_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            else:  
                print("File not found.")
            
            #удалить запись
            result = files_collection.delete_one({"_id": self.id})  
            print(result.deleted_count)
            return result.deleted_count
        else:
            return "File not found."

        #return files_collection.update_one({"_id": self.id}, {"$set": {"is_archive" : True}})

    def find_by_id(self):
        return files_collection.find_one({"_id": self.id})

    def need_update(self):
        return files_collection.find_one({"_id": self.id})

    def find_by_art_id(self):
        return files_collection.find_one({"article_id": self.art_id})

    def find_by_b24_id(self):
        return files_collection.find_one({"b24_id": self.id})

    def find_all_by_art_id(self):
        return files_collection.find({"article_id": self.art_id})

    def find_all_by_b24_id(self):
        return files_collection.find({"b24_id": self.art_id})



    # блок для аватарок
    def add_user_photo(self, file_data):
        file_id = user_photo_collection.insert_one(file_data).inserted_id
        return file_id

    def go_user_photo_archive(self):
        return user_photo_collection.update_one({"_id": self.id}, { "$set": { "is_archive" : False } })

    def remove_user_photo(self):
        # return user_photo_collection.delete_one(self.id)
        return user_photo_collection.update_one({"_id": self.id}, {"$set": {"is_archive" : True}})

    def find_user_photo_by_id(self):
        return user_photo_collection.find_one({"_id": self.id})
    
    def find_user_photo_by_uuid(self, uuid):
        return user_photo_collection.find_one({"uuid": uuid})