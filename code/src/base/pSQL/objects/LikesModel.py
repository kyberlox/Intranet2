from sqlalchemy import desc
from sqlalchemy.sql.expression import func

from typing import List, Optional, Dict

from datetime import datetime, timedelta
from .App import get_db, AsyncSessionLocal, select

import asyncio

db_gen = get_db()
database = next(db_gen)



from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Лайков")



class LikesModel:
    def __init__(self, user_id: Optional[int] = None, art_id: Optional[int] = None, user_uuid: Optional[str] = None):
        
        self.user_id = user_id
        self.art_id = art_id
        self.user_uuid = user_uuid

        # from .App import db
        # database = db

        from ..models.Likes import Likes
        self.Likes = Likes

        self.reactions = {
            "views" : 0,
            "likes" : {'count': 0, 'likedByMe': False}
        }

    async def add_or_remove_like(self):
        """
        Ставит лайк статье если пользователь его еще не ставил
        Убрает лайк со статьи
        Меняет статус лайка
        """

        from .ViewsModel import ViewsModel
        views = await ViewsModel(art_id=self.art_id).get_art_viewes()
        self.reactions["views"] = views

        likes_count = await self.get_likes_count()
        self.reactions["likes"]["count"] = likes_count
        
        async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже активный лайк
            stmt = select(self.Likes).where(self.Likes.user_id == self.user_id, self.Likes.article_id == self.art_id)
            result = await session.execute(stmt)
            existing_like = result.first()
            # existing_like = database.query(self.Likes).filter(
            #     self.Likes.user_id == self.user_id,
            #     self.Likes.article_id == self.art_id
            # ).first()

            

            if not existing_like:
                # создаем новый лайк если прежде никогда не стоял
                new_like = self.Likes(
                    user_id=self.user_id,
                    article_id=self.art_id,
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                await session.add(new_like)
                await session.commit()
                self.reactions["likes"]["count"] += 1
                self.reactions["likes"]["likedByMe"] = True

            else:
                if existing_like.is_active:
                    self.reactions["likes"]["count"] -= 1
                else:
                    self.reactions["likes"]["count"] += 1

                existing_like.is_active = not existing_like.is_active
                await session.commit()

                self.reactions["likes"]["likedByMe"] = existing_like.is_active

        return self.reactions

    async def _get_VM(self):
        try:
            VM = ViewsModel()
            VM.art_id = self.art_id
            views = await VM.get_art_viewes()
            return views
        except Exception as e:
            return 0
            LogsMaker().error_message(str(e))

    async def has_liked(self ) -> bool:
        """
        Проверяет, поставил ли пользователь лайк статье.
        """
        try:
            from .ViewsModel import ViewsModel
            views = await ViewsModel(art_id=self.art_id).get_art_viewes()
            self.reactions["views"] = views

            likes_count = await self.get_likes_count()
            self.reactions["likes"]["count"] = likes_count
            
            likes_count = await self.get_likes_count()
            
            reactions = {}
            async with AsyncSessionLocal() as session:
            # Проверяем, есть ли уже активный лайк
                stmt = select(self.Likes).where(self.Likes.user_id == self.user_id, self.Likes.article_id == self.art_id)
                result = await session.execute(stmt)
                existing_like = result.first()
            # Проверяем, есть ли уже активный лайк
            # existing_like = database.query(self.Likes).filter(
            #     self.Likes.user_id == self.user_id,
            #     self.Likes.article_id == self.art_id
            # ).first()
             

            if existing_like:
                self.reactions["likes"]["likedByMe"] = existing_like.is_active
            
            return self.reactions

        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при выводе лайка статьи с id = {self.art_id}: {e}")


    async def get_likes_count(self ) -> int:
        """
        Возвращает количество активных лайков для статьи.
        """
        async with AsyncSessionLocal() as session:
            # Проверяем, есть ли уже активный лайк
            stmt = select(self.Likes).where(self.Likes.user_id == self.user_id, self.Likes.article_id == self.art_id)
            result = await session.execute(stmt)
            res = result.count()
            # res = database.query(self.Likes).filter(
            #     self.Likes.article_id == self.art_id,
            #     self.Likes.is_active == True
            # ).count()
         
        return res

    async def get_user_likes(self ) -> List[int]:
        """
        Возвращает список ID статей, которые лайкнул пользователь.

        Args:
            user_id: ID пользователя

        Returns:
            Список article_id, которые пользователь лайкнул
        """
        async with AsyncSessionLocal() as session:
            # Проверяем, есть ли уже активный лайк
            stmt = select(self.Likes.article_id).where(self.Likes.user_id == self.user_id, self.Likes.article_id == self.art_id)
            result = await session.execute(stmt)
            likes = result.all()
        # likes = database.query(self.Likes.article_id).filter(
        #     self.Likes.user_id == self.user_id,
        #     self.Likes.is_active == True
        # ).all()
        
         

        return [like.article_id for like in likes]

    async def get_article_likers(self ) -> List[int]:
        """
        Возвращает список ID пользователей, которые лайкнули статью.

        Args:
            art_id: ID статьи

        Returns:
            Список user_id пользователей, которые лайкнули статью
        """
        async with AsyncSessionLocal() as session:
            # Проверяем, есть ли уже активный лайк
            stmt = select(self.Likes.user_id).where(self.Likes.user_id == self.user_id, self.Likes.article_id == self.art_id)
            result = await session.execute(stmt)
            likers = result.all()
        # likers = database.query(self.Likes.user_id).filter(
        #     self.Likes.article_id == self.art_id,
        #     self.Likes.is_active == True
        # ).all()
        
         

        return [liker.user_id for liker in likers]

    async def add_like_from_b24(self, created_at) -> bool:
        """
        Пользователь поставил лайк статье.
        Возвращает True, если лайк успешно добавлен, False если лайк уже существует.
        """
        # Проверяем, есть ли уже активный лайк
        async with AsyncSessionLocal() as session:
            # Проверяем, есть ли уже активный лайк
            stmt = select(self.Likes).where(self.Likes.user_id == self.user_id, self.Likes.article_id == self.art_id, self.Likes.is_active == True)
            result = await session.execute(stmt)
            existing_like = result.first()
        # existing_like = database.query(self.Likes).filter(
        #     self.Likes.user_id == self.user_id,
        #     self.Likes.article_id == self.art_id,
        #     self.Likes.is_active == True
        # ).first()

            if existing_like:
                return False  # Лайк уже существует

            # Если лайк был, но is_active=False, обновляем его
            # inactive_like = database.query(Likes).filter(
            #     Likes.user_id == self.user_id,
            #     Likes.article_id == self.art_id,
            #     Likes.is_active == False
            # ).first()

            # if inactive_like:
            #     inactive_like.is_active = True
            #     inactive_like.created_at = datetime.utcnow()
            # else:
                # Создаем новый лайк
            new_like = self.Likes(
                user_id=self.user_id,
                article_id=self.art_id,
                is_active=True,
                created_at=created_at
            )
            await session.add(new_like)

            await session.commit()
         
        return True

    # def has_liked_by_uuid(self): 
    #     user = database.query(User).filter(User.uuid == self.user_uuid).subquery()
    #     stmt = select(Likes.article_id).where(Likes.user_id == user.с.id)
    #     result = database.execute(stmt).fetchall()
    #     return [re for re in result]

    @classmethod
    def get_popular_articles(cls, limit: int = 10) -> List[Dict[str, int]]:
        """
        Возвращает список самых популярных статей по количеству лайков

        Args:
            session: SQLAlchemy сессия
            limit: Количество возвращаемых статей

        Returns:
            Список словарей с данными статей:               @database
            [{'article_id': int, 'likes_count': int}, ...]
        """
        from .App import db
        from ..models.Likes import Likes

        popular_articles = db.query(
            Likes.article_id,
            func.count(Likes.id).label('likes_count')
        ).filter(
            Likes.is_active == True
        ).group_by(
            Likes.article_id
        ).order_by(
            desc('likes_count')
        ).limit(limit).all()

        db.close()
        
        return [{
            'article_id': article.article_id,
            'likes_count': article.likes_count
        } for article in popular_articles]

    @classmethod
    def get_recent_popular_articles(cls, days: int = 30, limit: int = 10):
        """
        Возвращает популярные статьи за последние N дней
        """
        from .App import db
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        from ..models.Likes import Likes

        popular = db.query(
            Likes.article_id,
            func.count(Likes.id).label('likes_count')
        ).filter(
            Likes.is_active == True,
            Likes.created_at >= cutoff_date
        ).group_by(
            Likes.article_id
        ).order_by(
            desc('likes_count')
        ).limit(limit).all()

        db.close()
        
        return [dict(article_id=row.article_id, likes_count=row.likes_count) for row in popular]