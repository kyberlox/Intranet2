from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.orm import relationship

from .App import Base

class Activities(Base):
    __tablename__ = "activities"
  
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    coast = Column(Integer, nullable=True)
    need_valid = Column(Boolean, nullable=True)

    activeusers = relationship("ActiveUsers", back_populates="activities")
