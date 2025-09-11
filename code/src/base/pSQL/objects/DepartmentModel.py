from sqlalchemy import text
from sqlalchemy.sql.expression import select

from ..models.Department import Department
from .App import db, engine

from sqlalchemy.exc import SQLAlchemyError

#!!!!!!!!!!!!!!!
from ....services import LogsMaker
#!!!!!!!!!!!!!!!

class DepartmentModel():
    def __init__(self, Id=None): #убрать None в будущем
        self.id = Id
        self.department = Department
        self.db = db

    def upsert_dep(self, dep_data):
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
            q = self.db.query(Department).filter(Department.id == dep_data["id"])
            dep_exist = self.db.query(q.exists()).scalar() # ПРОВЕРЕНО 

            DB_columns_dep = ['id', 'name', 'sort', 'user_head_id', 'father_id']

            # если такой id существует - проверить необходимость обновленияs
            if dep_exist:

                dep = self.db.execute(select(self.department).where(self.department.id == dep_data["id"])).scalar()
                                
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
                            

                        with engine.connect() as connection:
                            connection.execute(sql, dep_data)
                            connection.commit()
                    
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
                with engine.connect() as connection:
                    connection.execute(sql, dep_data)
                    connection.commit()
                    

        except SQLAlchemyError as e:
            # print(f'An error: {e}')
            return LogsMaker().error_message(e)

    def find_dep_by_id(self):
        """
        Ищет департамент по id
        """
        res = self.db.execute(select(self.department).where(self.department.id == self.id)).scalar()
        if res is not None:
            return [res]
        else:
            # return {'err': 'Нет такого департамента'}
            #return LogsMaker().warning_message('Нет такого департамента')
            return []

        # dep = self.db.query(self.department).get(self.id)
        # result = dict()
        # DB_columns = ['id', 'name', 'sort', 'user_head_id', 'father_id']
        # if dep is not None:
        #     for key in DB_columns:
        #         result[key] = dep.__dict__[key]
        #     return result
        # else:
        #     return {'err': 'Нет такого департамента'}
    
    def find_deps_by_father_id(self, father_id):
        result = []
        #null_depart = self.db.execute(select(self.department).where(self.department.father_id == None)).scalars().all()
        #res = self.db.query(self.department).filter(self.department.father_id == father_id).all()
        res = self.db.execute(select(self.department).where(self.department.father_id == father_id)).scalars().all()
        if res is not None:
            return res
        else:
            # return {'err': 'Нет такого департамента'}
            #return LogsMaker().warning_message('Нет такого департамента')
            return []

    def all(self):
        return self.db.query(self.department).all()
