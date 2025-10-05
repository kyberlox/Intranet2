from ..models.Section import Section
from .App import get_db


from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Разделов")

db_gen = get_db()
database = next(db_gen)

class SectionModel:

    def __init__(self, id=0, name="", parent_id=0):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        # database = db
        self.Section = Section

    def upload(self, section_data):
        for section in section_data:
            sec = database.query(Section).filter(self.Section.id == section["id"]).first()

            if sec is not None:
                #надо ли обновить?
                if sec.name != section["name"]:
                   sec.name = section["name"]
                if sec.parent_id != section["parent_id"]:
                    sec.parent_id = section["parent_id"]
                if "sectionHref" in section and sec.sectionHref != section["sectionHref"]:
                    sec.sectionHref = section["sectionHref"]
            else:
                if "sectionHref" in section:
                    sec = self.Section(id=section["id"], name=section["name"], parent_id=section["parent_id"], sectionHref=section["sectionHref"])
                else:
                    sec = self.Section(id=section["id"], name=section["name"], parent_id=section["parent_id"])
            database.add(sec)
            database.commit()

        return section_data

    def search_by_id(self):
        result = database.query(Section).filter(self.Section.id == self.id).first()
        return result

    def search_by_parent_id(self):
        result = database.query(Section).filter(self.Section.parent_id == self.parent_id).all()
        return result