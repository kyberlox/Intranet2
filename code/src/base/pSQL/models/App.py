# Определим базовые переменные пакета
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

from src.services.LogsMaker import LogsMaker

load_dotenv()

ADMINS_PEER = []

DOMAIN = os.getenv('HOST')

user = os.getenv('user')
pswd = os.getenv('pswd')

# Настройка подключения к базе данных PostgreSQL
engine = create_engine(f'postgresql+psycopg2://{user}:{pswd}@postgres/pdb', pool_size=50, max_overflow=0)

try:  
    engine.connect()
    LogsMaker().ready_status_message("pSQL успешно подключен!")
except Exception as ex: 
    LogsMaker().fatal_message(f"Ошибка подключения pSQL: {ex}")

Base = declarative_base()
Base.metadata.create_all(engine)