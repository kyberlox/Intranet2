from ..models.FileModel import FileModel
from .App import get_db

import os

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Файлов")

db_gen = get_db()
database = next(db_gen)

STORAGE_PATH = "./files_db"

class UserFilesModel():
    def __init__(self, id=None, article_id=None, name=None, original_name = "", stored_name = "", b24_url=None, active=True, content_type = ""):
        self.id = id
        self.article_id = article_id

        self.name = name
        self.original_name = original_name
        self.stored_name = stored_name
        self.b24_url = b24_url
        self.active = active
        self.content_type = content_type

        from ..models.FileModel import FileModel
        self.FileModel = FileModel
    
    def add(self, file_data):

        if self.article_id is None:
            return {'err' : 'No article_id'}

        if self.name is None:
            return {'err' : 'No name'}

        from .ArticleModel import ArticleModel
        existing_art = ArticleModel(Id=self.article_id).find_by_id()
        if existing_art:
            new_artfile = self.FileModel(article_id = int(self.article_id), name = self.name, original_name = self.original_name, b24_url=self.b24_url, active=self.active, content_type = self.content_type)
            database.add(new_artfile)
            database.commit()
        
        return new_artfile.id

    def go_archive(self):
        #return files_collection.update_one({"b24_id": self.b24_id}, { "$set": { "is_archive" : False } })
        
        #получаю объект по Id
        database.query(self.FileModel).filter(self.FileModel.id == self.id).update({"active" : False})
        database.commit()

        return True

    def find_by_id(self):
        if self.id is not None:
            file_db = database.query(self.FileModel).filter(self.FileModel.id == self.id, self.FileModel.active == True).one()
            res = file_db.__dict__
            return res
        else:
            return None

    def find_by_id_all(self):
        if self.id is not None:
            file_db = database.query(self.FileModel).get(self.id)
            res = file_db.__dict__
            return res
        else:
            return None


    def remove(self):
        #удалить сам файл
        file_data = self.find_by_id_all()
        if file_data is not None: #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! не уверен в валидности проверки
            unique_name = file_data['stored_name']
            file_path = os.path.join(STORAGE_PATH, unique_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            else:  
                LogsMaker().warning_message("File not found.")
            
            #удалить запись
            result = database.delete(file_data)
            database.commit()
            LogsMaker().ready_status_message(f"Файл {self.id} удален!")
            return result
        else:
            return "File not found."

        #return files_collection.update_one({"_id": self.id}, {"$set": {"is_archive" : True}})

    
    def need_update(self):
        if self.article_id is not None and self.original_name is not None:
            file_db = database.query(self.FileModel).filter(self.FileModel.article_id == self.article_id, self.FileModel.original_name == self.original_name).one()
            res = file_db.__dict__
            return False if self.original_name == res['original_name'] else True
        else:
            return None

        # return files_collection.find_one({"_id": self.id})

    def find_by_art_id(self):
        if self.article_id is not None:
            files_db = database.query(self.FileModel).filter(self.FileModel.article_id == self.article_id, self.FileModel.active == True).first()
            res = file_db.__dict__
            return res
        else:
            return None

        #return files_collection.find_one({"article_id": self.art_id})

    #def find_by_b24_id(self):
        #return files_collection.find_one({"b24_id": self.id})

    def find_all_by_art_id(self):
        if self.article_id is not None:
            files_db = database.query(self.FileModel).filter(self.FileModel.article_id == self.article_id, self.FileModel.active == True).all()
            result = []
            for file_db in files_db:
                res = file_db.__dict__
                result.append(res)
            
            return result
        else:
            return None
        #return files_collection.find({"article_id": self.art_id})

    #def find_all_by_b24_id(self):
    #    return files_collection.find({"b24_id": self.art_id})

    # def update_data(self, new_data):
    #     files_collection.update_one({"_id": self.id}, {'$set': new_data})