from ..models.Section import Section

from .App import select


from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Разделов")



class SectionModel:

    def __init__(self, id=0, name="", parent_id=0):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        # database = db
        self.Section = Section


    async def upload(self, section_data, session):
        for section in section_data:
            res = await session.execute(select(self.Section).where(self.Section.id == int(section["id"])))
            sec = res.scalar_one_or_none()
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

            session.add(sec)
        await session.commit()

        return section_data

    async def search_by_id(self, session):
        result = await session.query(Section).filter(self.Section.id == self.id)
        return result.first()

    async def search_by_parent_id(self, session):
        result = await session.query(Section).filter(self.Section.parent_id == self.parent_id)
        return result.all()
