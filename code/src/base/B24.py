from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header
from fastapi.responses import JSONResponse

from bitrix24 import Bitrix24
import requests

#import asyncio

b24_router = APIRouter(prefix="/b24", tags=["Битрикс24"])

class B24:
    def __init__(self):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/qunp7dwdrwwhsh1w/")



    def getUsers(self):
        result = self.bx24.callMethod('user.get')
        return result

    def getDeps(self):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/wk7uewb9l4xjo0xc/")
        result = self.bx24.callMethod('department.get')
        return result

    def getInfoBlock(self, id):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/2158/no7abhbtokxxctlb/")
        result = self.bx24.callMethod(f'lists.element.get?IBLOCK_TYPE_ID=lists&IBLOCK_ID={id}')
        return result



    def get_file(self, id, inf_id):
        self.bx24 = Bitrix24("https://portal.emk.ru/rest/1/j6122m0ystded5ag/")
        result = self.bx24.callMethod(f'disk.attachedObject.get?ENTITY_ID={inf_id}&id={id}')
        return result

    def get_all_files(self, id):
        url = f'https://portal.emk.ru/pub/rest/d105d8c66fc049a96c58d2cc18ea171e98c7ba89a9afa6425f003e42b4d90991/getBfileById.php?id={id}'
        response = requests.get(url)
        result = response.json()
        return result



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

        return link

    def get_likes_views(self, art_id):
        url = f'https://portal.emk.ru/pub/rest/d105d8c66fc049a96c58d2cc18ea171e98c7ba89a9afa6425f003e42b4d90991/getLikes.php?id={art_id}'
        response = requests.get(url)
        result = response.json()
        return result



    '''Проксирую запросы в битру'''
    def send_idea(self, incr : int, fields : dict):
        #el_code = f"intranet2_{incr}"

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
            base = fields["base"]
            base_name = fields["base_name"]
            url = f"https://portal.emk.ru/rest/1/aj7d42rcogl2f51b/lists.element.add?IBLOCK_TYPE_ID=lists&IBLOCK_ID=121&ELEMENT_CODE={incr}&FIELDS[PROPERTY_1049]={incr}&FIELDS[NAME]={name}&FIELDS[PROPERTY_1049]=909&FIELDS[DETAIL_TEXT]={cont_text}&FIELDS[CREATED_BY]={uid}&FIELDS[PROPERTY_1027][fileName]={base_name}&FIELDS[PROPERTY_1027][fileData]={base}"
            headers = {
                'Content-Type': "Multipart/form-data"
            }
            
            response = requests.post(url)
        
            return response.json()
        else:
            url = f"https://portal.emk.ru/rest/1/aj7d42rcogl2f51b/lists.element.add?IBLOCK_TYPE_ID=lists&IBLOCK_ID=121&ELEMENT_CODE={incr}&FIELDS[PROPERTY_1049]=909&FIELDS[PROPERTY_1049]={incr}&FIELDS[NAME]={name}&FIELDS[DETAIL_TEXT]={cont_text}&FIELDS[CREATED_BY]={uid}"
            print(url)
            response = requests.get(url)
            #result = response.json()
            #return result
            return response


@b24_router.get("/calendar/{date_from}/{date_to}")
def calendar_event(date_from, date_to):
    url = f"https://portal.emk.ru/rest/1/f5ij1aoyuw5f39nb/calendar.event.get.json?type=company_calendar&ownerId=0&from={date_from}&to={date_to}"
    response = requests.get(url)
    result = response.json()
    return result.text