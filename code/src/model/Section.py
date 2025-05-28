from src.base.B24 import B24
from src.base.pSQLmodels import SectionModel
from src.base.mongodb import FileModel
from src.services.LogsMaker import LogsMaker

from datetime import datetime

import json

from fastapi import APIRouter

section_router = APIRouter(prefix="/section", tags=["Разделы"])


class Section:
    def __init__(self, id=0, name="", parent_id=0):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def load(self):
        #загрузить из JSON
        section_data_file = open("./src/base/sections.json", "r")
        section_data = json.load(section_data_file)
        section_data_file.close()

        logg = LogsMaker()
        for _ in logg.progress(section_data, "Загрузка струтуры разделов сайта "):
            pass

        return SectionModel().upload(section_data)

    def get_all(self):
        section_data_file = open("./src/base/sections.json", "r")
        section_data = json.load(section_data_file)
        section_data_file.close()

        return section_data

    def find_by_id(self):
        return SectionModel(id = self.id).search_by_id()

    def find_by_parent_id(self):
        return SectionModel(parent_id = self.parent_id).search_by_parent_id()


#загрузить разделы из json файла
@section_router.put("")
def upload_sections():
    return Section().load()

#получить все разделы
@section_router.get("/all")
def get_all_sections():
    return Section().get_all()

#получить раздел по id
@section_router.get("/{ID}")
def get_section(ID):
    return Section(id = ID).find_by_id()

#получить подразделы раздела
@section_router.get("/subsection/{ID}")
def get_subsection(ID):
    return Section(parent_id = ID).find_by_parent_id()


