from fastapi import APIRouter

tag_router = APIRouter(prefix="/tags", tags=["Тэги"])

class Tag:
    def __init__(self, id: int = 0, tag_name: str = '', art_id: int = 0):
        self.id = id
        self.art_id = art_id
        self.tag_name = tag_name

        from ..base.pSQL.objects import TagsModel
        self.TagsModel = TagsModel()

    def add_tag(self):
        self.TagsModel.tag_name = self.tag_name
        return self.TagsModel.create_tag()

    def get_tag_by_id(self):
        ############################################
        # пусть возвращает True/False !!!!!!!!!!!!!#
        ############################################
        self.TagsModel.id = self.id
        return self.TagsModel.find_tag_by_id()

    def delete_tag(self):
        self.TagsModel.id = self.id
        return self.TagsModel.remove_tag()

    def add_b24_tag(self):
        self.TagsModel.id = self.id
        return self.TagsModel.create_b24_tag()
    
    def get_articles_by_tag_id(self, section_id):
        self.TagsModel.id = self.id
        return self.TagsModel.find_articles_by_tag_id(section_id=section_id)

    def get_all_tags(self):
        return self.TagsModel.all_tags()
    
    def set_tag_to_art_id(self):
        self.TagsModel.id = self.id
        self.TagsModel.art_id = self.art_id
        return self.TagsModel.set_tag_to_art_id()
    
    def remove_tag_from_art_id(self):
        self.TagsModel.id = self.id
        self.TagsModel.art_id = self.art_id
        return self.TagsModel.remove_tag_from_art_id()
    
    def get_art_tags(self):
        self.TagsModel.art_id = self.art_id
        return self.TagsModel.get_art_tags()


@tag_router.put("/upload_b24_tags")
def upload_b24_tags():
    return Tag().add_b24_tag()

@tag_router.get("/get_tags")
def get_tags():
    return Tag().get_all_tags()
    
@tag_router.put("/add_tag/{tag_name}")
def add_tag(tag_name: str):
    return Tag(tag_name=tag_name).add_tag()

@tag_router.delete("/delete_tag/{tag_id}")
def delete_tag(tag_id: int):
    return Tag(id=tag_id).delete_tag()

@tag_router.get("/get_art_tags/{art_id}")
def get_art_tags(art_id: int):
    return Tag(art_id=art_id).get_art_tags()