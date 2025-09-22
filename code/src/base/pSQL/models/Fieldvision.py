from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import  relationship

from .App import Base
# from .UservisionsRoot import UservisionsRoot

class Fieldvision(Base):
    """
    Класс для хранения области видимости
    """
    __tablename__ = 'fieldvision'
    id = Column(Integer, primary_key=True)
    vision_name = Column(Text, nullable=True)

    # uservisionsroot = relationship("UservisionsRoot", back_populates="fieldvision")