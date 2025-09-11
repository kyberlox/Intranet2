from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from .App import Base

class Moders(Base):
    __tablename__ = "moders"

    id = Column(Integer, primary_key=True)
    user_uuid = Column(Text, nullable=True)
    activities_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)

    activities = relationship("Activities", back_populates="moders")