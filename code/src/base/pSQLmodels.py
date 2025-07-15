from sqlalchemy import create_engine, Column, Integer, Text, Boolean, String, DateTime, JSON, MetaData, Table, ForeignKey, desc, func, Date
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import exists, select
from sqlalchemy import inspect, text
from sqlalchemy import update, insert, delete

from typing import List, Optional, Dict, Tuple

import json
import datetime
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

from src.model.File import File
from src.services.LogsMaker import LogsMaker

load_dotenv()

user = os.getenv('user')
pswd = os.getenv('pswd')

# Настройка подключения к базе данных PostgreSQL
engine = create_engine(f'postgresql+psycopg2://{user}:{pswd}@postgres/pdb', pool_size=50, max_overflow=0)



Base = declarative_base()
Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uuid = Column(Text, nullable=True)
    active = Column(Boolean, nullable=True)
    name = Column(Text, nullable=True)
    last_name = Column(Text, nullable=True)
    second_name = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    personal_mobile = Column(Text, nullable=True)
    uf_phone_inner = Column(Text, nullable=True)
    personal_city = Column(Text, nullable=True)
    personal_gender = Column(String, nullable=True)
    personal_birthday = Column(DateTime, nullable=True)
    indirect_data = Column(JSONB, nullable=True)
    photo_file_id = Column(Text, nullable=True)

    # Отношения для лайков и просмотров
    likes = relationship("Likes", back_populates="user")
    #views = relationship("Views", back_populates="user")

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    father_id = Column(Integer, nullable=True)
    user_head_id = Column(Integer, nullable=True)
    sort = Column(Integer, nullable=True)

class UsDep(Base):
    __tablename__ = 'usdep'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    dep_id = Column(Integer, nullable=True)

class Section(Base):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    parent_id = Column(Integer, nullable=True)

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, nullable=True)
    name = Column(Text, nullable=True)
    active = Column(Boolean, nullable=True, default=True)
    preview_text = Column(Text, nullable=True)
    content_text = Column(Text, nullable=True)
    content_type = Column(String, nullable=True)
    date_publiction = Column(DateTime, nullable=True)
    date_creation = Column(DateTime, nullable=True)
    indirect_data = Column(JSONB, nullable=True)
    #preview_image_url = Column(Text, nullable=True)

    # Отношения для лайков и просмотров
    likes = relationship("Likes", back_populates="article")
    views = relationship("Views", back_populates="article")

class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID пользователя
    article_id = Column(Integer, ForeignKey('article.id'), nullable=False)  # ID статьи
    created_at = Column(DateTime, default=datetime.utcnow)  # Время создания лайка
    is_active = Column(Boolean, default=True)  # Флаг активности лайка (можно убирать лайки)

    # Опциональные отношения для удобства доступа
    user = relationship("User", back_populates="likes")
    article = relationship("Article", back_populates="likes")

class Views(Base):
    """
    Класс для хранения просмотров пользователями статей.
    Связывает пользователей (User) и статьи (Article) многие-ко-многим.
    """
    __tablename__ = 'views'

    id = Column(Integer, primary_key=True)
    #user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID пользователя
    article_id = Column(Integer, ForeignKey('article.id'), nullable=False)  # ID статьи
    viewes_count = Column(Integer, nullable=False)  # Время просмотра

    # Опциональные отношения для удобства доступа
    #user = relationship("User", back_populates="views")
    article = relationship("Article", back_populates="views")


metadata = MetaData()

NewUser = Table('newusers', metadata,
                Column('id', Integer, primary_key=True),
                Column('active', Boolean),
                Column('last_name', Text),
                Column('name', Text),
                Column('second_name', Text),
                Column('dat', Date),
                Column('indirect_data', JSONB),
                Column('photo_file_id', Text)
            )

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=True, bind=engine)
db = SessionLocal()



class UserModel():
    def __init__(self, Id=None, uuid=None):
        self.id = Id
        self.uuid = uuid
        self.user = User#.__table__
        #self.inspector = inspect(engine)

        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autoflush=True, bind=engine)
        self.db = SessionLocal()

    def upsert_user(self, user_data):
        """
        Добавляет или обновляет запись в таблице.
        user_data: словарь с данными пользователя
        """

        #валидация
        new_user_data = dict()
        for key in user_data.keys():
            # валидация
            if key == 'ID':
                new_user_data["id"] = int(user_data[key])
            elif key == 'XML_ID':
                new_user_data["uuid"] = user_data["XML_ID"][3:]
            else:
                new_user_data[key.lower()] = user_data[key]
        user_data = new_user_data

        #проверить по id есть ли такой пользователь
        try:
            #usr = db.query(self.user).get(user_data['id'])
            #usr = db.query(User).filter(self.user.id == user_data['id']).first()

            q = self.db.query(User).filter(User.id == user_data["id"])
            usr = self.db.query(q.exists()).scalar()  # returns True or False

            DB_columns = ['uuid', 'active', 'name', 'last_name', 'second_name', 'email', 'personal_mobile', 'uf_phone_inner', 'personal_city', 'personal_gender', 'personal_birthday']

            #если есть - проверить необходимость обновления
            if usr:
                #user = db.query(self.user).filter(User.id == user_data["id"]).first()
                user = self.db.query(User).get(user_data['id'])

                #проверить есть ли изменения
                need_update = False

                #проверка основных параметров
                new_params = []
                for column in DB_columns:
                    if user_data.get(column) != user.__dict__[column]:
                        if column == 'personal_birthday':
                            # обработка дат
                            if user_data.get('personal_birthday') != "":
                                dt_new = datetime.strptime(user_data.get('personal_birthday').split('T')[0], '%Y-%m-%d').date()
                                cur_dt = f"\'{datetime.strptime(user_data.get('personal_birthday').split('T')[0], '%Y-%m-%d').date()}  04:00:00\'"
                            else:
                                dt_new = None

                            if user.personal_birthday is not None:
                                dt_old = user.personal_birthday.date()
                            else:
                                dt_old = user.personal_birthday

                            if dt_new != dt_old:
                                need_update = True
                                new_params.append(column)
                                user.__dict__[column] = dt_new
                                print(user.id , column, dt_new)
                        else:
                            need_update = True
                            new_params.append(column)
                            if user_data.get(column) == "":
                                user.__dict__[column] = "NULL"
                            else:
                                user.__dict__[column] = f"\'{user_data.get(column)}\'"
                            print(user.id, column, user_data.get(column))

                # если есть изменения - внести
                if need_update:
                    for cls in new_params:
                        sql = text(f"UPDATE {User.__tablename__} SET {cls} = {user.__dict__[cls]} WHERE id = {user.id}")
                        with engine.connect() as connection:
                            connection.execute(sql, user_data)
                            connection.commit()



                # проверить есть ли изменения
                need_update_indirect_data = False
                #проверка доп. параметров
                for key in user_data.keys():
                    if key not in DB_columns:
                        if (key not in user.indirect_data) or (user_data[key] != user.indirect_data[key]):
                            #изменить, если требуется
                            need_update_indirect_data = True
                            user.indirect_data[key] = user_data[key]
                            print(key, user.indirect_data[key])

                # если есть изменения - внести
                if need_update_indirect_data:
                    indirect_jsnb = json.dumps(user.indirect_data)
                    sql = text(f"UPDATE {User.__tablename__} SET indirect_data = \'{indirect_jsnb}\' WHERE id = {user.id}")
                    with engine.connect() as connection:
                        connection.execute(sql, user_data)
                        connection.commit()



            #если нет - добавить
            else:
                # Формируем SQL-запрос
                columns = "id"
                values = f"{user_data['id']}"
                meta = dict()
                # Все данные пользователя
                for key in user_data.keys():
                    #если это обязательные поля
                    if key in DB_columns:
                        #отдельно обработаем active так это не строковый формат
                        if key == 'active':
                            columns += f", active"
                            values += f", {user_data[key]}"
                        #если дата - пустая строка
                        elif key == 'personal_birthday' and user_data[key] == "":
                            columns += f", {key}"
                            values += f", NULL"
                        #потом остальные
                        else:
                            columns += f", {key}"
                            values += f", \'{user_data[key]}\'"

                    #оставшиеся - в метаданные
                    else:
                        meta[key] = user_data[key]



                columns += f", indirect_data"
                indirect_jsnb = json.dumps(meta)
                values += f", \'{indirect_jsnb}\'"
                # Запрос
                sql = text(f"INSERT INTO {User.__tablename__} ({columns}) VALUES ({values})")

                # Выполняем SQL-запрос
                with engine.connect() as connection:
                    connection.execute(sql, user_data)
                    connection.commit()
            # тут создать представление
            view = text(f"CREATE VIEW NewUsers AS\n"
            f"SELECT users.id,\n"
                f"users.active,\n"
                f"users.last_name,\n"
                f"users.name,\n"
                f"users.second_name,\n"
                f"to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text) AS dat,\n"
                f"users.indirect_data,\n"
                f"users.photo_file_id\n"
            f"FROM users\n"
            f"WHERE users.active = true AND to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text) >= (date_trunc('week'::text, CURRENT_DATE::timestamp with time zone) - '14 days'::interval)\n"
            f"ORDER BY (to_date(users.indirect_data ->> 'date_register'::text, 'YYYY-MM-DD'::text));"
            )
            try:
                with engine.connect() as connection:
                    connection.execute(view)
                    connection.commit()
            except:
                pass
        except SQLAlchemyError as e:
            db.rollback()
            #print(f"An error occurred: {e}")
            LogsMaker().error_message(e)

    def find_by_id(self):
        """
        Ищет пользователя по id
        """
        user = self.db.query(self.user).get(self.id)
        result = dict()
        DB_columns = ['id', 'uuid', 'active', 'name', 'last_name', 'second_name', 'email', 'personal_mobile', 'uf_phone_inner', 'personal_city', 'personal_gender', 'personal_birthday']
        if user is not None:
            for key in DB_columns:
                result[key] = user.__dict__[key]

            indirect_data = user.indirect_data
            list_departs = []
            if len(indirect_data['uf_department']) != 0:
                for dep in indirect_data['uf_department']:
                    dedep = DepartmentModel(dep).find_dep_by_id()
                    if type(dedep) == type(dict()):
                        if 'name' in dedep:
                            list_departs.append(dedep['name'])
                        else:
                            print(dedep)
                    else: #если объект
                        for dp in dedep:
                            list_departs.append(dp.__dict__['name'])

            if "uf_usr_department_main" in indirect_data:
                dedep = DepartmentModel(indirect_data["uf_usr_department_main"]).find_dep_by_id()
                indirect_data["uf_usr_department_main"] = dedep[0].name

            indirect_data['uf_department'] = list_departs
            result['indirect_data'] = indirect_data
            
            #информация о фото
            #вывод ID фотографии пользователя
            result['photo_file_id'] = user.__dict__['photo_file_id']
            if 'photo_file_id' in user.__dict__.keys() and user.__dict__['photo_file_id'] is not None:
                photo_inf = File(id=user.__dict__['photo_file_id']).get_users_photo()

                #вывод URL фотографии пользователя
                url = photo_inf['URL']
                #!!!!!!!!!!!!!!!!!!временно исправим ссылку!!!!!!!!!!!!!!!!!
                result['photo_file_url'] = f"http://intranet.emk.org.ru{url}"
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                result['photo_file_b24_url'] = photo_inf['b24_url']
            else:
                result['photo_file_id'] = None
                result['photo_file_url'] = None
                result['photo_file_b24_url'] = None
                
            return result

        else:
            LogsMaker().warning_message("Invalid user id")
            '''
            user_not_found = {
                "id": 9999999,
                "uuid": "",
                "active": True,
                "name": "Не",
                "last_name": "Пользователь",
                "second_name": "Найден",
                "email": "",
                "personal_mobile": "",
                "uf_phone_inner": "",
                "personal_city": "",
                "personal_gender": "M",
                "personal_birthday": "2025-07-04T04:00:00",
                "photo_file_id": None,
                "photo_file_url": None,
                "photo_file_b24_url": None,
                "indirect_data": {
                    "id": 2375,
                    "title": "",
                    "work_fax": "",
                    "work_www": "",
                    "work_zip": "",
                    "is_online": "N",
                    "time_zone": "Europe/Saratov",
                    "user_type": "employee",
                    "work_city": "",
                    "last_login": "",
                    "work_notes": "",
                    "work_pager": "",
                    "work_phone": "",
                    "work_state": "",
                    "timestamp_x": {},
                    "work_street": "",
                    "personal_fax": "",
                    "personal_icq": "",
                    "personal_www": "",
                    "personal_zip": "",
                    "work_company": "",
                    "work_country": "0",
                    "work_mailbox": "",
                    "work_profile": "",
                    "date_register": "",
                    "uf_department": [],
                    "work_position": "Не определено",
                    "personal_notes": "",
                    "personal_pager": "",
                    "personal_phone": "",
                    "personal_photo": "",
                    "personal_state": "",
                    "personal_street": "",
                    "work_department": "",
                    "personal_country": "0",
                    "personal_mailbox": "",
                    "time_zone_offset": "0",
                    "last_activity_date": {},
                    "uf_employment_date": "",
                    "personal_profession": "",
                    "uf_usr_1586854037086": "",
                    "uf_usr_1586861567149": "",
                    "uf_usr_1594879216192": "",
                    "uf_usr_1679387413613": [],
                    "uf_usr_1696592324977": [""],
                    "uf_usr_1705744824758": [""],
                    "uf_usr_1707225966581": False
                }
            }
            '''
            return None

    def find_by_uuid(self):
        user = self.db.query(self.user).filter(self.user.uuid == self.id).one()

        if user is not None:
            return {
                "ID": user.id,
                "email" : user.email,
                "full_name" : f"{user.second_name} {user.name} {user.last_name}"
            }
        else:
            return LogsMaker().warning_message("Invalid user uuid")
    
    def all(self):
        return self.db.query(self.user).all()
    
    def set_user_photo(self, file_id):
        #update(User).values({"photo_file_id": file_id, "photo_file_url" : file_url}).where(User.id == self.id)
        with Session(engine) as session:
            stmt = update(User).where(User.id == self.id).values(photo_file_id=str(file_id))
            result = session.execute(stmt)
            session.commit()

            return result
    
    def find_all_celebrants(self, date):
        """
        Выводит список пользователей, у кого день рождение в этот день (date)
        Важно! Не выводит пользователей, у кого департамент Аксиома и у кого нет фото
        """
        normal_list = []
        users = self.db.query(self.user).filter(func.to_char(self.user.personal_birthday, 'DD.MM') == date).all()
        for usr in users:
            user = usr.__dict__
            
            if 112 in user['indirect_data']['uf_department']:
                pass
            else:
                if user['active'] and user['photo_file_id'] is not None:
                    print(user)
                    user_info = {}
                    indirect_data = user['indirect_data']
                    list_departs = []
                    if len(indirect_data['uf_department']) != 0:
                        for dep in indirect_data['uf_department']:
                            dep_str = DepartmentModel(dep).find_dep_by_id()
                            for de in dep_str:
                                list_departs.append(de.__dict__['name'])
                    
                            
                    indirect_data['uf_department'] = list_departs
                    # добавляем только нужную информацию
                    user_info = {}
                    user_image = File(user['photo_file_id']).get_users_photo()
                    user_info['id'] = user['id']
                    if user['second_name'] == '' or user['second_name'] is None:
                        user_info['user_fio'] = f'{user['last_name']} {user['name']}'
                    else:
                        user_info['user_fio'] = f'{user['last_name']} {user['name']} {user['second_name']}'
                    user_info['position'] = indirect_data['work_position']
                    user_info['department'] = indirect_data['uf_department']
                    if "uf_usr_department_main" in indirect_data:
                        dedep = DepartmentModel(indirect_data["uf_usr_department_main"]).find_dep_by_id()
                        user_info['uf_usr_department_main'] = dedep[0].name
                    user_info['image'] =  f'http://intranet.emk.org.ru{user_image['URL']}'
                    
                    normal_list.append(user_info)
        return normal_list

    def new_workers(self):
        # query = select().select_from(demo_view).order_by(demo_view.c.created_at)
        result = self.db.execute(select(NewUser)).fetchall() # приносит кортеж, где индекс(0) - id, индекс(1) - active, индекс(2) - last_name, индекс(3) - name, индекс(4) - second_name,
        # индекс(5) - dat, индекс(6) - indirect_data, индекс(7) - photo_file_id
        
        users = []
        for res in result:
            
            user = list(res)
            
            if 112 in user[6]['uf_department']:
                pass
            else:
                if user[1] and user[7] is not None:
                    user_info = {}
                    indirect_data = user[6]
                    list_departs = []
                    if len(indirect_data['uf_department']) != 0:
                        for dep in indirect_data['uf_department']:
                            dep_str = DepartmentModel(dep).find_dep_by_id()
                            for de in dep_str:
                                list_departs.append(de.__dict__['name'])
                    if "uf_usr_department_main" in indirect_data:
                        dedep = DepartmentModel(indirect_data["uf_usr_department_main"]).find_dep_by_id()
                        indirect_data["uf_usr_department_main"] = dedep[0].name
                    indirect_data['uf_department'] = list_departs
                    # добавляем только нужную информацию
                    user_info = {}
                    user_image = File(user[7]).get_users_photo()
                    
                    user_info['id'] = user[0]
                    if user[4] == '' or user[4] is None:
                        user_info['user_fio'] = f'{user[2]} {user[3]}'
                    else:
                        user_info['user_fio'] = f'{user[2]} {user[3]} {user[4]}'
                    user_info['position'] = indirect_data['work_position']
                    user_info['department'] = indirect_data['uf_department']
                    user_info['image'] = f'http://intranet.emk.org.ru{user_image['URL']}'
                    users.append(user_info)
        return users
    """
    def put_uf_depart(self, usr_dep):
        
        Выводит пользователей и их uf_department
        
        all_users = []
        print('Выполняю запрос')
        users = self.db.execute(select(self.user)).scalars().all()
        print('Запрос выполнен')
        for user in users:
            
            if user is not None:
                result = dict()
                user_id = getattr(user, 'id', None)
                user_indirict = getattr(user, 'indirect_data')
                result['id'] = user_id
                result['uf_department'] = user_indirict['uf_department']
                for deps_id in result:
                    #проверка
                    #если пользователь есть
                    #если нет - добавить
                # if len(result['uf_department']) > 1:
                #     print(f'у чувака {user_id} НЕСКОЛЬКО ({len(result['uf_department'])}) департаментов')
                # elif len(result['uf_department']) == 0:
                #     print(f'у чувака {user_id} 0 департаментов')
                all_users.append(result)
            else:
                return f'пустой'
        return all_users """



class DepartmentModel():
    def __init__(self, Id=None): #убрать None в будущем
        self.id = Id
        self.department = Department

        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autoflush=True, bind=engine)
        self.db = SessionLocal()

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
    
    def all(self):
        return self.db.query(self.department).all()



class UsDepModel():
    def __init__(self, id=0, user_id=0, dep_id=0):
        self.id = id
        self.user_id = user_id
        self.dep_id = dep_id
        self.us_dep = UsDep

        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autoflush=True, bind=engine)
        self.db = SessionLocal()
    
    def put_uf_depart(self, usr_dep):
        """
        Принимает данные с битрикса. Сравнивает юзеров с б24 и с таблицы users.
        Сравнивает значения depart_id с таблицы users, departaments, с б24 и добавляет в таблицу usdep значения user_id и их departments если все проверки пройдены
        """

        # все пользователи из таблицы users
        users = self.db.execute(select(User.id)).scalars().all() # возвращает все id в виде [1, 11, 61 ...]
        
        # все департаменты из таблицы users
        departs_from_users_table = self.db.execute(select(User.indirect_data['uf_department'])).scalars().all() # возвращает в виде [[642], [642], [94], [94], [94], [483], [86]]
        departs_from_users_table = [item[0] for item in departs_from_users_table] # сразу преобразовали в рабочий вид [642, 642, 94, 94, 94, 483, 86]
        
        # все департаменты из таблицы departments
        departs = self.db.execute(select(Department.id)).scalars().all() # возвращает все id в виде [1, 11, 61 ...]

        # все пользователи из таблицы usdep
        users_from_usdep_table = self.db.execute(select(self.us_dep.user_id)).scalars().all()

        # все департаменты из таблицы usdep
        departs_from_usdep_table = self.db.execute(select(self.us_dep.dep_id)).scalars().all()
        
        # проверка на наличия пользователя в таблицах users и departments
        for us_dep_key, us_dep_value in usr_dep.items():
            #преобразуем [11] в 11 или оставляем [11, 12]
            if len(us_dep_value) > 1:
                pass
            else: 
                us_dep_value = us_dep_value[0]
            

            # если такого пользователя нет в таблице users - ошибка
            if us_dep_key not in users:
                return {'err' : [{'Пользователя нет в таблице users' : us_dep_key}]}
            else:
                # если есть такой пользователь в таблице users - проверяем есть ли он в таблице usdep
                if us_dep_key not in users_from_usdep_table:
                    # добавляем в таблицу usdep
                    self.db.execute(insert(self.us_dep).values(user_id=us_dep_key))
                    self.db.commit()
                    
                # если такой пользователь есть в таблице usdep, проверяем dep_id из Битрикса  в таблицах users, departs, us_deps
                else:
                    # проверяем есть ли департамент из таблицы users в таблице departs
                    for dep_frm_usr in departs_from_users_table:
                        if isinstance(dep_frm_usr, int):
                            if dep_frm_usr not in departs:
                                #print({'err' : [{'такого департамента из таблицы users нет в таблице departments' : dep_frm_usr}]}) 
                                continue
                            # если есть
                            else:
                                pass
                            
                        else:
                            # если департамента из таблицы users в таблице departs нет
                            
                            for i in dep_frm_usr:
                                if i not in departs:
                                    return {'err' : [{f'такого департамента {i} из таблицы users нет в таблице departments' : us_dep_key}]}
                                else:
                                    pass
                    
                    # проверяем департамент в Б24 и в users. Если департаменты разные - ошибка.
                    depart_from_user = self.db.execute(select(User.indirect_data['uf_department']).where(User.id == us_dep_key)).scalar()
                    if isinstance(us_dep_value, int):
                        if isinstance(depart_from_user, int):
                            if us_dep_value != depart_from_user:
                                return {'err' : [{f'Департамент в Б24 {us_dep_value} не равен департаменту в таблице users {depart_from_user}' : us_dep_key}]}
                            else:
                                pass # департаменты в б24 и в таблице юзерс равны по текущему индексу
                        elif len(depart_from_user) > 1:
                            return {'err' : [{f'Департаментов {us_dep_value} у пользователя в битриксе меньше чем в таблице users {us_dep_key}' : depart_from_user}]}
                    elif len(us_dep_value) > 1:
                        if isinstance(depart_from_user, int):
                            return {'err' : [{f'Департаментов {us_dep_value} у пользователя в битриксе больше чем в таблице users {us_dep_key}' : depart_from_user}]}
                        elif len(depart_from_user) > 1: # если значений департамента к одному пользоватлю несколько (таблица users)
                            for i in us_dep_value:
                                if i not in depart_from_user:
                                    return {'err' : [{f'Такого значения департамента из битрикса нет у пользователя {us_dep_key}' : i}]}
                                else:
                                    pass # департаменты одинаковы у пользователя в таблице и в Б24

                    
                    # после всех проверок если пользователь в Б24 есть в таблице users и их департаменты равны, то проверяем есть ли департамент из б24 в usdep
                    dep_from_usdep_table = self.db.execute(select(UsDep.dep_id).where(UsDep.user_id == us_dep_key)).scalars().all()
                   
                    # если значение dep_id по данному user_id отсутствует, то просто добавляем все проверенные значения из б24
                    if dep_from_usdep_table[0] is None:
                        # если из б24 только одно значение
                        if isinstance(us_dep_value, int):
                            self.db.execute(update(UsDep).values(dep_id=us_dep_value).where(UsDep.user_id == us_dep_key))
                        # если из б24 значения в виде списка
                        else:
                            for i, k in enumerate(us_dep_value):
                                # заменяем Null на значение
                                if i == 0:
                                    self.db.execute(update(UsDep).values(dep_id=k).where(UsDep.user_id == us_dep_key))
                                # все остальные просто добавляем
                                else:
                                    tbl = UsDep(user_id=us_dep_key, dep_id=k)
                                    self.db.add(tbl)
                        
                        self.db.commit()
                    # для всех остальных значений, когда dep_from_usdep_table не None
                    else:
                        if len(dep_from_usdep_table) > 1:
                            pass
                        else:
                            dep_from_usdep_table = dep_from_usdep_table[0]
                    
                        # проверка если из б24 по данному id только одно значение dep_id
                        if isinstance(us_dep_value, int):
                            # если в таблице usdep тоже только одно значение и если они не равны со значением из б24, то заменяем на значение из б24
                            if isinstance(dep_from_usdep_table, int):
                                if us_dep_value != dep_from_usdep_table:
                                    self.db.execute(update(UsDep).values(dep_id=us_dep_value).where(UsDep.user_id == us_dep_key))
                                    
                                else:
                                    pass
                            # если в таблице usdep несколько значений dep_id, то оставляем только то что равно значению dep_id из б24, остальные удаляем
                            elif len(dep_from_usdep_table) > 1:
                                for i in dep_from_usdep_table:
                                    if i != us_dep_value:
                                        self.db.execute(delete(UsDep).where(UsDep.user_id == us_dep_key).where(UsDep.dep_id == i))
                                        dep_from_usdep_table.remove(i)
                                    else:
                                        pass
                                # если список значений из таблицы usdep пустой, значит добавляем значение из б24
                                if dep_from_usdep_table == []:
                                    tbl = UsDep(user_id=us_dep_key, dep_id=us_dep_value)
                                    self.db.add(tbl)
                                    
                                else:
                                    pass
                            self.db.commit()
                        # если в б24 по данному user_id список значений
                        elif len(us_dep_value) > 1:
                            #сравниваем с единственным значением в таблице usdep
                            if isinstance(dep_from_usdep_table, int):
                                count = 0
                                for i in us_dep_value:
                                    if i == dep_from_usdep_table: 
                                        count += 1                                   
                                        pass
                                    # если не равно, то добавляем
                                    else:
                                        tbl = UsDep(user_id=us_dep_key, dep_id=i)
                                        self.db.add(tbl)
                                        
                                # если ни одно значение из б24 не сошлось со значением из таблицы, то удаляем его из таблицы
                                if count == 0:
                                    self.db.execute(delete(UsDep).where(UsDep.user_id == us_dep_key).where(UsDep.dep_id == dep_from_usdep_table))
                                else:
                                    pass
                                self.db.commit()
                            
                            # если в таблице usdep содержится спиксок значений
                            elif len(dep_from_usdep_table) > 1:
                                for i in dep_from_usdep_table:
                                    # если одного из значений из usdep нет в списке значений с б24, удаляем с таблицы
                                    if i not in us_dep_value:
                                        self.db.execute(delete(UsDep).where(UsDep.user_id == us_dep_key).where(UsDep.dep_id == i))
                                        self.db.commit()
                                        dep_from_usdep_table.remove(i)
                                    else:
                                        # если есть, удаляем со списка значений б24, чтобы оставить тока исключительные
                                        us_dep_value.remove(i)
                                # если все значения из usdep есть в списке значений из б24, пропускаем итерацию
                                if us_dep_value == []:
                                    pass
                                # если нет, то добавляем новые значения в таблицу usdep
                                else:
                                    if len(us_dep_value) > 1:
                                        for i in us_dep_value:
                                            tbl = UsDep(user_id=us_dep_key, dep_id=i)
                                            self.db.add(tbl)
                                    else:
                                        tbl = UsDep(user_id=us_dep_key, dep_id=us_dep_value[0])
                                        self.db.add(tbl)
                                    self.db.commit()                         
        
        return True

    def find_dep_by_user_id(self):
        """
        Выдает данные по департаментам пользователя
        """
        res = self.db.execute(select(self.us_dep).where(self.us_dep.user_id == self.id)).scalars().all()
        print(res)
        if res != []:
            return [res]
        else:
            return {'err' : "Invalid user id"}
    
    def find_user_by_dep_id(self):
        """
        Выдает id пользователей по id департамента
        """
        users = self.db.execute(select(self.us_dep).where(self.us_dep.dep_id == self.id)).scalars().all()
        if users != []:
            res = []
            for usr in users:
                res.append(usr.user_id)
            return res
        else:
            return {'err' : "Invalid user id"}



class SectionModel():

    def __init__(self, id=0, name="", parent_id=0):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def upload(self, section_data):
        for section in section_data:
            sec = db.query(Section).filter(Section.id == section["id"]).first()

            if sec is not None:
                #надо ли обновить?
                if sec.name != section["name"]:
                   sec.name = section["name"]
                if sec.parent_id != section["parent_id"]:
                    sec.parent_id = section["parent_id"]
            else:
                sec = Section(id=section["id"], name=section["name"], parent_id=section["parent_id"])
            db.add(sec)
            db.commit()

        return section_data

    def search_by_id(self):
        return db.query(Section).filter(Section.id == self.id).first()

    def search_by_parent_id(self):
        return db.query(Section).filter(Section.parent_id == self.parent_id).all()



class ArticleModel():

    def __init__(self, id=0, section_id=0):
        self.id = id
        self.section_id = section_id
        self.article = Article

    def add_article(self, article_data):
        article = Article(**article_data)
        db.add(article)
        db.commit()

        return article_data

    def need_add(self):
        db_art = db.query(Article).filter(Article.section_id == self.section_id).all()
        # если в таблице есть раздел
        if db_art != []:
            need = True
            for art in db_art:
                # добавить статью в таблицу, если её там нет
                if int(art.id) == int(self.id):
                    need = False
                    # print("Такой раздел уже есть", self.id)
            return need

        # если в таблице нет статей раздела
        else:
            return True

    def reassembly(self, article_data):
        #удалить статью
        db.query(Article).get(self.id).delete()
        #залить заново
        self.add_article(article_data)

    def update(self, article_data):
        db_art = db.query(Article).get(self.id).__dict__
        for key in article_data:
            if key not in ["ID", "_sa_instance_state"]:
                if key not in db_art:
                    self.reassembly(article_data)
                    LogsMaker().warning_message(f'{db_art['id']} добавить {key} = {article_data[key]}')
                    # print(db_art['id'], "добавить", key, "=", article_data[key])
                    return True
                elif article_data[key] != db_art[key]:
                    self.reassembly(article_data)
                    LogsMaker().warning_message(f'{db_art['id']} {key} {db_art[key]} --> {article_data[key]}')
                    # print(db_art['id'], key, db_art[key], "-->", article_data[key])
                    return True
                else:
                    return False



    def find_by_id(self):
        art = db.query(Article).get(self.id)
        try:
            art.__dict__["indirect_data"] = json.loads(art.indirect_data)
        except:
            if art is not None:
                art.__dict__["indirect_data"] = art.indirect_data
            else:
                return dict()
        return art.__dict__

    def find_by_section_id(self):
        
        data = db.query(Article).filter(Article.section_id == self.section_id).all()
        new_data = []
        try:
            for art in data:
                art.__dict__["indirect_data"] = json.loads(art.indirect_data)
                new_data.append(art.__dict__)
        except:
            for art in data:
                art.__dict__["indirect_data"] = art.indirect_data
                new_data.append(art.__dict__)

        return new_data
    
    def all(self):
        data = db.query(Article).all()
        new_data = []
        try:
            for art in data:
                art.__dict__["indirect_data"] = json.loads(art.indirect_data)
                new_data.append(art.__dict__)
        except:
            for art in data:
                art.__dict__["indirect_data"] = art.indirect_data
                new_data.append(art.__dict__)

        
        return new_data



class LikesModel:
    def __init__(self, user_id: Optional[int] = None, art_id: Optional[int] = None, user_uuid: Optional[str] = None):
        self.session = db
        self.user_id = user_id
        self.art_id = art_id
        self.user_uuid = user_uuid

    def add_or_remove_like(self ) -> bool:
        """
        Ставит лайк статье если пользователь его еще не ставил
        Убрает лайк со статьи
        Меняет статус лайка
        """
        reactions = {}
        # Проверяем, есть ли уже активный лайк
        existing_like = self.session.query(Likes).filter(
            Likes.user_id == self.user_id,
            Likes.article_id == self.art_id
        ).first()
        views = ViewsModel(art_id=self.art_id).get_art_viewes()
        if not existing_like:
            # создаем новый лайк если прежде никогда не стоял
            new_like = Likes(
                user_id=self.user_id,
                article_id=self.art_id,
                is_active=True,
                created_at=datetime.utcnow()
            )
            self.session.add(new_like)
            self.session.commit()
            likes_count = self.get_likes_count()

            likes = {'count': likes_count, 'likedByMe': True}
            reactions['views'] = views
            reactions['likes'] = likes
            return reactions

        elif existing_like.is_active is False:
            # если лайк не был поставлен, ставим
            existing_like.is_active = True
            self.session.commit()
            likes_count = self.get_likes_count()

            likes = {'count': likes_count, 'likedByMe': True}
            reactions['views'] = views
            reactions['likes'] = likes
            return reactions

        elif existing_like.is_active is True:
            # если лайк был поставлен, убираем
            existing_like.is_active = False
            self.session.commit()

            likes_count = self.get_likes_count()

            likes = {'count': likes_count, 'likedByMe': False}
            reactions['views'] = views
            reactions['likes'] = likes
            return reactions


    def has_liked(self ) -> bool:
        """
        Проверяет, поставил ли пользователь лайк статье.
        """
        reactions = {}
        # Проверяем, есть ли уже активный лайк
        existing_like = self.session.query(Likes).filter(
            Likes.user_id == self.user_id,
            Likes.article_id == self.art_id
        ).first()
        views = ViewsModel(art_id=self.art_id).get_art_viewes()
        if not existing_like:
            # если лайк никогда не существовал, значит False
            likes_count = self.get_likes_count()

            likes = {'count': likes_count, 'likedByMe': False}
            reactions['views'] = views
            reactions['likes'] = likes
            return reactions

        elif existing_like.is_active is False:
            # если лайк не был поставлен, но когда то стоял возвращаем False
            likes_count = self.get_likes_count()

            likes = {'count': likes_count, 'likedByMe': False}
            reactions['views'] = views
            reactions['likes'] = likes
            return reactions

        elif existing_like.is_active is True:
            # если лайк был поставлен, возвращаем True

            likes_count = self.get_likes_count()

            likes = {'count': likes_count, 'likedByMe': True}
            reactions['views'] = views
            reactions['likes'] = likes
            return reactions
        # return self.session.query(Likes).filter(
        #     Likes.user_id == self.user_id,
        #     Likes.article_id == self.art_id,
        #     Likes.is_active == True
        # ).count() > 0

    def get_likes_count(self ) -> int:
        """
        Возвращает количество активных лайков для статьи.
        """
        return self.session.query(Likes).filter(
            Likes.article_id == self.art_id,
            Likes.is_active == True
        ).count()

    def get_user_likes(self ) -> List[int]:
        """
        Возвращает список ID статей, которые лайкнул пользователь.

        Args:
            user_id: ID пользователя

        Returns:
            Список article_id, которые пользователь лайкнул
        """
        likes = self.session.query(Likes.article_id).filter(
            Likes.user_id == self.user_id,
            Likes.is_active == True
        ).all()

        return [like.article_id for like in likes]

    def get_article_likers(self ) -> List[int]:
        """
        Возвращает список ID пользователей, которые лайкнули статью.

        Args:
            art_id: ID статьи

        Returns:
            Список user_id пользователей, которые лайкнули статью
        """
        likers = self.session.query(Likes.user_id).filter(
            Likes.article_id == self.art_id,
            Likes.is_active == True
        ).all()

        return [liker.user_id for liker in likers]

    def add_like_from_b24(self, created_at) -> bool:
        """
        Пользователь поставил лайк статье.
        Возвращает True, если лайк успешно добавлен, False если лайк уже существует.
        """
        # Проверяем, есть ли уже активный лайк
        existing_like = self.session.query(Likes).filter(
            Likes.user_id == self.user_id,
            Likes.article_id == self.art_id,
            Likes.is_active == True
        ).first()

        if existing_like:
            return False  # Лайк уже существует

        # Если лайк был, но is_active=False, обновляем его
        # inactive_like = self.session.query(Likes).filter(
        #     Likes.user_id == self.user_id,
        #     Likes.article_id == self.art_id,
        #     Likes.is_active == False
        # ).first()

        # if inactive_like:
        #     inactive_like.is_active = True
        #     inactive_like.created_at = datetime.utcnow()
        # else:
            # Создаем новый лайк
        new_like = Likes(
            user_id=self.user_id,
            article_id=self.art_id,
            is_active=True,
            created_at=created_at
        )
        self.session.add(new_like)

        self.session.commit()
        return True

    # def has_liked_by_uuid(self): 
    #     user = self.session.query(User).filter(User.uuid == self.user_uuid).subquery()
    #     stmt = select(Likes.article_id).where(Likes.user_id == user.с.id)
    #     result = self.session.execute(stmt).fetchall()
    #     return [re for re in result]

    @classmethod
    def get_popular_articles(cls, limit: int = 10) -> List[Dict[str, int]]:
        """
        Возвращает список самых популярных статей по количеству лайков

        Args:
            session: SQLAlchemy сессия
            limit: Количество возвращаемых статей

        Returns:
            Список словарей с данными статей:               @self.session
            [{'article_id': int, 'likes_count': int}, ...]
        """
        popular_articles = db.query(
            Likes.article_id,
            func.count(Likes.id).label('likes_count')
        ).filter(
            Likes.is_active == True
        ).group_by(
            Likes.article_id
        ).order_by(
            desc('likes_count')
        ).limit(limit).all()

        return [{
            'article_id': article.article_id,
            'likes_count': article.likes_count
        } for article in popular_articles]

    @classmethod
    def get_recent_popular_articles(cls, days: int = 30, limit: int = 10):
        """
        Возвращает популярные статьи за последние N дней
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        popular = db.query(
            Likes.article_id,
            func.count(Likes.id).label('likes_count')
        ).filter(
            Likes.is_active == True,
            Likes.created_at >= cutoff_date
        ).group_by(
            Likes.article_id
        ).order_by(
            desc('likes_count')
        ).limit(limit).all()

        return [dict(article_id=row.article_id, likes_count=row.likes_count) for row in popular]

class ViewsModel:
    def __init__(self, views_count: Optional[int] = None, art_id: Optional[int] = None):
        self.session = db
        self.views_count = views_count
        self.art_id = art_id

    def add_view_b24(self ) -> None:
        """
        Добавляет запись о количестве просмотров статьи
        """
        existing_view = self.session.query(Views).where(Views.article_id == self.art_id).first()

        if existing_view:
            existing_view.viewes_count = self.views_count
            self.session.commit()
            return {"msg": "существует"}  # Лайк уже существует
        else:
            new_view = Views(
                article_id=self.art_id,
                viewes_count=self.views_count
            )
            self.session.add(new_view)
            self.session.commit()
            return {"msg": "добавили"}

    def get_art_viewes(self):
        """
        Возвращает количество просмотров у данной статьи
        """
        return self.session.query(Views.viewes_count).where(
            Views.article_id == self.art_id
        ).scalar()
    
    def add_art_view(self):
        """
        Добавляет просмотр к статье и возвращает итоговое количество просмотров у статьи
        """
        existing_view = self.session.query(Views).where(Views.article_id == self.art_id).first()
        if existing_view:
            existing_view.viewes_count = existing_view.viewes_count + 1
            self.session.commit()
            return {"views": existing_view.viewes_count}
        else:
            new_view = Views(
                article_id=self.art_id,
                viewes_count=1
            )
            self.session.add(new_view)
            self.session.commit()
            return {"views": new_view.viewes_count}


