# Определим базовые переменные пакета
from sqlalchemy import MetaData, Table, Column, Integer, Boolean, Text, Date
from sqlalchemy.dialects.postgresql import JSONB

import ..models
#from models.App import Base
#from models.App import engine
from sqlalchemy.orm import sessionmaker

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



Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=True, bind=engine)
db = SessionLocal()