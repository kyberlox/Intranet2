from sqlalchemy import text
from sqlalchemy.sql.expression import select

from ..models.Department import Department
# from .App import engine, get_db

from .App import AsyncSessionLocal, async_engine

from sqlalchemy.exc import SQLAlchemyError

import asyncio

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Подразделений")

# db_gen = get_db()
# database = next(db_gen)

class DepartmentModel:

    def __init__(self, Id: int = None): #убрать None в будущем
        self.id = Id

        from ..models.Department import Department
        self.department = Department

    async def upsert_dep(self, dep_data, session):
        """
        Добавляет или обновляет запись в таблице 'departments'.
        Использует только переданную сессию.
        """
        try:
            # Валидация и нормализация данных
            new_depat_data = {}
            for key in dep_data.keys():
                if key == 'ID':
                    new_depat_data['id'] = int(dep_data[key])
                elif key == 'PARENT':
                    new_depat_data['father_id'] = int(dep_data[key])
                elif key == 'UF_HEAD':
                    new_depat_data['user_head_id'] = int(dep_data[key])
                elif key == 'SORT':
                    new_depat_data['sort'] = int(dep_data[key])
                else:
                    new_depat_data[key.lower()] = dep_data[key]
            dep_data = new_depat_data

            # Проверяем существование департамента
            stmt = select(self.department).where(self.department.id == dep_data["id"])
            result = await session.execute(stmt)
            existing_dep = result.scalar_one_or_none()

            DB_columns_dep = ['id', 'name', 'sort', 'user_head_id', 'father_id']

            if existing_dep:
                # ОБНОВЛЕНИЕ существующего департамента через ORM
                need_update = False
                
                for column in DB_columns_dep:
                    if column == 'id':  # ID не обновляем
                        continue
                        
                    current_value = getattr(existing_dep, column)
                    new_value = dep_data.get(column)
                    
                    if new_value != current_value:
                        setattr(existing_dep, column, new_value)
                        need_update = True
                
                if need_update:
                    # Сессия уже отслеживает изменения, коммит будет позже
                    LogsMaker().info_message(f"Обновлен департамент {dep_data['id']}")
                else:
                    LogsMaker().info_message(f"Департамент {dep_data['id']} не требует обновления")
                    
            else:
                # СОЗДАНИЕ нового департамента через ORM
                create_data = {col: dep_data[col] for col in DB_columns_dep if col in dep_data}
                new_dep = self.department(**create_data)
                session.add(new_dep)
                LogsMaker().info_message(f"Создан департамент {dep_data['id']}")

            # НЕТ коммита здесь - коммит будет в вызывающем коде
            return True
            
        except Exception as e:
            return LogsMaker().error_message(f'Ошибка при обработке департамента {dep_data.get("id")}: {e}')
            # return False

    async def find_dep_by_id(self, session):
        """
        Ищет департамент по id
        """
        result = await session.execute(select(self.department).where(self.department.id == int(self.id)))
        res = result.scalar()
        # res = database.query(Department).get(self.id) #database.execute(select(self.department).where(self.department.id == self.id)).scalar()

        if res is not None:
            # res = res.__dict__
            # res.pop('_sa_instance_state')
            return [res]

        else:
            # return {'err': 'Нет такого департамента'}
            #return LogsMaker().warning_message('Нет такого департамента')
            return []

        # dep = database.query(self.department).get(self.id)
        # result = dict()
        # DB_columns = ['id', 'name', 'sort', 'user_head_id', 'father_id']
        # if dep is not None:
        #     for key in DB_columns:
        #         result[key] = dep.__dict__[key]
        #     return result
        # else:
        #     return {'err': 'Нет такого департамента'}
    
    async def find_deps_by_father_id(self, father_id, session):
        # result = []
        #null_depart = database.execute(select(self.department).where(self.department.father_id == None)).scalars().all()
        #res = database.query(self.department).filter(self.department.father_id == father_id).all()
        
        result = await session.execute(select(self.department).where(self.department.father_id == father_id))
        res = result.scalars().all()
        # res = database.execute(select(Department).where(self.department.father_id == father_id)).scalars().all()
        if res is not None:
            return res
        else:
            # return {'err': 'Нет такого департамента'}
            #return LogsMaker().warning_message('Нет такого департамента')
            return []

    async def all(self):
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(self.department)).scalars().all()
        # return database.query(Department).all()
        return res
