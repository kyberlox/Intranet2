from sqlalchemy import text
from sqlalchemy.sql.expression import select

from ..models.Department import Department
from .App import engine, get_db

from .App import AsyncSessionLocal, async_engine

from sqlalchemy.exc import SQLAlchemyError

import asyncio

from src.services.LogsMaker import LogsMaker
LogsMaker().ready_status_message("Успешная инициализация таблицы Подразделений")

db_gen = get_db()
database = next(db_gen)

class DepartmentModel:

    def __init__(self, Id=None): #убрать None в будущем
        self.id = Id

        from ..models.Department import Department
        self.department = Department

        # from .App import db
        # database = db

    async def upsert_dep(self, dep_data):
        """
        Добавляет или обновляет запись в таблице 'departments'.
        dep_data: словарь с данными департамента
        """
        # print(data)

        #валидация
        new_depat_data = dict()
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
                new_depat_data[key.lower()] = dep_data[key] # key.lower() - чтобы с БД были одинаковые столбцы
        dep_data = new_depat_data

        # проверить по id есть ли такой департамент
        try:  
            async with AsyncSessionLocal() as session:
                stmt = select(self.department).where(self.department.id == dep_data["id"])
                result = await session.execute(stmt)
                dep_exist = result.scalar_one_or_none()  # True или False
            # q = database.query(Department).filter(Department.id == dep_data["id"])
            # dep_exist = database.query(q.exists()).scalar() # ПРОВЕРЕНО 

            DB_columns_dep = ['id', 'name', 'sort', 'user_head_id', 'father_id']

            # если такой id существует - проверить необходимость обновленияs
            if dep_exist:

                async with AsyncSessionLocal() as session:
                    dep = await session.execute(select(self.departmen).where(self.department.id == dep_data["id"])).scalar()
                # dep = database.execute(select(Department).where(self.department.id == dep_data["id"])).scalar()
                                
                for column in DB_columns_dep:

                    u = getattr(dep, column, None) # значение column в БД
                    u_id = dep.__dict__["id"] # id данного значения column в БД
                    
                    # если есть изменения - обновить                    
                    if dep_data.get(column) != u:
                       
                        if dep_data.get(column) == None:  # если в битриксе нет значения по столбцу, то в БД запишет NULL
                            sql = text(f"UPDATE {Department.__tablename__} SET {column} = NULL WHERE id = {u_id}")

                        elif isinstance(dep_data.get(column), str): # если строковый тип, запишет в строковом виде
                            sql = text(f"UPDATE {Department.__tablename__} SET {column} = '{dep_data.get(column)}' WHERE id = {u_id}")

                        else:  # в если в битриксе числовое значение, то значение по колонке в БД запишет как число
                            sql = text(f"UPDATE {Department.__tablename__} SET {column} = {dep_data.get(column)} WHERE id = {u_id}")
                            

                        with async_engine.connect() as connection:
                            await connection.execute(sql, dep_data)
                            await connection.commit()
                    
                    # если изменений нет - пропустит итерацию
                    else:
                        pass
                            
                
            # если такого id не существует - добавляем        
            else:
                columns = "id"
                values = f"{dep_data['id']}"
                for key in dep_data.keys():
                    if key == 'id': # пропускаем итерацию по ключу 'id' тк его мы уже добавили
                        continue
                    elif key == 'name': # отдельно обрабатываем строковые значения
                        columns += f", {key}"
                        values += f", \'{dep_data[key]}\'"
                    else: # тут обрабатываем числовые значения, такие как: father_id, sort, user_head_id
                        columns += f", {key}"
                        values += f", {dep_data[key]}"
    
                # Запрос
                sql = text(f"INSERT INTO {Department.__tablename__} ({columns}) VALUES ({values})")
                
                # Выполняем SQL-запрос
                with async_engine.connect() as connection:
                    await connection.execute(sql, dep_data)
                    await connection.commit()
                    

        except SQLAlchemyError as e:
            # print(f'An error: {e}')
            return LogsMaker().error_message(e)

    async def find_dep_by_id(self):
        """
        Ищет департамент по id
        """
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(self.department).where(self.department.id == self.id)).scalar()
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
    
    async def find_deps_by_father_id(self, father_id):
        result = []
        #null_depart = database.execute(select(self.department).where(self.department.father_id == None)).scalars().all()
        #res = database.query(self.department).filter(self.department.father_id == father_id).all()
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(self.department).where(self.department.father_id == father_id)).scalars().all()
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
