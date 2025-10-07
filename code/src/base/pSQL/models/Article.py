from sqlalchemy import Column, Integer, Text, Boolean, String, DateTime
from sqlalchemy.orm import  relationship
from sqlalchemy.dialects.postgresql import JSONB

from .App import Base
from .Likes import Likes
from .Views import Views

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, nullable=True)
    name = Column(Text, nullable=True)
    active = Column(Boolean, nullable=True, default=True)
    preview_text = Column(Text, nullable=True)
    content_text = Column(Text, nullable=True)
    content_type = Column(String, nullable=True)
    date_publiction = Column(DateTime, nullable=True)
    date_creation = Column(DateTime, nullable=True)
    indirect_data = Column(JSONB, nullable=True)
    #preview_image_url = Column(Text, nullable=True)

    # Отношения для лайков и просмотров
    likes = relationship("Likes", back_populates="article")
    views = relationship("Views", back_populates="article")
    artvis = relationship("ArtVis", back_populates="article")