from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import  relationship

from .App import Base

class UservisionsRoot(Base):
    """
    Класс для хранения области видимости
    """
    __tablename__ = 'uservisionsroot'
    id = Column(Integer, primary_key=True)
    vision_id = Column(Integer, ForeignKey('fieldvision.id', ondelete="CASCADE"), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    fieldvision = relationship("Fieldvision", back_populates="uservisionsroot")
    user = relationship("User", back_populates="uservisionsroot")