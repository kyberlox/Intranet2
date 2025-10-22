# Определим базовые переменные пакета
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.ext.asyncio import async_sessionmaker # AsyncSession, 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import os
import time
from dotenv import load_dotenv

from src.services.LogsMaker import LogsMaker

load_dotenv()

ADMINS_PEER = []

DOMAIN = os.getenv('HOST')

user = os.getenv('user')
pswd = os.getenv('pswd')

# Настройка подключения к базе данных PostgreSQL
# engine = create_engine(f'postgresql+psycopg2://{user}:{pswd}@postgres/pdb', pool_size=50, max_overflow=0)

# try:  
#     engine.connect()
#     LogsMaker().ready_status_message("pSQL успешно подключен!")
# except Exception as ex: 
#     LogsMaker().fatal_message(f"Ошибка подключения pSQL: {ex}")

def create_db_engine():
    max_retries = 5
    retry_delay = 5
    
    for i in range(max_retries):
        try:
            engine = create_engine(f'postgresql+psycopg2://{user}:{pswd}@postgres/pdb', pool_size=50, max_overflow=0)
            connection = engine.connect()
            LogsMaker().ready_status_message("pSQL успешно подключен!")
            connection.close()
            return engine
        except Exception as e:
            LogsMaker().warning_message(f"❌ Connection attempt {i+1}/{max_retries} failed: {e}")
            if i < max_retries - 1:
                LogsMaker().info_message(f"🕐 Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    LogsMaker().fatal_message("Failed to connect to PostgreSQL after multiple attempts")

engine = create_db_engine()

Base = declarative_base()
Base.metadata.create_all(engine)



def create_async_db_engine():
    max_retries = 5
    retry_delay = 5
    
    for i in range(max_retries):
        try:
            # Используем asyncpg драйвер для асинхронной работы
            engine = create_async_engine(
                f'postgresql+asyncpg://{user}:{pswd}@postgres/pdb',
                pool_size=50,
                max_overflow=0,
                echo=False  # Можно включить для отладки SQL запросов
            )
            LogsMaker().ready_status_message("Асинхронный pSQL движок успешно создан!")
            return engine
        except Exception as e:
            LogsMaker().warning_message(f"❌ Async connection attempt {i+1}/{max_retries} failed: {e}")
            if i < max_retries - 1:
                LogsMaker().info_message(f"🕐 Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    LogsMaker().fatal_message("Failed to create async PostgreSQL engine after multiple attempts")

# Создаем асинхронный движок
async_engine = create_async_db_engine()

# Асинхронная сессия
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=True
)

# Base = declarative_base()
# Функция для создания таблиц (вызывается при старте приложения)
# async def create_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     LogsMaker().info_message("Таблицы успешно созданы/проверены")