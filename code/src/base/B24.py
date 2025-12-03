from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse

from bitrix24 import Bitrix24
import requests

import asyncio
import aiohttp


b24_router = APIRouter(prefix="/b24", tags=["Битрикс24"])

class B24:
    def __init__(self):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/qunp7dwdrwwhsh1w/")
        # self.bx24 = Bitrix24("https://test-portal.emk.ru/rest/3830/0gtzqs1nai8ocqft/")



    def getUsers(self):
        result = self.bx24.callMethod('user.get')
        return result
    
    def getUser(self, ID):
        result = self.bx24.callMethod(f'user.get?ID={ID}')
        return result

    def getDeps(self):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/wk7uewb9l4xjo0xc/")
        result = self.bx24.callMethod('department.get')
        return result

    def getInfoBlock(self, id):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/no7abhbtokxxctlb/")
        result = self.bx24.callMethod(f'lists.element.get?IBLOCK_TYPE_ID=lists&IBLOCK_ID={id}')
        return result




    async def get_file(self, id, inf_id):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/1/j6122m0ystded5ag/")
        result = await self.bx24.callMethod(f'disk.attachedObject.get?ENTITY_ID={inf_id}&id={id}')
        return result

    async def get_all_files(self, id):
        url = f'https://portal.emk.ru/pub/rest/d105d8c66fc049a96c58d2cc18ea171e98c7ba89a9afa6425f003e42b4d90991/getBfileById.php?id={id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    return None
        
        
        # response = requests.get(url)
        # result = response.json()
        # return result



    # функции vcard
    def getUsersByUuid(self, uuid):
        filter = {
                "XML_ID" : uuid
        }
        result = self.bx24.callMethod('user.search', filter=filter)
        return result

    def getDepartByID(self, id):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/wk7uewb9l4xjo0xc/")
        result = self.bx24.callMethod('department.get', ID=id)
        return result



    def get_picture_link(self, inf_id, art_id, picture_type, property):
        link = f"https://portal.emk.ru/company/lists/{inf_id}/file/0/{art_id}/{picture_type}/{property}/"
        # link = f"https://portal.emk.ru/user.search{inf_id}/file/0/{art_id}/{picture_type}/{property}/"

        return link

    def get_likes_views(self, art_id):
        url = f'https://portal.emk.ru/pub/rest/d105d8c66fc049a96c58d2cc18ea171e98c7ba89a9afa6425f003e42b4d90991/getLikes.php?id={art_id}'
        response = requests.get(url)
        result = response.json()
        return result



    '''Проксирую запросы в битру'''
    def send_idea(self, incr : int, fields : dict):
        el_code = f"intranet2_{incr}"

        #url = "https://portal.emk.ru/rest/1/aj7d42rcogl2f51b/lists.element.add?IBLOCK_TYPE_ID=lists&IBLOCK_ID=121&ELEMENT_CODE=test3&FIELDS%5BPROPERTY_1049%5D=test_number&FIELDS%5BNAME%5D=test_name&FIELDS%5BDETAIL_TEXT%5D=test_text&FIELDS%5BCREATED_BY%5D=user_id&FIELDS%5BPROPERTY_1027%5D=test_file"
        '''
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/1/aj7d42rcogl2f51b/")
        params = {
            "IBLOCK_TYPE_ID" : "lists",
            "IBLOCK_ID" : "121",
            "ELEMENT_CODE" : el_code,
            "FIELDS" : fields
        }
        try:
            result = self.bx24.callMethod('lists.element.add', params)
            print(f"Элемент успешно добавлен с ID: {result['ELEMENT_ID']}")
            return result
        except Exception as e:
            print(f"Не удалось добавить элемент: {e}")
            return e
        '''
        #https://portal.emk.ru/rest/1/p6653nbau95j5a0h/bizproc.workflow.start?TEMPLATE_ID=2216&DOCUMENT_ID[]=lists&DOCUMENT_ID[]=Bitrix\Lists\BizprocDocumentLists&DOCUMENT_ID[]=$ID
        
        name = fields["NAME"]
        cont_text = fields["DETAIL_TEXT"]
        uid = fields["CREATED_BY"]
        if "base" in fields:
            '''
            base = fields["base"]
            base_name = fields["base_name"]
            url = f"https://portal.emk.ru/rest/1/aj7d42rcogl2f51b/lists.element.add?IBLOCK_TYPE_ID=lists&IBLOCK_ID=121&ELEMENT_CODE={incr}&FIELDS[PROPERTY_1049]={incr}&FIELDS[NAME]={name}&FIELDS[PROPERTY_1049]=909&FIELDS[DETAIL_TEXT]={cont_text}&FIELDS[CREATED_BY]={uid}&FIELDS[PROPERTY_1027][fileName]={base_name}&FIELDS[PROPERTY_1027][fileData]={base}"
            headers = {
                'Content-Type': "Multipart/form-data"
            }

            response = requests.post(url)
            '''

            api_url = "https://portal.emk.ru/rest/1/aj7d42rcogl2f51b/lists.element.add"
            base = fields["base"]
            base_name = fields["base_name"]
            data = {
                'IBLOCK_TYPE_ID': 'lists',
                'IBLOCK_ID': '121',
                "IBLOCK_SECTION_ID": "319",
                'ELEMENT_CODE': el_code,
                'FIELDS[NAME]': name,
                'FIELDS[PROPERTY_1049]' : incr,
                #'FIELDS[PROPERTY_1117]' : "909",
                'FIELDS[DETAIL_TEXT]' : cont_text,
                'FIELDS[CREATED_BY]'  : uid,
                'FIELDS[PROPERTY_1027][fileName]'  : base_name,
                'FIELDS[PROPERTY_1027][fileData]' : base
            }

            headers = {
                'Content-Type': "application/x-www-form-urlencoded"
            }
                            
            response  = requests.post(api_url, data=data, headers=headers)
            

        else:
            url = f"https://portal.emk.ru/rest/1/aj7d42rcogl2f51b/lists.element.add?IBLOCK_TYPE_ID=lists&IBLOCK_ID=121&IBLOCK_SECTION_ID=319&ELEMENT_CODE={el_code}&FIELDS[PROPERTY_1049]={incr}&FIELDS[NAME]={name}&FIELDS[DETAIL_TEXT]={cont_text}&FIELDS[CREATED_BY]={uid}"
            response = requests.post(url)
        
        ID = response.json()['result']
            
        bis_url = f"https://portal.emk.ru/rest/1/p6653nbau95j5a0h/bizproc.workflow.start?TEMPLATE_ID=2216&DOCUMENT_ID[]=lists&DOCUMENT_ID[]=Bitrix\\Lists\\BizprocDocumentLists&DOCUMENT_ID[]={ID}"
        
        bis_response = requests.get(bis_url)

        return {"create_idea" : response.json(), "create_bis_log" : bis_response.json()}

    '''
    def get_calendar(self, date_from, date_to):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/1/f5ij1aoyuw5f39nb/")
        result = self.bx24.callMethod(f'calendar.event.get.json?type=company_calendar&ownerId=0&from={date_from}&to={date_to}')
        return result
    '''



@b24_router.get("/calendar/{date_from}/{date_to}",
description="""
    ## Получение событий корпоративного календаря
    
    Этот эндпоинт позволяет получить события из корпоративного календаря 
    за указанный период времени.
    
    ### Особенности:
    - Подключается к внешнему API Битрикс24
    - Возвращает события в формате JSON
    - Поддерживает фильтрацию по датам
    
    ### Параметры:
    - **date_from**: Начальная дата периода (формат: ГГГГ-ММ-ДД)
    - **date_to**: Конечная дата периода (формат: ГГГГ-ММ-ДД)
    - **type**: (опционально) Тип событий для фильтрации
    - **owner_id**: (опционально) ID владельца событий
    
    ### Примеры использования:
    ```
    GET /calendar/2024-01-01/2024-01-31
    GET /calendar/2024-01-01/2024-01-31?type=meeting&owner_id=123
    ```
    """,
)
def calendar_event(date_from, date_to):
    
    url = f"https://portal.emk.ru/rest/1/f5ij1aoyuw5f39nb/calendar.event.get.json?type=company_calendar&ownerId=0&from={date_from}&to={date_to}"
    response = requests.get(url)
    result = response.json()
    return result 