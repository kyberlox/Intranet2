from ..base.pSQL.objects.SectionModel import SectionModel
from ..base.pSQL.objects.SectionModel import SectionModel
from ..base.pSQL.objects.ArticleModel import ArticleModel
from ..services.LogsMaker import LogsMaker

from datetime import datetime

import json

import asyncio

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db
import aiofiles

section_router = APIRouter(prefix="/section", tags=["Разделы"])


class Section:
    def __init__(self, id=0, name="", parent_id=0, sectionHref=""):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.sectionHref = sectionHref

    async def load(self, session):
        #загрузить из JSON
        # section_data_file = open("./src/base/sections.json", "r")
        # section_data = json.load(section_data_file)
        # section_data_file.close()

        async with aiofiles.open("./src/base/sections.json", "r", encoding='utf-8') as file:
            section_data = json.loads(await file.read())

        logg = LogsMaker()
        for _ in logg.progress(section_data, "Загрузка струтуры разделов сайта "):
            pass
        res = await SectionModel().upload(section_data=section_data, session=session)
        return res

    async def get_all(self):
        # section_data_file = open("./src/base/sections.json", "r")
        # section_data = json.load(section_data_file)
        # section_data_file.close()
        async with aiofiles.open("./src/base/sections.json", "r", encoding='utf-8') as file:
            section_data = json.loads(await file.read())

        return section_data

    async def find_by_id(self, session):
        arts_info = await ArticleModel(section_id = self.id).find_by_section_id(session)
        arts_id = []
        for art in arts_info:
            art_id = art['id']
            arts_id.append(art_id)
        res = await SectionModel(id = self.id).search_by_id(session)
        res = res.__dict__
        res["arts_id"] = arts_id
        return res

    async def find_by_parent_id(self, session):
        return await SectionModel(parent_id = self.parent_id).search_by_parent_id(session)


#загрузить разделы из json файла
@section_router.put("")
async def upload_sections(session: AsyncSession=Depends(get_async_db)):
    return await Section().load(session)

#получить все разделы
@section_router.get("/all")
async def get_all_sections():
    return await Section().get_all()

#получить раздел по id
@section_router.get("/{ID}")
async def get_section(ID, session: AsyncSession=Depends(get_async_db)):
    return await Section(id = ID).find_by_id(session)

#получить подразделы раздела
@section_router.get("/subsection/{ID}")
async def get_subsection(ID, session: AsyncSession=Depends(get_async_db)):
    return await Section(parent_id = ID).find_by_parent_id(session)