from src.B24 import B24
from src.pSQLmodels import SectionModel

import json



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

        return SectionModel().upload(section_data)



    def get_all(self):
        section_data_file = open("./src/sections.json", "r")
        section_data = json.load(section_data_file)
        section_data_file.close()

        return section_data

    def find_by_id(self):
        return SectionModel(id = self.id).search_by_id()

    def find_by_parent_id(self):
        return SectionModel(parent_id = self.parent_id).search_by_parent_id()