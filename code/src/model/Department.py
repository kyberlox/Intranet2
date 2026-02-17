# from ..base.Elastic.StuctureSearchmodel import StructureSearchModel
from ..services.LogsMaker import LogsMaker

from fastapi import APIRouter, Body, Request

# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.pSQL.objects.App import get_async_db

# templates = Jinja2Templates(directory="./front_jinja")

import asyncio

depart_router = APIRouter(prefix="/departments")

class Department:
    def __init__(self, id=0, name="", father_id="", data=""): #убрать = после каждой переменной в будущем
        self.id = id
        self.name = name
        self.father_id = father_id
        self.data = data

        from ..base.pSQL.objects.DepartmentModel import DepartmentModel
        self.department = DepartmentModel()


    async def fetch_departments_data(self, session):
        from ..base.B24 import B24
        data = await B24().getDeps()
        logg = LogsMaker()

        # if hasattr(data, '_asyncio_future_blocking'):  # Это Task
        #     data = await data

        #отправить записи
        for dep in logg.progress(data, "Загрузка данных подразделений "):
            #if dep['ID'] == '420':
            await self.department.upsert_dep(dep_data=dep, session=session)
            await session.commit()

            
        # StructureSearchModel().create_index()
        return {"status" : True}
    

    async def search_dep_by_id(self, session):
        self.department.id = self.id
        return await self.department.find_dep_by_id(session)

# Dependency для получения айдишника пользователя
async def get_user_id_by_session_id(request: Request) -> int:
    from ..base.RedisStorage import RedisStorage
    """Получение текущей сессии пользователя"""
    # Ищем session_id в куках или заголовках
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        auth_header = request.headers.get("session_id")
        if auth_header:# and auth_header.startswith("Bearer "):
            session_id = auth_header#[7:]
    
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    session_data = RedisStorage().get_session(key=session_id)

    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_id = session_data['user_info']['ID']
    return user_id


# Департаменты можно обновить
# @depart_router.put("",tags=["Департамент", "Битрикс24"])
# async def get_department(session: AsyncSession=Depends(get_async_db)):
#     """
#     ## Метод `department.get`

#     > Метода вызывается один раз, в момент запуска сервиса для загрузки данных с прошлой версии сайта

#     Получает список всех подразделений (департаментов) из Битрикс24 через API метод `department.get`.

#     ### Входные параметры
#     Метод не принимает параметров. Автоматически использует предварительно настроенное подключение к порталу Битрикс24.

#     ### Возвращаемые данные
#     Возвращает список словарей с данными подразделений. Каждое подразделение содержит следующие поля:
#     - `ID` (int/string) — уникальный идентификатор подразделения
#     - `NAME` (string) — название подразделения
#     - `PARENT` (int/string) — ID родительского подразделения (1 для корневых)
#     - `UF_HEAD` (int/string) — ID руководителя подразделения
#     - `SORT` (int) — индекс сортировки
#     - Другие стандартные поля подразделения Битрикс24

#     ### Пример ответа
#     ```json
#     [
#         {
#             "ID": "1",
#             "NAME": "Компания",
#             "PARENT": null,
#             "UF_HEAD": "123",
#             "SORT": "100"
#         },
#         {
#             "ID": "5",
#             "NAME": "Отдел разработки",
#             "PARENT": "1",
#             "UF_HEAD": "456",
#             "SORT": "200"
#         },
#         {
#             "ID": "12",
#             "NAME": "Фронтенд разработка",
#             "PARENT": "5",
#             "UF_HEAD": "789",
#             "SORT": "210"
#         }
#     ]
#     ```
    
#     """
#     depart = Department()
#     return await depart.fetch_departments_data(session)

# Департамент можно выгрузить
@depart_router.get("/find_by/{id}", tags=["Департамент"])
async def get_department(id: int, session: AsyncSession=Depends(get_async_db)):
    return await Department(id).search_dep_by_id(session)

#загрузить дату в ES
@depart_router.put("/elastic_data", tags=["Департамент"])
def upload_department_to_es(session: AsyncSession=Depends(get_async_db)):
    return StructureSearchModel().dump(session=session)

