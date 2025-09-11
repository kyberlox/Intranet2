from sqlalchemy import create_engine, Column, Integer, Text, Boolean, String, DateTime, JSON, MetaData, Table, ForeignKey, desc, func, Date, or_, and_, over
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import JSONB

from .App import Base

class Tags(Base):
    """
    Класс для хранения тэгов статей
    """
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag_name = Column(Text, nullable=True)