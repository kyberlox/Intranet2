from typing import Optional

from ..models.Views import Views
from .App import AsyncSessionLocal, select #db get_db, 

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Просмотров")

# db_gen = get_db()
# database = next(db_gen)

class ViewsModel:
    def __init__(self, views_count: Optional[int] = None, art_id: Optional[int] = None):
        # database = db
        self.views_count = views_count
        self.art_id = art_id
        self.Views = Views

    async def add_view_b24(self, session) -> None:
        """
        Добавляет запись о количестве просмотров статьи
        """
        # async with AsyncSessionLocal() as session:
        stmt = select(self.Views).where(self.Views.article_id == self.art_id)
        result = await session.execute(stmt)
        existing_view = result.scalar_one_or_none()
        # existing_view = database.query(self.Views).where(self.Views.article_id == self.art_id).first()

        if existing_view:
            existing_view.viewes_count = self.views_count
        else:
            new_view = self.Views(
                article_id=self.art_id,
                viewes_count=self.views_count
            )
            session.add(new_view)

        await session.commit()

        return {"msg": "добавили"}



    async def get_art_viewes(self, session):
        """
        Возвращает количество просмотров у данной статьи
        """
        # async with AsyncSessionLocal() as session:
        stmt = select(self.Views.viewes_count).where(self.Views.article_id == int(self.art_id))
        result = await session.execute(stmt)
        res = result.scalar()
        # res = database.query(self.Views.viewes_count).where(
        #     self.Views.article_id == self.art_id
        # ).scalar()

        return res
    
    async def add_art_view(self, session):
        """
        Добавляет просмотр к статье и возвращает итоговое количество просмотров у статьи
        """
        # async with AsyncSessionLocal() as session:
        stmt = select(self.Views).where(self.Views.article_id == int(self.art_id))
        result = await session.execute(stmt)
        existing_view = result.scalar_one_or_none()
    # existing_view = database.query(self.Views).where(self.Views.article_id == self.art_id).first()
        curr_count = 0
        if existing_view:
            existing_view.viewes_count = existing_view.viewes_count + 1
            curr_count = existing_view.viewes_count

            await session.commit()

        else:
            new_view = self.Views(
                article_id=self.art_id,
                viewes_count=1
            )
            # new_view.article_id=self.art_id,
            # new_view.viewes_count=1
            curr_count = 1
            # print(new_view.__dict__)
            session.add(new_view)
            await session.commit()


        return curr_count