import json

from ..models.Tags import Tags
from ..models.Article import Article
from .App import flag_modified, select, delete

import asyncio

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Тэгов")

# db_gen = get_db()
# database = next(db_gen) get_db, 

class TagsModel:
    def __init__(self, id: int = 0, tag_name: str = '', art_id: int = 0):
        # database = db
        self.id = id
        self.tag_name = tag_name
        self.art_id = art_id
        
        self.Tags = Tags
        self.Article = Article
    
    async def create_tag(self, session):
        """Создание нового тега"""
        try:
            stmt = select(self.Tags).where(self.Tags.tag_name == self.tag_name)
            result = await session.execute(stmt)
            existing_tag = result.scalar_one_or_none()
            
            if existing_tag:
                return {"msg": "Такой тэг уже существует"}
                
            new_tag = self.Tags(tag_name=self.tag_name)
            session.add(new_tag)
            await session.commit()
            
            return {"msg": "Добавлен"}
            
        except Exception as e:
            # await session.rollback()
            return LogsMaker().error_message(f"Ошибка создания тега: {str(e)}")
            # return {"msg": f"Ошибка: {str(e)}"}

    async def find_tag_by_id(self, session):
        """Поиск тега по ID"""
        try:
            stmt = select(self.Tags).where(self.Tags.id == self.id)
            result = await session.execute(stmt)
            existing_tag = result.scalar_one_or_none()
            
            if existing_tag:
                return existing_tag
            return None
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка поиска тега: {str(e)}")
            # return None

    async def remove_tag(self, session):
        """Удаление тега"""
        try:
            stmt = select(self.Tags).where(self.Tags.id == self.id)
            result = await session.execute(stmt)
            existing_tag = result.scalar_one_or_none()
            
            if not existing_tag:
                return LogsMaker().info_message(f"Тэг с id = {self.id} не существует")
          
            articles_stmt = select(self.Article).where(
                self.Article.indirect_data["tags"].contains([self.id])
            )
            articles_result = await session.execute(articles_stmt)
            articles = articles_result.scalars().all()
            
            # Удаляем тег из статей
            for art in articles:
                if "tags" in art.indirect_data and self.id in art.indirect_data["tags"]:
                    art.indirect_data["tags"].remove(self.id)
                    flag_modified(art, "indirect_data")
            
            # Удаляем сам тег
            await session.delete(existing_tag)
            await session.commit()
            
            return LogsMaker().info_message(f"Тэг с id = {self.id} удален из {len(articles)} статей")
            # return {"msg": f"Тэг удален из {len(articles)} статей"}
            
        except Exception as e:
            # await session.rollback()
            return LogsMaker().error_message(f"Ошибка удаления тега: {str(e)}")
            # return {"msg": f"Ошибка: {str(e)}"}

    async def create_b24_tag(self, session):
        """Создание тегов из Bitrix24"""
        try:
            import aiofiles
            import json
            
            async with aiofiles.open('./src/base/current_tags.json', mode='r', encoding='UTF-8') as f:
                content = await f.read()
                cur_tags = json.loads(content)
                
            added_count = 0
            for tag in cur_tags:
                stmt = select(self.Tags).where(self.Tags.id == tag['id'])
                result = await session.execute(stmt)
                existing_tag = result.scalar_one_or_none()
                
                if not existing_tag:
                    new_tag = self.Tags(id=tag['id'], tag_name=tag['name'])
                    session.add(new_tag)
                    added_count += 1
            
            await session.commit()
            return {"msg": f"Добавлено {added_count} тегов"}
            
        except Exception as e:
            # await session.rollback()
            return LogsMaker().error_message(f"Ошибка создания тегов B24: {str(e)}")
            # return {"msg": f"Ошибка: {str(e)}"}

    async def find_articles_by_tag_id(self, section_id: int, session):
        """Поиск статей по ID тега и section_id"""
        try:
            stmt = select(self.Article).where(
                self.Article.indirect_data["tags"].contains([self.id]),
                self.Article.active == True,
                self.Article.section_id == section_id
            )
            result = await session.execute(stmt)
            articles = result.scalars().all()
            
            return articles if articles else []
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка поиска статей по тегу: {str(e)}")
            # return []

    async def all_tags(self, session):
        """Получение всех тегов"""
        try:
            stmt = select(self.Tags)
            result = await session.execute(stmt)
            tags = result.scalars().all()
            
            # Если нужно преобразовать теги
            # tag_list = []
            # for tag in tags:
            #     tag_dict = {
            #         "id": tag.id,
            #         "name": tag.tag_name
            #     }
            #     tag_list.append(tag_dict)
            # return tag_list
            
            return tags if tags else []
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка получения тегов: {str(e)}")
            # return []

    async def set_tag_to_art_id(self, session):
        """Привязка тега к статье"""
        try:
            # Проверяем существование тега
            tag_stmt = select(self.Tags).where(self.Tags.id == self.id)
            tag_result = await session.execute(tag_stmt)
            existing_tag = tag_result.scalar_one_or_none()
            
            if not existing_tag:
                return LogsMaker().info_message(f"Тэга с id = {self.id} не существует")
                # return {"msg": f"Тэга с id = {self.id} не существует"}
            
            # Проверяем существование статьи
            art_stmt = select(self.Article).where(self.Article.id == self.art_id)
            art_result = await session.execute(art_stmt)
            existing_art = art_result.scalar_one_or_none()
            
            if not existing_art:
                return LogsMaker().info_message(f"Статьи с id = {self.art_id} не существует")
                # return {"msg": f"Статьи с id = {self.art_id} не существует"}
            
            # Привязываем тег
            if existing_art.indirect_data is None:
                existing_art.indirect_data = {}
            
            if "tags" not in existing_art.indirect_data:
                existing_art.indirect_data["tags"] = []
            
            if self.id not in existing_art.indirect_data["tags"]:
                existing_art.indirect_data["tags"].append(self.id)
                flag_modified(existing_art, 'indirect_data')
                await session.commit()
                return LogsMaker().info_message(f"Тэг с id = {self.id} успешно привязан к статье с id = {self.art_id}")
                # return {"msg": "Тэг успешно привязан"}
            else:
                return LogsMaker().info_message(f"Тэг с id = {self.id} уже привязан к статье с id = {self.art_id}")
                # return {"msg": "Тэг уже привязан"}
                
        except Exception as e:
            # await session.rollback()
            return LogsMaker().error_message(f"Ошибка привязки тега: {str(e)}")
            # return {"msg": f"Ошибка: {str(e)}"}

    async def remove_tag_from_art_id(self, session):
        """Отвязка тега от статьи"""
        try:
            stmt = select(self.Article).where(
                self.Article.id == self.art_id,
                self.Article.indirect_data["tags"].contains([self.id])
            )
            result = await session.execute(stmt)
            existing_tag_in_art = result.scalar_one_or_none()

            if not existing_tag_in_art:
                return LogsMaker().info_message(f"К статье с id = {self.art_id} не привязан тэг с id = {self.id}")
                # return {"msg": "Тэг не привязан к статье"}
            
            if "tags" in existing_tag_in_art.indirect_data and self.id in existing_tag_in_art.indirect_data["tags"]:
                existing_tag_in_art.indirect_data['tags'].remove(self.id)
                flag_modified(existing_tag_in_art, 'indirect_data')
                await session.commit()
                # return LogsMaker().info_message(f"Тэг с id = {self.id} успешно отвязан от статьи с id = {self.art_id}")
                # return {"msg": "Тэг успешно отвязан"}
            else:
                return LogsMaker().info_message(f"Тэг с id = {self.id} не найден в статье с id = {self.art_id}")
                # return {"msg": "Тэг не найден в статье"}
                
        except Exception as e:
            # await session.rollback()
            return LogsMaker().error_message(f"Ошибка отвязки тега: {str(e)}")
            # return {"msg": f"Ошибка: {str(e)}"}

    async def get_art_tags(self, session):
        """Получение тегов статьи"""
        try:
            stmt = select(self.Article.indirect_data["tags"]).where(self.Article.id == self.art_id)
            result = await session.execute(stmt)
            article_tags = result.scalar_one_or_none()
            
            return article_tags if article_tags else []
            
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка получения тегов статьи: {str(e)}")
            # return []

    # def create_tag(self, session):
    #     existing_tag = database.query(self.Tags).filter(self.Tags.tag_name == self.tag_name).first()
    #     if existing_tag:
    #         return {"msg": "Такой тэг уже существует"}
    #     new_tag = self.Tags(tag_name=self.tag_name)
    #     database.add(new_tag)
    #     database.commit()

    #     return {"msg": "Добавлен"}
    
    # def find_tag_by_id(self, session):
    #     existing_tag = database.query(self.Tags).filter(self.Tags.id == self.id).first()
    #     if existing_tag:
    #         database.close()
    #         return existing_tag


    # def remove_tag(self, session):
    #     try:
    #         existing_tag = database.query(self.Tags).filter(self.Tags.id == self.id).first()
    #         if existing_tag:
    #             articles = database.query(self.Article).filter(self.Article.indirect_data["tags"].contains([self.id])).all()
    #             for art in articles:
    #                 art.indirect_data["tags"].remove(self.id)
    #                 flag_modified(art, "indirect_data")
    #                 database.commit()
    #             database.query(self.Tags).filter(self.Tags.id == self.id).delete()
    #             database.commit()
    #             return LogsMaker().info_message(f"Тэг с id = {self.id} удален из статей")
    #         return LogsMaker().info_message(f"Тэг с id = {self.id} не существует")
    #     except Exception as e:
    #         database.rollback()
    #         return LogsMaker().error_message(f"Произошла ошибка при удалении тэга с id = {self.id} из статей, {e}")
    
    # def create_b24_tag(self, session):
    #     with open('./src/base/current_tags.json', mode='r', encoding='UTF-8') as f:
    #         cur_tags = json.load(f)
    #     for tag in cur_tags:
    #         existing_tag = database.query(self.Tags).filter(self.Tags.id == tag['id']).first()
    #         if existing_tag:
    #             continue
    #         else:
    #             new_tag = self.Tags(id=tag['id'], tag_name=tag['name'])
    #             database.add(new_tag)
    #             database.commit()

    #     return {"msg": "Добавлены"}
    
    # def find_articles_by_tag_id(self, section_id : int, session):
    #     articles = database.query(self.Article).filter(self.Article.indirect_data["tags"].contains([self.id]), self.Article.active == True, self.Article.section_id == section_id).all()

    #     if articles:
    #         return articles
    #     return []
    
    # def all_tags(self, session):
    #     tags = database.query(self.Tags).all()
    #     if tags:
    #         # for tag in tags:
    #         #     tag = tag.__dict__
    #         #     tag['name'] = tag['tag_name']
    #         #     tag.pop('tag_name')
    #         return tags
            
    #     return []

    # def set_tag_to_art_id(self, session):
    #     try:
    #         existing_tag = database.query(self.Tags).filter(self.Tags.id == self.id).first()
    #         existing_art = database.query(self.Article).filter(self.Article.id == self.art_id).first()
    #         if not existing_tag:
    #             return LogsMaker().info_message(f"Тэга с id = {self.id} не существует")
            
    #         if not existing_art:
    #             return LogsMaker().info_message(f"Статьи с id = {self.art_id} не существует")
            
    #         if existing_art.indirect_data is not None and "tags" in existing_art.indirect_data:
    #             existing_art.indirect_data["tags"].append(self.id)
    #             flag_modified(existing_art, 'indirect_data')
    #             database.commit()
    #             return LogsMaker().info_message(f"Тэг с id = {self.id} успешно привязан к статье с id = {self.art_id}")
    #         return LogsMaker().info_message(f"Тэг с id = {self.id} не был привязан к статье с id = {self.art_id}, поле indirect_data не валдино")
    #     except Exception as e:
    #         return LogsMaker().error_message(f"Ошибка при привязке тэга с id = {self.id} к статье с id = {self.art_id}, {e}")
    
    # def remove_tag_from_art_id(self, session):
    #     try:
    #         existing_tag_in_art = database.query(self.Article).filter(
    #             self.Article.id == self.art_id,
    #             self.Article.indirect_data["tags"].contains([self.id])
    #         ).first()

    #         if not existing_tag_in_art:
    #             return LogsMaker().info_message(f"К статье с id = {self.art_id} не привязан тэг с id = {self.id}")
            
    #         existing_tag_in_art.indirect_data['tags'].remove(self.id)
    #         flag_modified(existing_tag_in_art, 'indirect_data')
    #         database.commit()
    #         return LogsMaker().info_message(f"Тэг с id = {self.id} успешно отвязан от статьи с id = {self.art_id}")
    #     except Exception as e:
    #         return LogsMaker().error_message(f"Ошибка при отвязке тэга с id = {self.id} от статьи с id = {self.art_id}, {e}")
    
    # def get_art_tags(self, session):
    #     article = database.query(self.Article.indirect_data["tags"]).filter(self.Article.id == self.art_id).first()
    #     if article:
    #         # print(article)
    #         return article[0]
    #     return None