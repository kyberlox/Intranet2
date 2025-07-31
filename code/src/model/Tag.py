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
        return TagsModel(id=self.id).find_tag_by_id()

    def delete_tag(self):
        return TagsModel(id=self.id).remove_tag()

    def add_b24_tag(self):
        return TagsModel(id=self.id, tag_name=self.tag_name).create_b24_tag()
    
    def get_articles_by_tag_id(self):
        return TagsModel(id=self.id).find_articles_by_tag_id()


@tag_router.put("/upload_b24_tags/{id}/{tag_name}")
def upload_b24_tags(id: int, tag_name: str):
    return Tag(id=id, tag_name=tag_name).add_b24_tag()