from src.base.pSQLmodels import TagsModel

from fastapi import APIRouter

tag_router = APIRouter(prefix="/tags", tags=["Тэги"])

class Tag:
    def __init__(self, id: int = 0, tag_name: str = ''):
        self.id = id
        self.tag_name = tag_name

    def add_tag(self):
        return TagsModel(tag_name=self.tag_name).create_tag()

    def get_tag_by_id(self):
        ############################################
        # пусть возвращает True/False !!!!!!!!!!!!!#
        ############################################
        return TagsModel(id=self.id).find_tag_by_id()

    def delete_tag(self):
        return TagsModel(id=self.id).remove_tag()

    def add_b24_tag(self):
        return TagsModel().create_b24_tag()
    
    def get_articles_by_tag_id(self, section_id):
        return TagsModel(id=self.id).find_articles_by_tag_id(section_id)

    def get_all_tags(self):
        return TagsModel().all_tags()

@tag_router.put("/upload_b24_tags")
def upload_b24_tags():
    return Tag().add_b24_tag()

@tag_router.get("/get_tags")
def get_tags():
    return Tag().get_all_tags()
    
@tag_router.put("/add_tag/{tag_name}")
def add_tag(tag_name: str):
    return Tag(tag_name=tag_name).add_tag()
