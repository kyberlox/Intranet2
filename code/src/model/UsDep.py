from ..base.Elastic.StuctureSearchmodel import StructureSearchModel
from ..base.Elastic.StuctureSearchmodel import StructureSearchModel
from ..base.B24 import B24
from ..services.LogsMaker import LogsMaker

from fastapi import APIRouter

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
# from jinja2 import Environment, FileSystemLoader
import json
import asyncio

from ..base.pSQL.objects.App import get_async_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

usdep_router = APIRouter(prefix="/users_depart")


# env = Environment(loader=FileSystemLoader("./front_jinja")) #/intranet_test/Intranet2/code/main.py


class UsDep:
    def __init__(self, ID=0, usr_id=0, dep_id=0):
        self.ID = ID
        self.usr_id = usr_id
        self.dep_id = dep_id

        from ..base.pSQL.objects import UsDepModel
        self.UserSQL = UsDepModel()

    async def get_usr_dep(self, session):
        b24 = B24()
        data = await b24.getUsers()
        logg = LogsMaker()

        # if hasattr(data, '_asyncio_future_blocking'):  # Это Task
        #     data = await data

        result = dict()
        # for usr in logg.progress(data, "Загрузка данных связей пользователей и подразделений "):

        for usr in logg.progress(data, "Загрузка данных связей пользователей и подразделений "):
            if usr['ID'] is not None:
                result['id'] = int(usr['ID'])
                result['depart'] = usr['UF_DEPARTMENT']
                await self.UserSQL.put_uf_depart(usr_dep=result, session=session)
        await StructureSearchModel().dump(session)
        return {"status": True}

    async def search_usdep_by_id(self, session):
        self.UserSQL.id = self.ID
        return await self.UserSQL.find_dep_by_user_id(session)


# Таблицу пользователей и департаментов можно обновить
@usdep_router.put("", tags=["Пользователь-Департамент", "Битрикс24"],
description="""
## Метод `getUsers()`

Получает список всех пользователей из Битрикс24 через API метод `user.get`.

### Параметры
Метод не принимает входных параметров.

### Возвращаемые данные
Возвращает список словарей с данными пользователей. Каждый словарь содержит поля пользователя Битрикс24, включая:
- `ID` (int) — уникальный идентификатор пользователя
- `UF_DEPARTMENT` (list) — список ID подразделений, к которым привязан пользователь
- другие стандартные поля пользователя (имя, фамилия, email и т.д.)

---

## Функция `get_usr_dep()`

Асинхронная функция для обработки и сохранения связей пользователей с подразделениями. Извлекает данные пользователей, обрабатывает связи с департаментами и сохраняет в базу данных.

### Входные параметры
| Параметр | Тип | Описание | Обязательный |
|----------|-----|----------|--------------|
| `session` | `AsyncSession` | Сессия для работы с базой данных | Да |

### Выходные данные
Возвращает словарь со статусом выполнения:
```json
{"status": true}
```

""")
async def get_user(session: AsyncSession = Depends(get_async_db)):
    return await UsDep().get_usr_dep(session)


# Пользователя и его департамент можно выгрузить
@usdep_router.get("/find_by/{ID}", tags=["Пользователь-Департамент"])
async def get_usdepart(ID, session: AsyncSession = Depends(get_async_db)):
    return await UsDep(ID=ID).search_usdep_by_id(session)


# поиск по id подразделения
@usdep_router.get("/get_structure_by_dep_id/{parent_id}", tags=["Пользователь-Департамент"])
def get_structure_by_dep_id(parent_id: int):
    return StructureSearchModel().get_structure_by_parent_id(parent_id)

# @usdep_router.get("/get_structure_by_dep_id/{parent_id}", response_class=HTMLResponse)
# async def get_structure_by_dep_id(request: Request, parent_id: int):
#     # Получаем сырые данные
#     raw_data = StructureSearchModel().get_structure_by_id(parent_id)

#     # Преобразуем данные в удобный формат
#     departments = []
#     for item in raw_data:
#         try:
#             source = item.get('_source', item)  # Для Elasticsearch и обычных dict
#             departments.append({
#                 'id': source['id'],
#                 'name': source['name'],
#                 'father_id': source.get('father_id'),
#                 'users': source.get('users', []),
#                 'path_depart': source.get('path_depart', '')
#             })
#         except (KeyError, TypeError) as e:
#             print(f"Ошибка обработки элемента: {e}, данные: {item}")
#             continue

#     # Находим корневое подразделение
#     root_dep = next((d for d in departments if d['id'] == parent_id), None)

#     if not root_dep:
#         return HTMLResponse(content="<h1>Подразделение не найдено</h1>", status_code=404)

#     # Строим иерархическую структуру
#     def build_tree(dep_id, deps):
#         children = [d for d in deps if d['father_id'] == dep_id]
#         for child in children:
#             child['children'] = build_tree(child['id'], deps)
#         return children

#     root_dep['children'] = build_tree(root_dep['id'], departments)

#     # Загружаем шаблон
#     template = env.get_template("department_structure.html")

#     # Рендерим шаблон
#     return template.render(
#         request=request,
#         root_department=root_dep,
#         all_departments=departments,
#         current_dep_id=parent_id
#     )