from sqlalchemy import create_engine, Column, Integer, Text, Boolean, String, DateTime, JSON, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import exists, select
from sqlalchemy import inspect, text

import json
import datetime
from datetime import datetime


import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('user')
pswd = os.getenv('pswd')
port = os.getenv('PORT')

# Настройка подключения к базе данных PostgreSQL
engine = create_engine(f'postgresql+psycopg2://{user}:{pswd}@postgres/pdb')



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
    personal_mobile = Column(Text, nullable=True)
    uf_phone_inner = Column(Text, nullable=True)
    personal_city = Column(Text, nullable=True)
    personal_gender = Column(String, nullable=True)
    personal_birthday = Column(DateTime, nullable=True)
    indirect_data = Column(JSONB, nullable=True)

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



Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=True, bind=engine)
db = SessionLocal()



class UserModel:
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
                user = db.query(self.user).get(user_data['id'])

                #проверить есть ли изменения
                need_update = False

                #проверка основных параметров
                for column in DB_columns:
                    if user_data.get(column) != user.__dict__[column]:
                        if column == 'personal_birthday':
                            # обработка дат
                            dt_new = datetime.strptime(user_data.get('personal_birthday').split('T')[0], '%Y-%m-%d').date()
                            dt_old = user.personal_birthday.date()
                            if dt_new != dt_old:
                                need_update = True
                                user.__dict__[column] = user_data.get(column)
                                print(column, user_data.get(column))
                        else:
                            need_update = True
                            user.__dict__[column] = user_data.get(column)
                            print(column, user_data.get(column))

                        #print(column, user_data.get(column), user.__dict__[column])

                #проверка доп. параметров
                for key in user_data.keys():
                    if key not in DB_columns:
                        if key not in user.indirect_data:
                            #добавить, если нет
                            user.indirect_data[key] = user_data[key]
                            need_update = True
                            print(key, user_data.get(key))
                        elif user_data[key] != user.indirect_data[key]:
                            #изменить, если требуется
                            user.indirect_data[key] = user_data[key]
                            need_update = True
                            print(key, user_data.get(key))

                #если есть изменения - внести
                if need_update:
                    self.db.commit() #НЕ СРАБАТЫВАЕТ! (

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

        except SQLAlchemyError as e:
            db.rollback()
            print(f"An error occurred: {e}")

    def find_by_id(self):
        user = self.db.query(self.user).get(self.id)
        result = dict()
        DB_columns = ['uuid', 'active', 'name', 'last_name', 'second_name', 'email', 'personal_mobile', 'uf_phone_inner', 'personal_city', 'personal_gender', 'personal_birthday']
        if user in not None:
            for key in DB_columns:
                result[key] = user.__dict__[key]

            result['indirect_data'] = user.indirect_data

            return result

        else:
            return {'err' : "Invalid user id"}





class DepartmentModel():
    def __init__(self, Id):
        self.id = Id

        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autoflush=True, bind=engine)
        self.db = SessionLocal()

    def upsert_dep(self, data):
        print(data)



