from .models import Section
from .App import db

#!!!!!!!!!!!!!!!
from services import LogsMaker
#!!!!!!!!!!!!!!!

class SectionModel():

    def __init__(self, id=0, name="", parent_id=0):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.db = db

    def upload(self, section_data):
        for section in section_data:
            sec = self.db.query(Section).filter(Section.id == section["id"]).first()

            if sec is not None:
                #надо ли обновить?
                if sec.name != section["name"]:
                   sec.name = section["name"]
                if sec.parent_id != section["parent_id"]:
                    sec.parent_id = section["parent_id"]
            else:
                sec = Section(id=section["id"], name=section["name"], parent_id=section["parent_id"])
            self.db.add(sec)
            self.db.commit()
            self.db.close()

        return section_data

    def search_by_id(self):
        result = self.db.query(Section).filter(Section.id == self.id).first()
        self.db.close()
        return result

    def search_by_parent_id(self):
        result = self.db.query(Section).filter(Section.parent_id == self.parent_id).all()
        self.db.close()
        return self.close()