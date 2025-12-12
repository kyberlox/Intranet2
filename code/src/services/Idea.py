from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header

from ..base.B24 import B24
from ..model.User import User

from .LogsMaker import LogsMaker

import asyncio

idea_router = APIRouter(prefix="/idea")



def take_value(PROPERTY):
    if type(PROPERTY) == type(str()):
        return PROPERTY
    elif type(PROPERTY) == type(dict()):
        return list(PROPERTY.values())[0]
    elif type(PROPERTY) == type(list()):
        return PROPERTY[0]
    else:
        return None

class Idea:
    def __init__(self, user_id=None, user_uuid=None):
        

        self.ideas = []
        self.user_uuid = None
        self.username = None

    async def validate_ideas(self):
        #беру идеи из битры
        b24_ideas = await B24().getInfoBlock(121)

        

        ideas = []
        #каждую идею
        for idea in b24_ideas:
            #проебразую по шаблону с нормальными ключами
            prop_keys = {
                "ID" : "id",
                "NAME" : "name",
                "CREATED_BY" : "user_id",
                "CREATED_USER_NAME" : "username",
                "DETAIL_TEXT" : "content",
                "DETAIL_TEXT_TYPE" : "content_type",
                "DATE_CREATE" : "date_create",
                "PROPERTY_1049" : "number",
                "PROPERTY_1117" : "status",
                "PROPERTY_1027" : "document_id"
            }

            
            
            cool_idea = dict()
            for prop in prop_keys.keys():
                key = prop_keys[prop]
                val = None
                if prop in idea.keys():
                    val = take_value(idea[prop])

                cool_idea[key] = val
            
            

            #валидирую статус идеи
            valid_staus = {
                None : None,
                "909" : "На экспертизе",
                "910" : "В работе",
                "912" : "Реализовано",
                "913" : "Отказано",
                "2151" : "Новая",
                "2152" : "Рассмотрение",
                "2161" : "Реализация в рамках другой задачи",
                "2176" : "Принято"
            }

            if "status" in cool_idea:
                cool_idea["status"] = valid_staus[cool_idea["status"]]

            #сохраняю
            ideas.append(cool_idea)
        self.ideas = ideas

    async def get_user(self, user_id, session):
        from src.services.Auth import AuthService
        self.user = User(id=user_id).find_by_id()

        if self.user is not None:
            self.user_uuid = self.user["user_uuid"]
            self.username = self.user["username"]

            #получить и вывести его id
            user_inf = await User(uuid = self.user_uuid).user_inf_by_uuid(session)
            return user_inf["ID"]
        return None
        
    async def get_ideas(self, user_id, session):
        await self.validate_ideas()
        if user_id is not None:
            #print(user_id)
            result = []
            for idea in self.ideas:

                if str(idea['user_id']) == str(user_id):
                
                    if idea["document_id"]:
                        file_id = idea.pop("document_id")
                        try:
                            file_info = B24().get_file(id=file_id, inf_id=121)
                        except:
                            file_info = B24().get_all_files(id=file_id)
                        file_url = "https://portal.emk.ru" + file_info["SRC"]
                        idea['files'] = {'original_name': file_info['ORIGINAL_NAME'], 'file_url': file_url}
                    else:
                        idea.pop("document_id")
                        idea['files'] = dict()
                    result.append(idea)
            return result
        else:
            return None
    
    async def add(self, fields):
        await self.validate_ideas()
        #получить значение инкремента
        print(self.ideas[-1])

        '''
        max_id = 0
        
        for idea in self.ideas:
            if int(idea['number']) > max_id:
                max_id = int(idea['number'])
        incr = max_id + 1
        '''

        incr = int(self.ideas[-1]['number']) + 1
        print(incr)
        res = B24().send_idea(incr, fields)
        return res


@idea_router.post("/new/", tags=["Есть Идея!", "Битрикс24"])
async def calendar_event(data = Body()):
    """
    ## Метод `getInfoBlock(id)`

    Получает элементы информационного блока (списка) из Битрикс24 по его ID через API метод `lists.element.get`.

    ### Входные параметры
    | Параметр | Тип | Описание | Обязательный |
    |----------|-----|----------|--------------|
    | `id` | integer | ID информационного блока (IBLOCK_ID) в Битрикс24 | Да |

    ### Возвращаемые данные
    Возвращает список элементов информационного блока. Каждый элемент содержит следующие поля:
    - `ID` (string) — уникальный идентификатор элемента в Битрикс24
    - `NAME` (string) — название идеи
    - `CREATED_BY` (string) — ID создателя
    - `CREATED_USER_NAME` (string) — имя создателя
    - `DETAIL_TEXT` (string) — подробное описание идеи
    - `DETAIL_TEXT_TYPE` (string) — тип текста (text/html)
    - `DATE_CREATE` (string) — дата создания
    - `PROPERTY_1049` (string) — номер идеи
    - `PROPERTY_1117` (string) — код статуса идеи
    - `PROPERTY_1027` (string) — ID связанного документа
    - Другие пользовательские свойства

    ### Пример ответа
    ```json
    [
        {
            "ID": "456",
            "NAME": "Автоматизация отчетности",
            "CREATED_BY": "123",
            "CREATED_USER_NAME": "Иванов Иван",
            "DETAIL_TEXT": "Предлагаю автоматизировать формирование еженедельных отчетов...",
            "DETAIL_TEXT_TYPE": "html",
            "DATE_CREATE": "2024-03-15T14:30:00+03:00",
            "PROPERTY_1049": "15",
            "PROPERTY_1117": "2151",
            "PROPERTY_1027": "789"
        }
    ]
    """
    return await Idea().add(dict(data))