from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import inspect, Table, MetaData

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, uuid={self.uuid})>"

def update_table_structure(engine, fields):
    # Создаем объект MetaData
    metadata = MetaData()

    # Загружаем существующую таблицу
    metadata.reflect(bind=engine, only=['users'])
    users_table = metadata.tables['users']

    # Получаем информацию о существующих столбцах
    inspector = inspect(engine)
    existing_columns = {column['name'] for column in inspector.get_columns('users')}

    # Добавляем новые столбцы, если их нет
    with engine.connect() as connection:
        for field_name, field_type in fields.items():
            if field_name not in existing_columns:
                # Добавляем новый столбец
                connection.execute(f"ALTER TABLE users ADD COLUMN {field_name} {field_type}")
                print(f"Added new column: {field_name}")