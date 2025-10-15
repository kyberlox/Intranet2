import json

from ..models.Tags import Tags
from ..models.Article import Article
from .App import get_db, flag_modified



from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Тэгов")

db_gen = get_db()
database = next(db_gen)

class TagsModel:
    def __init__(self, id: int = 0, tag_name: str = '', art_id: int = 0):
        # database = db
        self.id = id
        self.tag_name = tag_name
        self.art_id = art_id
        
        self.Tags = Tags
        self.Article = Article
        

    def create_tag(self):
        existing_tag = database.query(self.Tags).filter(self.Tags.tag_name == self.tag_name).first()
        if existing_tag:
            return {"msg": "Такой тэг уже существует"}
        new_tag = self.Tags(tag_name=self.tag_name)
        database.add(new_tag)
        database.commit()

        return {"msg": "Добавлен"}
    
    def find_tag_by_id(self):
        existing_tag = database.query(self.Tags).filter(self.Tags.id == self.id).first()
        if existing_tag:
            database.close()
            return existing_tag


    def remove_tag(self):
        try:
            existing_tag = database.query(self.Tags).filter(self.Tags.id == self.id).first()
            if existing_tag:
                articles = database.query(self.Article).filter(self.Article.indirect_data["tags"].contains([self.id])).all()
                for art in articles:
                    art.indirect_data["tags"].remove(self.id)
                    flag_modified(art, "indirect_data")
                    database.commit()
                database.query(self.Tags).filter(self.Tags.id == self.id).delete()
                database.commit()
                return LogsMaker().info_message(f"Тэг с id = {self.id} удален из статей")
            return LogsMaker().info_message(f"Тэг с id = {self.id} не существует")
        except Exception as e:
            database.rollback()
            return LogsMaker().error_message(f"Произошла ошибка при удалении тэга с id = {self.id} из статей, {e}")
    
    def create_b24_tag(self):
        with open('./src/base/current_tags.json', mode='r', encoding='UTF-8') as f:
            cur_tags = json.load(f)
        for tag in cur_tags:
            existing_tag = database.query(self.Tags).filter(self.Tags.id == tag['id']).first()
            if existing_tag:
                continue
            else:
                new_tag = self.Tags(id=tag['id'], tag_name=tag['name'])
                database.add(new_tag)
                database.commit()

        return {"msg": "Добавлены"}
    
    def find_articles_by_tag_id(self, section_id : int):
        articles = database.query(self.Article).filter(self.Article.indirect_data["tags"].contains([self.id]), self.Article.active == True, self.Article.section_id == section_id).all()

        if articles:
            return articles
        return []
    
    def all_tags(self):
        tags = database.query(self.Tags).all()
        if tags:
            return tags
        return []

    def set_tag_to_art_id(self):
        try:
            existing_tag = database.query(self.Tags).filter(self.Tags.id == self.id).first()
            existing_art = database.query(self.Article).filter(self.Article.id == self.art_id).first()
            if not existing_tag:
                return LogsMaker().info_message(f"Тэга с id = {self.id} не существует")
            
            if not existing_art:
                return LogsMaker().info_message(f"Статьи с id = {self.art_id} не существует")
            
            if existing_art.indirect_data is not None and "tags" in existing_art.indirect_data:
                existing_art.indirect_data["tags"].append(self.id)
                flag_modified(existing_art, 'indirect_data')
                database.commit()
                return LogsMaker().info_message(f"Тэг с id = {self.id} успешно привязан к статье с id = {self.art_id}")
            return LogsMaker().info_message(f"Тэг с id = {self.id} не был привязан к статье с id = {self.art_id}, поле indirect_data не валдино")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при привязке тэга с id = {self.id} к статье с id = {self.art_id}, {e}")
    
    def remove_tag_from_art_id(self):
        try:
            existing_tag_in_art = database.query(self.Article).filter(
                self.Article.id == self.art_id,
                self.Article.indirect_data["tags"].contains([self.id])
            ).first()

            if not existing_tag_in_art:
                return LogsMaker().info_message(f"К статье с id = {self.art_id} не привязан тэг с id = {self.id}")
            
            existing_tag_in_art.indirect_data['tags'].remove(self.id)
            flag_modified(existing_tag_in_art, 'indirect_data')
            database.commit()
            return LogsMaker().info_message(f"Тэг с id = {self.id} успешно отвязан от статьи с id = {self.art_id}")
        except Exception as e:
            return LogsMaker().error_message(f"Ошибка при отвязке тэга с id = {self.id} от статьи с id = {self.art_id}, {e}")
    
    def get_art_tags(self):
        article = database.query(self.Article.indirect_data["tags"]).filter(self.Article.id == self.art_id).first()
        if article:
            # print(article)
            return article[0]
        return None