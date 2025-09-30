from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import  relationship
from sqlalchemy.dialects.postgresql import JSONB

from .App import Base

class Roots(Base):
    __tablename__ = "Roots"
    id = Column(Integer, primary_key=True)
    user_uuid = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    root_token = Column(JSONB, nullable=True)
    user_points = Column(Integer, nullable=True)

    user = relationship("User", back_populates="rootsusers")