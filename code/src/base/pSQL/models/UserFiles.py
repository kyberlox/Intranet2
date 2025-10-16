from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import  relationship

from .App import Base
from .User import User



class UserFiles(Base):
    __tablename__ = 'userFiles'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    b24_url = Column(Text, nullable=True)
    active = Column(Boolean, nullable=True)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Отношения втарок и пользователей
    user = relationship("User", back_populates="userFiles")