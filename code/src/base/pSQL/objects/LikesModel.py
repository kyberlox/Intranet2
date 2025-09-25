from sqlalchemy import desc
from sqlalchemy.sql.expression import func

from typing import List, Optional, Dict

from datetime import datetime, timedelta




from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Лайков")



class LikesModel:
    def __init__(self, user_id: Optional[int] = None, art_id: Optional[int] = None, user_uuid: Optional[str] = None):
        
        self.user_id = user_id
        self.art_id = art_id
        self.user_uuid = user_uuid

        from .App import db
        self.session = db

        from ..models.Likes import Likes
        self.Likes = Likes

    def add_or_remove_like(self ) -> bool:
        from .ViewsModel import ViewsModel
        """
        Ставит лайк статье если пользователь его еще не ставил
        Убрает лайк со статьи
        Меняет статус лайка
        """
        reactions = {}
        # Проверяем, есть ли уже активный лайк
        existing_like = self.session.query(self.Likes).filter(
            self.Likes.user_id == self.user_id,
            self.Likes.article_id == self.art_id
        ).first()
        views = ViewsModel(art_id=self.art_id).get_art_viewes()
        if not existing_like:
            # создаем новый лайк если прежде никогда не стоял
            new_like = self.Likes(
                user_id=self.user_id,
                article_id=self.art_id,
                is_active=True,
                created_at=datetime.utcnow()
            )
            self.session.add(new_like)
            self.session.commit()
            self.session.close()
            likes_count = self.get_likes_count()

            likes = {'count': likes_count, 'likedByMe': True}
            reactions['views'] = views
            reactions['likes'] = likes
            return reactions

        elif existing_like.is_active is False:
            # если лайк не был поставлен, ставим
            existing_like.is_active = True
            self.session.commit()
            self.session.close()
            likes_count = self.get_likes_count()

            likes = {'count': likes_count, 'likedByMe': True}
            reactions['views'] = views
            reactions['likes'] = likes
            return reactions

        elif existing_like.is_active is True:
            # если лайк был поставлен, убираем
            existing_like.is_active = False
            self.session.commit()
            self.session.close()

            likes_count = self.get_likes_count()

            likes = {'count': likes_count, 'likedByMe': False}
            reactions['views'] = views
            reactions['likes'] = likes
            return reactions


    def has_liked(self ) -> bool:
        try:
            from .ViewsModel import ViewsModel
            """
            Проверяет, поставил ли пользователь лайк статье.
            """
            reactions = {}
            # Проверяем, есть ли уже активный лайк
            existing_like = self.session.query(self.Likes).filter(
                self.Likes.user_id == self.user_id,
                self.Likes.article_id == self.art_id
            ).first()
            # self.session.close()

            views = ViewsModel(art_id=self.art_id).get_art_viewes()
            
            
            
            if not existing_like:
                # если лайк никогда не существовал, значит False
                likes_count = self.get_likes_count()

                likes = {'count': likes_count, 'likedByMe': False}
                reactions['views'] = views
                reactions['likes'] = likes
                return reactions

            elif existing_like.is_active is False:
                # если лайк не был поставлен, но когда то стоял возвращаем False
                likes_count = self.get_likes_count()

                likes = {'count': likes_count, 'likedByMe': False}
                reactions['views'] = views
                reactions['likes'] = likes
                return reactions

            elif existing_like.is_active is True:
                # если лайк был поставлен, возвращаем True

                likes_count = self.get_likes_count()

                likes = {'count': likes_count, 'likedByMe': True}
                reactions['views'] = views
                reactions['likes'] = likes
                return reactions
            # return self.session.query(Likes).filter(
            #     Likes.user_id == self.user_id,
            #     Likes.article_id == self.art_id,
            #     Likes.is_active == True
            # ).count() > 0
        except Exception as e:
            self.session.rollback()
            return LogsMaker().error_message(f"Ошибка при выводе лайка статьи с id = {self.art_id}: {e}")
        finally:
            self.session.close()


    def get_likes_count(self ) -> int:
        """
        Возвращает количество активных лайков для статьи.
        """
        res = self.session.query(self.Likes).filter(
            self.Likes.article_id == self.art_id,
            self.Likes.is_active == True
        ).count()
        self.session.close()
        return res

    def get_user_likes(self ) -> List[int]:
        """
        Возвращает список ID статей, которые лайкнул пользователь.

        Args:
            user_id: ID пользователя

        Returns:
            Список article_id, которые пользователь лайкнул
        """
        likes = self.session.query(self.Likes.article_id).filter(
            self.Likes.user_id == self.user_id,
            self.Likes.is_active == True
        ).all()
        
        self.session.close()

        return [like.article_id for like in likes]

    def get_article_likers(self ) -> List[int]:
        """
        Возвращает список ID пользователей, которые лайкнули статью.

        Args:
            art_id: ID статьи

        Returns:
            Список user_id пользователей, которые лайкнули статью
        """
        likers = self.session.query(self.Likes.user_id).filter(
            self.Likes.article_id == self.art_id,
            self.Likes.is_active == True
        ).all()
        
        self.session.close()

        return [liker.user_id for liker in likers]

    def add_like_from_b24(self, created_at) -> bool:
        """
        Пользователь поставил лайк статье.
        Возвращает True, если лайк успешно добавлен, False если лайк уже существует.
        """
        # Проверяем, есть ли уже активный лайк
        existing_like = self.session.query(self.Likes).filter(
            self.Likes.user_id == self.user_id,
            self.Likes.article_id == self.art_id,
            self.Likes.is_active == True
        ).first()

        if existing_like:
            return False  # Лайк уже существует

        # Если лайк был, но is_active=False, обновляем его
        # inactive_like = self.session.query(Likes).filter(
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
        self.session.add(new_like)

        self.session.commit()
        self.session.close()
        return True

    # def has_liked_by_uuid(self): 
    #     user = self.session.query(User).filter(User.uuid == self.user_uuid).subquery()
    #     stmt = select(Likes.article_id).where(Likes.user_id == user.с.id)
    #     result = self.session.execute(stmt).fetchall()
    #     return [re for re in result]

    @classmethod
    def get_popular_articles(cls, limit: int = 10) -> List[Dict[str, int]]:
        """
        Возвращает список самых популярных статей по количеству лайков

        Args:
            session: SQLAlchemy сессия
            limit: Количество возвращаемых статей

        Returns:
            Список словарей с данными статей:               @self.session
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