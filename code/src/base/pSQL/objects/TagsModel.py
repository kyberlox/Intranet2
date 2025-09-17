import json

from ..models.Tags import Tags
from ..models.Article import Article
from .App import db




#!!!!!!!!!!!!!!!
from ....services.LogsMaker import LogsMaker
#!!!!!!!!!!!!!!!

class TagsModel:
    def __init__(self, id: int = 0, tag_name: str = ''):
        self.session = db
        self.id = id
        self.tag_name = tag_name
        
        self.Tags = Tags
        self.Article = Article
        

    def create_tag(self):
        existing_tag = self.session.query(self.Tags).filter(self.Tags.tag_name == self.tag_name).first()
        if existing_tag:
            return {"msg": "Такой тэг уже существует"}
        new_tag = self.Tags(tag_name=self.tag_name)
        self.session.add(new_tag)
        self.session.commit()
        self.session.close()
        return {"msg": "Добавлен"}
    
    def find_tag_by_id(self):
        existing_tag = self.session.query(self.Tags).filter(self.Tags.id == self.id).first()
        if existing_tag:
            self.session.close()
            return existing_tag
        self.session.close()

    def remove_tag(self):
        existing_tag = self.session.query(self.Tags).filter(self.Tags.id == self.id).first()
        if existing_tag:
            self.session.query(self.Tags).filter(self.Tags.id == self.id).delete()
            self.session.commit()
            self.session.close()
            
            return {"msg": "удален"}
        
        self.session.close()
        
        return {"msg": "отсутствует такой тэг"}
    
    def create_b24_tag(self):
        with open('./src/base/current_tags.json', mode='r', encoding='UTF-8') as f:
            cur_tags = json.load(f)
        for tag in cur_tags:
            existing_tag = self.session.query(self.Tags).filter(self.Tags.id == tag['id']).first()
            if existing_tag:
                continue
            else:
                new_tag = self.Tags(id=tag['id'], tag_name=tag['name'])
                self.session.add(new_tag)
                self.session.commit()
        self.session.close()
        return {"msg": "Добавлены"}
    
    def find_articles_by_tag_id(self, section_id : int):
        articles = self.session.query(self.Article).filter(self.Article.indirect_data["tags"].contains([self.id]), self.Article.active == True, self.Article.section_id == section_id).all()
        self.session.close()
        if articles:
            return articles
        return []
    
    def all_tags(self):
        tags = self.session.query(self.Tags).all()
        self.session.close()
        if tags:
            return tags
        return []