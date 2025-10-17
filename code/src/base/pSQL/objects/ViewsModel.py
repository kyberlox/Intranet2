from typing import Optional

from ..models.Views import Views
from .App import get_db #db

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Просмотров")

db_gen = get_db()
database = next(db_gen)

class ViewsModel:
    def __init__(self, views_count: Optional[int] = None, art_id: Optional[int] = None):
        # database = db
        self.views_count = views_count
        self.art_id = art_id
        self.Views = Views

    def add_view_b24(self ) -> None:
        """
        Добавляет запись о количестве просмотров статьи
        """

        existing_view = database.query(self.Views).where(self.Views.article_id == self.art_id).first()

        if existing_view:
            existing_view.viewes_count = self.views_count
        else:
            new_view = self.Views(
                article_id=self.art_id,
                viewes_count=self.views_count
            )
            database.add(new_view)

        database.commit()

        return {"msg": "добавили"}



    def get_art_viewes(self):
        """
        Возвращает количество просмотров у данной статьи
        """
        res = database.query(self.Views.viewes_count).where(
            self.Views.article_id == self.art_id
        ).scalar()

        return res
    
    def add_art_view(self):
        """
        Добавляет просмотр к статье и возвращает итоговое количество просмотров у статьи
        """
        existing_view = database.query(self.Views).where(self.Views.article_id == self.art_id).first()
        curr_count = 0
        if existing_view:
            existing_view.viewes_count = existing_view.viewes_count + 1
            curr_count = existing_view.viewes_count

            database.commit()

        else:
            new_view = self.Views()
            new_view.article_id=self.art_id,
            new_view.viewes_count=1
            curr_count = 1

            database.add(new_view)
            database.commit()


        return curr_count