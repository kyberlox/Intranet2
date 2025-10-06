import json

from ..models.Tags import Tags
from ..models.Article import Article
from .App import get_db



from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Тэгов")

db_gen = get_db()
database = next(db_gen)

class TagsModel:
    def __init__(self, id: int = 0, tag_name: str = ''):
        # database = db
        self.id = id
        self.tag_name = tag_name
        
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
        existing_tag = database.query(self.Tags).filter(self.Tags.id == self.id).first()
        if existing_tag:
            database.query(self.Tags).filter(self.Tags.id == self.id).delete()
            database.commit()
            database.close()
            
            return {"msg": "удален"}
        

        
        return {"msg": "отсутствует такой тэг"}
    
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