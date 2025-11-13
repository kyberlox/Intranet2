from pymongo import MongoClient
import os
import time
from dotenv import load_dotenv

from bson.objectid import ObjectId

from src.services.LogsMaker import LogsMaker

load_dotenv()

user = os.getenv('user')
pswd = os.getenv('pswd')

STORAGE_PATH = "./files_db"

# MongoDB connection

# client = MongoClient(
#     host="mongodb",
#     port=27017,
#     username=user,
#     password=pswd,
#     authSource="admin"
# )
# client.admin.command('ismaster')

# def create_db_client():
#     max_retries = 5
#     retry_delay = 15
    
#     for i in range(max_retries):
#         try:
#             client = MongoClient(host="mongodb", port=27017, username=user, password=pswd, authSource="admin")
#             client.admin.command('ismaster')
#             LogsMaker().ready_status_message("mongodb успешно подключен!")
#             return client
#         except Exception as e:
#             LogsMaker().warning_message(f"❌ Connection attempt {i+1}/{max_retries} failed: {e}")
#             if i < max_retries - 1:
#                 LogsMaker().info_message(f"🕐 Retrying in {retry_delay} seconds...")
#                 time.sleep(retry_delay)
    
#     LogsMaker().fatal_message("Failed to connect to mongodb after multiple attempts")

client = create_db_client()

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
    

    # блок для аватарок
    