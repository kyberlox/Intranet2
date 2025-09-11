# Определим базовые переменные пакета
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

ADMINS_PEER = []

DOMAIN = os.getenv('HOST')

user = os.getenv('user')
pswd = os.getenv('pswd')

# Настройка подключения к базе данных PostgreSQL
engine = create_engine(f'postgresql+psycopg2://{user}:{pswd}@postgres/pdb', pool_size=50, max_overflow=0)

Base = declarative_base()
Base.metadata.create_all(engine)