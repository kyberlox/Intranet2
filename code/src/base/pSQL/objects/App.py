# Определим базовые переменные пакета
# from sqlalchemy import MetaData, Table, Column, Integer, Boolean, Text, Date, select, func
from sqlalchemy import MetaData, Table, Column, Integer, Boolean, Text, Date, select, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm.attributes import flag_modified
from ..models.App import Base, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

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