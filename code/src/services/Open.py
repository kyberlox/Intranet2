from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header

from ..base.pSQL.objects.ArticleModel import ArticleModel
from ..model.File import File
from .LogsMaker import LogsMaker

import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..base.pSQL.objects.App import get_async_db


open_router = APIRouter(prefix="/open")

@open_router.get("/career", tags=["Открытая ссылка", "ЭМК Карьера"])
async def career(session: AsyncSession = Depends(get_async_db)):
    # получить все статьи раздела
    active_articles = []
    result = await ArticleModel(section_id=int(51)).find_by_section_id(session)
    for res in result:
        if res['active']:
            active_articles.append(res)
    
    try:
        sorted_active_articles = sorted(active_articles, key=lambda x: x['date_publiction'], reverse=True)
    except:
        sorted_active_articles = sorted(active_articles, key=lambda x: x['date_creation'], reverse=True)

    # собрать данные каждой статьи
    arts_info = []
    for article in sorted_active_articles:
        art_id = article["id"]
        art = await ArticleModel(id=self.id).find_by_id(session)
        files = await File(art_id=int(self.id)).get_files_by_art_id(session)
        art['images'] = []
        art['videos_native'] = []
        art['videos_embed'] = []
        art['documentation'] = []
        if files:
            for file in files:
                # файлы делятся по категориям
                if "image" in file["content_type"] or "jpg" in file["original_name"] or "jpeg" in file["original_name"] or "png" in file["original_name"]:
                    url = file["file_url"]
                    preview_link = url.split("/")
                    preview_link[-2] = "compress_image/yowai_mo"
                    url = '/'.join(preview_link)
                    file["file_url"] = f"{DOMAIN}{url}"
                    art['images'].append(file)
                elif "video" in file["content_type"]:
                    url = file["file_url"]
                    file["file_url"] = f"{DOMAIN}{url}"
                    art['videos_native'].append(file)
                elif "link" in file["content_type"]:
                    art['videos_embed'].append(file)
                else:
                    url = file["file_url"]
                    file["file_url"] = f"{DOMAIN}{url}"
                    art['documentation'].append(file)

        # сортируем фотки по айдишникам
        sorted_images = sorted(art['images'], key=lambda x: int(x['id']), reverse=False)
        art['images'] = sorted_images
        self.section_id = art['section_id']
        prev = await self.get_preview(session)
        art["preview_file_url"] = prev if prev else "https://portal.emk.ru/local/templates/intranet/img/no-user-photo.png"

        arts_info.append(arts_info)

    return arts_info