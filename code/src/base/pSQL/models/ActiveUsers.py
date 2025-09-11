from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .App import Base

class ActiveUsers(Base):
    __tablename__ = "activeusers"
  
    id = Column(Integer, primary_key=True)
    uuid_from = Column(Integer, nullable=True)
    uuid_to = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    valid = Column(Integer, nullable=True)
    date_time = Column(DateTime, nullable=True)
    activities_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)

    activities = relationship("Activities", back_populates="activeusers")