from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import  relationship

from .App import Base
from .User import User



class UserFiles(Base):
    __tablename__ = 'userfiles'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    b24_url = Column(Text, nullable=True)
    active = Column(Boolean, nullable=True)
    URL = Column(Text, nullable=True)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Отношения втарок и пользователей
    
    user = relationship("User", back_populates="userfiles")