from pymongo import MongoClient
import os
from dotenv import load_dotenv

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

class FileModel:
    def __init__(self, id=""):
        self.id = id

    def add(self, file_data):
        file_id = files_collection.insert_one(file_data).inserted_id
        return file_id

    def remove(self):
        return files_collection.delete_one(self.id)

    def find_by_id(self):
        return files_collection.find_one({"_id": self.id})