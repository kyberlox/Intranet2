from sqlalchemy.sql.expression import func
from sqlalchemy.orm.attributes import flag_modified

from ..models import Article
from .App import db

import json

from sqlalchemy.exc import SQLAlchemyError


#!!!!!!!!!!!!!!!
from ....services.LogsMaker import LogsMaker
#!!!!!!!!!!!!!!!

class ArticleModel:

    def __init__(self, id=0, section_id=0):
        self.id = id
        self.section_id = section_id
        self.article = Article

        self.db = db
    
    def get_current_id(self ):
        current_id = self.db.query(func.max(Article.id)).scalar()
        current_id = int(current_id) + 1
        self.id = current_id
        self.db.close()
        return current_id

    def add_article(self, article_data):
        article = Article(**article_data)
        self.db.add(article)
        self.db.commit()
        self.db.close()

        return article_data

    def need_add(self):
        db_art = self.db.query(Article).filter(Article.section_id == self.section_id).all()
        # если в таблице есть раздел
        self.db.close()
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

    def update(self, article_data):
        #удалить статью
        self.db.query(Article).filter(Article.id==int(self.id)).delete()
        #залить заново
        self.add_article(article_data)
        self.db.commit()
        self.db.close()    
        return True

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
        #self.db.execute(delete(UsDep).where(UsDep.user_id == us_dep_key).where(UsDep.dep_id == i))
        #return db.query(Article).filter(Article.id == self.id).delete()
        #return self.db.execute(delete(Article).where(Article.id == self.id))
        #test = db.query(Article).filter(Article.id==int(self.id)).first()
        
        art = self.db.query(Article).get(self.id)
        if art is not None:
            self.db.query(Article).filter(Article.id==int(self.id)).delete()
            self.db.commit()
            self.db.close()
            return True
        else:
            self.db.close()
            return False

    def remove_b24_likes(self):
        art = self.db.query(self.article).filter(self.article.id == self.id).first()
        art.indirect_data.pop("likes_from_b24")
        flag_modified(art, 'indirect_data')
        self.db.commit()
        self.db.close()
        return True

    def find_by_id(self):
        art = self.db.query(Article).get(self.id)
        try:
            art.__dict__["indirect_data"] = json.loads(art.indirect_data)
        except:
            if art is not None:
                art.__dict__["indirect_data"] = art.indirect_data
            else:
                self.db.close()
                return dict()
        
        res = art.__dict__
        self.db.close()
        return res

    def find_by_section_id(self):
        
        data = self.db.query(Article).filter(Article.section_id == self.section_id).all()
        new_data = []
        try:
            for art in data:
                art.__dict__["indirect_data"] = json.loads(art.indirect_data)
                new_data.append(art.__dict__)
        except:
            for art in data:
                if art is not None:
                    art.__dict__["indirect_data"] = art.indirect_data
                    new_data.append(art.__dict__)

        return new_data
    
    def all(self):
        data = db.query(Article).all()
        new_data = []
        try:
            for art in data:
                art.__dict__["indirect_data"] = json.loads(art.indirect_data)
                new_data.append(art.__dict__)
        except:
            for art in data:
                art.__dict__["indirect_data"] = art.indirect_data
                new_data.append(art.__dict__)

        self.db.close()
        return new_data