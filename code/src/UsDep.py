from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Таблица для связи многие-ко-многим между Пользователем и Подразделением
user_department_association = Table(
    'user_department', Base.metadata,
    Column('user_id', Integer),
    Column('department_id', Integer)
)