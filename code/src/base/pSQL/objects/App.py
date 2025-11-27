# Определим базовые переменные пакета
# from sqlalchemy import MetaData, Table, Column, Integer, Boolean, Text, Date, select, func

from sqlalchemy import MetaData, Table, Column, Integer, Boolean, Text, Date, select, func, update, delete, and_
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm.attributes import flag_modified
from ..models.App import Base, async_engine #, AsyncSessionLocal engine, 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

import os
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv('HOST')

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


# Base = declarative_base()
# Base.metadata.create_all(async_engine)
# Асинхронная сессия
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=True
)

# Base.metadata.create_all(bind=engine)
# SessionLocal = sessionmaker(autoflush=True, bind=engine)
# # db = SessionLocal()
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
