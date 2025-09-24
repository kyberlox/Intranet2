from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import  relationship

from .App import Base
from .User import User
from .Department import Department


class UsDep(Base):
    __tablename__ = 'usdep'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    dep_id = Column(Integer, ForeignKey('departments.id', ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="usdep")
    depart = relationship("Department", back_populates="usdep")