from sqlalchemy.sql.expression import func
from sqlalchemy.orm.attributes import flag_modified

from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

import json

from sqlalchemy.exc import SQLAlchemyError

from .App import update, select, delete

from .App import AsyncSessionLocal
import asyncio

# db_gen = get_db() get_db, 
# database = next(db_gen)

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Cтатей")

class ArticleModel:

    def __init__(self, id=0, section_id: int=0):
        self.id = id
        self.section_id = section_id

        from ..models.Article import Article
        self.article = Article

        # from .App import db
        # database = db
    
    async def get_current_id(self, session):
        # async with AsyncSessionLocal() as session:
        stmt = select(func.max(self.article.id))
        result = await session.execute(stmt)
        current_max_id = result.scalar()
        # current_id = database.query(func.max(self.article.id)).scalar()
        current_id = int(current_max_id) + 1
        self.id = current_id
        return current_id

    async def add_article(self, article_data, session):
        # async with AsyncSessionLocal() as session:
        try:
            # Сначала проверяем, существует ли статья
            stmt = select(self.article).where(self.article.id == article_data['id'])
            result = await session.execute(stmt)
            existing_article = result.scalar_one_or_none()
            
            if existing_article:
                # Обновляем существующую
                for key, value in article_data.items():
                    setattr(existing_article, key, value)
                await session.commit()
                LogsMaker().info_message(f"Статья {article_data['id']} обновлена")
            else:
                # Создаем новую
                article = self.article(**article_data)
                session.add(article)
                await session.commit()
                LogsMaker().info_message(f"Статья {article_data['id']} создана")
            
            return article_data
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при добавлении статьи : {e}")

    async def need_add(self, session):
        # async with AsyncSessionLocal() as session:
        try:
            stmt = select(self.article).where(self.article.section_id == self.section_id)
            result = await session.execute(stmt)
            db_art = result.scalars().all()
            # db_art = database.query(self.article).filter(self.article.section_id == self.section_id).all()
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
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при проверке на обновление статьи с id = {self.id}: {e}")

    # def update(self, article_data):
    #     #удалить статью
    #     database.query(self.article).filter(self.article.id==int(self.id)).delete()
    #     #залить заново
    #     self.add_article(article_data)
    #     database.commit()  
    #     return True
    
    async def update(self, article_data, session):
        try:
            # async with AsyncSessionLocal() as session:
            await session.execute(update(self.article).where(self.article.id==int(self.id)).values(**article_data))
            await session.commit() 
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

    async def remove(self, session ):
        #database.execute(delete(UsDep).where(UsDep.user_id == us_dep_key).where(UsDep.dep_id == i))
        #return db.query(Article).filter(Article.id == self.id).delete()
        #return database.execute(delete(Article).where(Article.id == self.id))
        #test = db.query(Article).filter(Article.id==int(self.id)).first()
        # async with AsyncSessionLocal() as session:
        try:
            stmt = select(self.article).where(self.article.id==int(self.id))
            art = await session.execute(stmt)
            # art = database.query(self.article).get(self.id)
            if art is not None:
                stmt = delete(self.article).where(self.article.id==int(self.id))
                result = await session.execute(stmt)
                # database.query(self.article).filter(self.article.id==int(self.id)).delete()
                await session.commit()
                return True
            else:
                return False
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении статьи с id = {self.id}: {e}")

    async def remove_b24_likes(self, session):
        # async with AsyncSessionLocal() as session:
        try:
            stmt = select(self.article).where(self.article.id==int(self.id))
            result = await session.execute(stmt)
            art = result.scalar_one_or_none()
            # art = database.query(self.article).filter(self.article.id == self.id).first()
            art.indirect_data.pop("likes_from_b24")
            flag_modified(art, 'indirect_data')
            await session.commit()
            return True
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при удалении лайка со статьи с id = {self.id}: {e}")

    async def find_by_id(self, session):
        # async with AsyncSessionLocal() as session:
        art = await session.get(self.article, self.id)
        # art = database.query(self.article).get(self.id)
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

    async def find_by_section_id(self, session):
        # async with AsyncSessionLocal() as session:
        stmt = select(self.article).where(self.article.section_id == self.section_id)
        result = await session.execute(stmt)
        data = result.scalars().all()
        # data = database.query(self.article).filter(self.article.section_id == self.section_id).all()
        
        
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
    
    async def all(self, session):
        # async with AsyncSessionLocal() as session:
        res = await session.execute(select(self.article))
        data = res.scalars().all()
        # data = database.query(self.article).all()
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