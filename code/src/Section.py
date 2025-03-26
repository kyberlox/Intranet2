from src.B24 import B24
import json

from sqlalchemy import create_engine, Column, Integer, Text, Boolean, String, DateTime, JSON, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=True, bind=engine)
db = SessionLocal()

class Section:
    def __init__(self, id=0, name="", parent_id=0):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def load(self):
        #загрузить из JSON
        section_data_file = open("./src/sections.json", "r")
        section_data = json.load(section_data_file)
        section_data_file.close()

        for section in section_data:
            sec = db.query(SectionDB).filter(SectionDB.id == section["id"]).first()

            if sec is not None:
                #надо ли обновить?
                if sec.name != section["name"]:
                   sec.name = section["name"]
                if sec.parent_id != section["parent_id"]:
                    sec.parent_id = section["parent_id"]
            else:
                sec = SectionDB(id=section["id"], name=section["name"], parent_id=section["parent_id"])
            db.add(sec)
            db.commit()

        return section_data

    def get_all(self):
        section_data_file = open("./src/sections.json", "r")
        section_data = json.load(section_data_file)
        section_data_file.close()
        return section_data

    def find_by_id(self):
        return db.query(SectionDB).filter(SectionDB.id == self.id).first()

    def find_by_parent_id(self):
        return db.query(SectionDB).filter(SectionDB.parent_id == self.parent_id).all()