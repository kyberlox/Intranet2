from sqlalchemy.sql.expression import func
from sqlalchemy.orm.attributes import flag_modified


import json

from sqlalchemy.exc import SQLAlchemyError

from .App import get_db, update
db_gen = get_db()
database = next(db_gen)

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Cтатей")

class ArticleModel:

    def __init__(self, id=0, section_id=0):
        self.id = id
        self.section_id = section_id

        from ..models.Article import Article
        self.article = Article

        # from .App import db
        # database = db
    
    def get_current_id(self ):
        current_id = database.query(func.max(self.article.id)).scalar()
        current_id = int(current_id) + 1
        self.id = current_id
        return current_id

    def add_article(self, article_data):
        article = self.article(**article_data)
        database.add(article)
        database.commit()

        return article_data

    def need_add(self):
        db_art = database.query(self.article).filter(self.article.section_id == self.section_id).all()
        # если в таблице есть раздел
        if db_art != []:
            need = True
            for art in db_art:
                # добавить статью в таблицу, если её там нет
                if int(art.id) == int(self.id):
                    need = False
                    # print("Такой раздел уже есть", self.id)
            return need

        # если в таблице нет статей раздела
        else:
            return True

    # def update(self, article_data):
    #     #удалить статью
    #     database.query(self.article).filter(self.article.id==int(self.id)).delete()
    #     #залить заново
    #     self.add_article(article_data)
    #     database.commit()  
    #     return True
    
    def update(self, article_data):
        try:
            database.execute(update(self.article).where(self.article.id==int(self.id)).values(**article_data))
            database.commit() 
            return True
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при обновлении статьи с id = {int(self.id)}, {e}")

    '''def update(self, article_data):
        db_art = db.query(Article).get(self.id).__dict__
        for key in article_data:
            if key not in ["ID", "_sa_instance_state"]:
                if key not in db_art:
                    self.reassembly(article_data)
                    LogsMaker().warning_message(f"{db_art['id']} добавить {key} = {article_data[key]}")
                    # print(db_art['id'], "добавить", key, "=", article_data[key])
                    return True
                elif article_data[key] != db_art[key]:
                    self.reassembly(article_data)
                    LogsMaker().warning_message(f"{db_art['id']} {key} {db_art[key]} --> {article_data[key]}")
                    # print(db_art['id'], key, db_art[key], "-->", article_data[key])
                    return True
                else:
                    return False'''

    def remove(self ):
        #database.execute(delete(UsDep).where(UsDep.user_id == us_dep_key).where(UsDep.dep_id == i))
        #return db.query(Article).filter(Article.id == self.id).delete()
        #return database.execute(delete(Article).where(Article.id == self.id))
        #test = db.query(Article).filter(Article.id==int(self.id)).first()
        
        art = database.query(self.article).get(self.id)
        if art is not None:
            database.query(self.article).filter(self.article.id==int(self.id)).delete()
            database.commit()
            return True
        else:
            return False

    def remove_b24_likes(self):
        art = database.query(self.article).filter(self.article.id == self.id).first()
        art.indirect_data.pop("likes_from_b24")
        flag_modified(art, 'indirect_data')
        database.commit()
        return True

    def find_by_id(self):
        art = database.query(self.article).get(self.id)
        try:
            art.__dict__["indirect_data"] = json.loads(art.indirect_data)
        except:
            if art is not None:
                art.__dict__["indirect_data"] = art.indirect_data
            else:
                return dict()
        
        res = art.__dict__

        if '_sa_instance_state' in res.keys():
            res.pop("_sa_instance_state")

        return res

    def find_by_section_id(self):
        
        data = database.query(self.article).filter(self.article.section_id == self.section_id).all()
        
        try:
            new_data = []
            for art in data:
                art.__dict__["indirect_data"] = json.loads(art.indirect_data)
                new_data.append(art.__dict__)
        except:
            new_data = []
            for art in data:
                if art is not None:
                    art.__dict__["indirect_data"] = art.indirect_data
                    new_data.append(art.__dict__)

        return new_data
    
    def all(self):
        data = database.query(self.article).all()
        new_data = []
        try:
            for art in data:
                art.__dict__["indirect_data"] = json.loads(art.indirect_data)
                new_data.append(art.__dict__)
        except:
            for art in data:
                art.__dict__["indirect_data"] = art.indirect_data
                new_data.append(art.__dict__)

        return new_data