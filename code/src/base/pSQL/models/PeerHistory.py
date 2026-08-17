from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .App import Base

class PeerHistory(Base):
    __tablename__ = "PeerHistory"
    id = Column(Integer, primary_key=True)
    user_uuid = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    date_time = Column(DateTime, nullable=True)
    merch_info = Column(Text, nullable=True)
    merch_coast = Column(Integer, nullable=True)
    info_type = Column(Text, nullable=True)
    user_to = Column(Integer, nullable=True)
    active_info = Column(Text, nullable=True)
    active_coast = Column(Integer, nullable=True)
    active_id = Column(Integer, ForeignKey("activeusers.id", ondelete="CASCADE"), nullable=True)

    user = relationship("User", back_populates="peerhistory")
    activeusers = relationship("ActiveUsers", back_populates="peerhistory")
