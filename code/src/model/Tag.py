from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

import asyncio

tag_router = APIRouter(prefix="/tags", tags=["Тэги"])


class Tag:
    def __init__(self, id: int = 0, tag_name: str = '', art_id: int = 0):
        self.id = id
        self.art_id = art_id
        self.tag_name = tag_name

        from ..base.pSQL.objects import TagsModel
        self.TagsModel = TagsModel()

    async def add_tag(self, session):
        self.TagsModel.tag_name = self.tag_name
        return await self.TagsModel.create_tag(session)

    async def get_tag_by_id(self, session):
        ############################################
        # пусть возвращает True/False !!!!!!!!!!!!!#
        ############################################
        self.TagsModel.id = self.id
        return await self.TagsModel.find_tag_by_id(session)

    async def delete_tag(self, session):
        self.TagsModel.id = self.id
        return await self.TagsModel.remove_tag(session)

    async def add_b24_tag(self, session):
        self.TagsModel.id = self.id
        await self.TagsModel.create_b24_tag(session)
        return {"status": True}

    async def get_articles_by_tag_id(self, section_id, session):
        self.TagsModel.id = self.id
        return await self.TagsModel.find_articles_by_tag_id(section_id=section_id, session=session)

    async def get_all_tags(self, session):
        return await self.TagsModel.all_tags(session)

    async def set_tag_to_art_id(self, session):
        self.TagsModel.id = self.id
        self.TagsModel.art_id = self.art_id
        return await self.TagsModel.set_tag_to_art_id(session)

    async def remove_tag_from_art_id(self, session):
        self.TagsModel.id = self.id
        self.TagsModel.art_id = self.art_id
        return await self.TagsModel.remove_tag_from_art_id(session)

    async def get_art_tags(self, session):
        self.TagsModel.art_id = self.art_id
        return await self.TagsModel.get_art_tags(session)


@tag_router.put("/upload_b24_tags")
async def upload_b24_tags(session: AsyncSession = Depends(get_async_db)):
    return await Tag().add_b24_tag(session)


@tag_router.get("/get_tags")
async def get_tags(session: AsyncSession = Depends(get_async_db)):
    result = await Tag().get_all_tags(session)
    sorted_active_articles = sorted(result, key=lambda x: x['name'], reverse=False)
    return sorted_active_articles


@tag_router.put("/add_tag/{tag_name}")
async def add_tag(tag_name: str, session: AsyncSession = Depends(get_async_db)):
    return await Tag(tag_name=tag_name).add_tag(session)


@tag_router.delete("/delete_tag/{tag_id}")
async def delete_tag(tag_id: int, session: AsyncSession = Depends(get_async_db)):
    return await Tag(id=tag_id).delete_tag(session)


@tag_router.get("/get_art_tags/{art_id}")
async def get_art_tags(art_id: int, session: AsyncSession = Depends(get_async_db)):
    return await Tag(art_id=art_id).get_art_tags(session)