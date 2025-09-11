from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from models import Base


class Section(Base):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    parent_id = Column(Integer, nullable=True)
