from typing import Optional

from ..models.Views import Views
from .App import db

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Просмотров")

class ViewsModel:
    def __init__(self, views_count: Optional[int] = None, art_id: Optional[int] = None):
        self.session = db
        self.views_count = views_count
        self.art_id = art_id
        self.Views = Views

    def add_view_b24(self ) -> None:
        """
        Добавляет запись о количестве просмотров статьи
        """
        res = self.session.query(self.Views.viewes_count).where(
            self.Views.article_id == self.art_id
        ).scalar()
        print(res)
        existing_view = self.session.query(self.Views).where(self.Views.article_id == self.art_id).first()
        print(existing_view)
        # if existing_view:
        #     existing_view.viewes_count = self.views_count
        #     print()
        # else:
        #     new_view = self.Views(
        #         article_id=self.art_id,
        #         viewes_count=self.views_count
        #     )
        #     self.session.add(new_view)

        # self.session.commit()
        # self.session.close()
        # return {"msg": "добавили"}



    def get_art_viewes(self):
        """
        Возвращает количество просмотров у данной статьи
        """
        res = self.session.query(self.Views.viewes_count).where(
            self.Views.article_id == self.art_id
        ).scalar()
        self.session.close()
        return res
    
    def add_art_view(self):
        """
        Добавляет просмотр к статье и возвращает итоговое количество просмотров у статьи
        """
        existing_view = self.session.query(self.Views).where(self.Views.article_id == self.art_id).first()
        if existing_view:
            existing_view.viewes_count = existing_view.viewes_count + 1
            print(existing_view.viewes_count)
            self.session.commit()
            self.session.close()
            return {"views": existing_view.viewes_count}
        else:
            new_view = self.Views(
                article_id=self.art_id,
                viewes_count=1
            )
            self.session.add(new_view)
            self.session.commit()
            self.session.close()
            return {"views": new_view.viewes_count}