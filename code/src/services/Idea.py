from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Response, Request, Cookie#, Header

from ..base.B24 import B24
from ..model.User import User

from .LogsMaker import LogsMaker

import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..base.pSQL.objects.App import get_async_db


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
                            file_info = await B24().get_file(id=file_id, inf_id=121)
                        except:
                            file_info = await B24().get_all_files(id=file_id)
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

# async def get_uuid_from_request(request, session):
#     # from .Auth import AuthService
#     user_id = None
#     token = request.cookies.get("user_id")
#     if token is None:
#         token = request.headers.get("user_id")
#         if token is not None:
#             user_id = token
#     else:
#         user_id = token

#     if user_id is not None:

#         # получить и вывести его id
#         usr = User()
#         usr.id = int(user_id)
#         user_inf = await usr.search_by_id(session=session)
#         if user_inf is not None and "id" in user_inf.keys():
#             return user_inf["id"]
#     return None

@idea_router.post("/new/", tags=["Есть Идея!", "Битрикс24"],
description="""
## Метод `lists.element.add`

Создает новую идею в информационном блоке Битрикс24 и запускает бизнес-процесс. Метод поддерживает два варианта: с прикрепленным файлом и без него.

### Входные параметры
| Параметр | Тип | Описание | Обязательный |
|----------|-----|----------|--------------|
| `incr` | integer | Уникальный инкрементальный номер идеи | Да |
| `fields` | dict | Данные для создания идеи. Может включать: | Да |
| | | - `NAME` (string) — название идеи | |
| | | - `DETAIL_TEXT` (string) — описание идеи | |
| | | - `CREATED_BY` (string) — ID автора идеи | |
| | | - `base` (string) — содержимое файла в base64 (опционально) | |
| | | - `base_name` (string) — имя файла (опционально) | |

""")
async def calendar_event(request: Request, session: AsyncSession = Depends(get_async_db), data = Body()):
    from .Peer import Peer
    user_id = None
    token = request.cookies.get("user_id")
    if token is None:
        token = request.headers.get("user_id")
        if token is not None:
            user_id = token
    else:
        user_id = token
    print(user_id, 'Получили ли из заголовков')
    send_idea =  await Idea().add(dict(data))
    if send_idea and user_id:
        """
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        В будущем поставить сюда айдишник той активности, 
        которая отвечает за отправку баллов предложенной активности
        И поставить айдишник нашего административного аккаунта
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        # id = 8
        send_data = {
            "uuid_from": 4133, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК НАШЕГО АДМИНИСТРАТИВНОГО АККАУНТА
            "uuid_to": int(user_id),
            "activities_id": 8, #  В БУДУЩЕМ ПОСТАВИТЬ АЙДИИШНИК АКТИВНОСТИ 
            "description": f"Баллы за предложение по улучшению сервиса: {data['NAME']}"
        }
        send_point = await Peer(user_uuid=send_data['uuid_from']).send_points(data=send_data)
        return send_idea
    else:
        return LogsMaker().error_message("Произошла ошибка с получением айдишника пользоватля из сессии и заголовков")
    
