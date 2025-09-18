from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import  relationship

from .App import Base



class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    father_id = Column(Integer, nullable=True)
    user_head_id = Column(Integer, nullable=True)
    sort = Column(Integer, nullable=True)

    usdep = relationship("UsDep", back_populates="depart")