from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import  relationship

from .App import Base

class ArtVis(Base):
    """
    Класс для связи области видимости и статей
    """
    __tablename__ = 'artvis'
    id = Column(Integer, primary_key=True)
    vision_id = Column(Integer, ForeignKey('fieldvision.id', ondelete="CASCADE"), nullable=True)
    art_id = Column(Integer, ForeignKey('article.id', ondelete="CASCADE"), nullable=True)

    fieldvision = relationship("Fieldvision", back_populates="artvis")
    article = relationship("Article", back_populates="artvis")