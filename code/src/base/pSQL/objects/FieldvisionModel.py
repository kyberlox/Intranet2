from src.services.LogsMaker import LogsMaker

from .App import func, select #get_db, 
LogsMaker().ready_status_message("Успешная инициализация таблицы Области Видимости")

import asyncio

class FieldvisionModel:
    def __init__(self, vision_name: str = '', id: int = 0, art_id: int = 0):
        # from .App import db
        # database = db
        self.vision_name = vision_name
        self.id = id
        self.art_id = art_id

        from ..models.Fieldvision import Fieldvision
        self.Fieldvision = Fieldvision

        from ..models.ArtVis import ArtVis
        self.ArtVis = ArtVis

        from ..models.Article import Article
        self.Article = Article

    async def add_field_vision(self, session):
        try:
            # Проверяем существование vision с таким именем
            stmt = select(self.Fieldvision).where(self.Fieldvision.vision_name == self.vision_name)
            result = await session.execute(stmt)
            existing_vision = result.scalar_one_or_none()
            
            if existing_vision:
                return LogsMaker().info_message(f"Области видимости с id = {self.id} уже существует")
            
            # Находим максимальный ID
            stmt = select(func.max(self.Fieldvision.id))
            result = await session.execute(stmt)
            max_id = result.scalar() or 0
            new_id = max_id + 1
            
            # Создаем новую запись
            new_vision = self.Fieldvision(id=new_id, vision_name=self.vision_name)
            session.add(new_vision)
            await session.commit()
            
            # Возвращаем созданную запись
            stmt = select(self.Fieldvision).where(self.Fieldvision.vision_name == self.vision_name)
            result = await session.execute(stmt)
            return result.scalar_one()
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка при создании области видимости: {e}")

    async def remove_field_vision(self, session):
        try:
            stmt = select(self.Fieldvision).where(self.Fieldvision.id == self.id)
            result = await session.execute(stmt)
            existing_vision = result.scalar_one_or_none()
            
            if existing_vision:
                await session.delete(existing_vision)
                await session.commit()
                return LogsMaker().info_message(f"Удалена область видимости с id= {self.id}")
            
            return LogsMaker().info_message(f"Области видимости с id = {self.id} уже существует")
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка при удалении области видимостис id = {self.id}: {e}")

    async def find_vision_by_id(self, session):
        stmt = select(self.Fieldvision).where(self.Fieldvision.id == self.id)
        result = await session.execute(stmt)
        existing_vision = result.scalar_one_or_none()
        
        if existing_vision:
            return existing_vision
        return LogsMaker().info_message(f"Области видимости с id = {self.id} уже существует")

    async def find_all_visions(self, session):
        stmt = select(self.Fieldvision)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def set_art_to_vision(self, session):
        try:
            # Проверяем существование области видимости
            stmt_vision = select(self.Fieldvision).where(self.Fieldvision.id == self.id)
            result_vision = await session.execute(stmt_vision)
            existing_vision = result_vision.scalar_one_or_none()
            
            if not existing_vision:
                return LogsMaker().info_message(f"Области видимости с id = {self.id} не существует")
            
            # Проверяем существование статьи
            stmt_art = select(self.Article).where(self.Article.id == self.art_id)
            result_art = await session.execute(stmt_art)
            existing_art = result_art.scalar_one_or_none()
            
            if not existing_art:
                return LogsMaker().info_message(f"Статью с id = {self.art_id} невозможно добавить в ОВ с id = {self.id}, статьи не существует")

            # Проверяем, не существует ли уже такая связь
            stmt_existing = select(self.ArtVis).where(
                self.ArtVis.vision_id == self.id,
                self.ArtVis.art_id == self.art_id
            )
            result_existing = await session.execute(stmt_existing)
            existing_link = result_existing.scalar_one_or_none()
            
            if existing_link:
                return LogsMaker().info_message(f"Связь уже существует Статьи с id = {self.art_id} с в ОВ с id = {self.id}")

            # Находим максимальный ID
            stmt_max = select(func.max(self.ArtVis.id))
            result_max = await session.execute(stmt_max)
            max_id = result_max.scalar() or 0
            new_id = max_id + 1
            
            # Создаем новую связь
            new_node = self.ArtVis(
                id=new_id,
                vision_id=self.id,
                art_id=self.art_id
            )
            session.add(new_node)
            await session.commit()
            
            return LogsMaker().info_message(f"Статья с id = {self.art_id} успешно добавлена в ОВ с id = {self.id}")
            
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка при добавлении статьи с id = {self.art_id} в ОВ с id = {self.id}, {e}")

    async def delete_art_from_vision(self, session):
        try:
            # Проверяем существование области видимости
            stmt_vision = select(self.Fieldvision).where(self.Fieldvision.id == self.id)
            result_vision = await session.execute(stmt_vision)
            existing_vision = result_vision.scalar_one_or_none()
            
            if not existing_vision:
                return LogsMaker().info_message(f"Области видимости с id = {self.id} не существует")
            
            # Проверяем существование статьи
            stmt_art = select(self.Article).where(self.Article.id == self.art_id)
            result_art = await session.execute(stmt_art)
            existing_art = result_art.scalar_one_or_none()
            
            if not existing_art:
                return LogsMaker().info_message(f"Статью с id = {self.art_id} невозможно удалить из ОВ с id = {self.id}, статьи не существует")

            # Находим и удаляем связь
            stmt_link = select(self.ArtVis).where(
                self.ArtVis.art_id == self.art_id,
                self.ArtVis.vision_id == self.id
            )
            result_link = await session.execute(stmt_link)
            existing_link = result_link.scalar_one_or_none()
            
            if existing_link:
                await session.delete(existing_link)
                await session.commit()
                return LogsMaker().info_message(f"Статья с id = {self.art_id} успешно удалена из ОВ с id = {self.id}")
            else:
                return LogsMaker().info_message(f"Связь Статьи с id = {self.art_id} с в ОВ с id = {self.id} не найдена")
                
        except Exception as e:
            await session.rollback()
            return LogsMaker().error_message(f"Ошибка при удалении статьи с id = {self.art_id} из ОВ с id = {self.id}, {e}")

    async def get_all_vis_in_art(self, session):
        result = []
        stmt = select(
            self.ArtVis.vision_id,
            self.Fieldvision.vision_name
        ).join(
            self.Fieldvision, 
            self.Fieldvision.id == self.ArtVis.vision_id
        ).where(
            self.ArtVis.art_id == self.art_id
        )
        
        query_result = await session.execute(stmt)
        art_info = query_result.all()
        

        if art_info:
            for art in art_info:
                vis_info = {
                    "id": art[0],
                    "name": art[1]
                }
                result.append(vis_info)
        return result


    async def check_user_root(self, session, user_id: int):
        from ..models.Roots import Roots
        self.Roots = Roots

        try:
            # Получаем корни пользователя
            stmt_roots = select(self.Roots.root_token['VisionRoots']).where(self.Roots.user_uuid == user_id)
            result_roots = await session.execute(stmt_roots)
            user_roots = result_roots.scalar_one_or_none()

            # Получаем vision_id для статьи
            stmt_art_vis = select(self.ArtVis.vision_id).where(self.ArtVis.art_id == self.art_id)
            result_art_vis = await session.execute(stmt_art_vis)
            art_vis = result_art_vis.scalars().all()

            if user_roots is not None and art_vis:
                for user_root in user_roots:
                    if user_root in art_vis:
                        return True
            return False
            
        except Exception as e:
            # Логируем ошибку, если нужно
            return False
 