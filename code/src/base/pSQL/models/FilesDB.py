from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .App import Base

class FilesDB(Base):
    __tablename__ = 'filesdb'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    original_name = Column(Text, nullable=True)
    stored_name = Column(Text, nullable=True)
    b24_url = Column(Text, nullable=True)
    active = Column(Boolean, nullable=True)
    is_preview = Column(Boolean, nullable=True)
    content_type = Column(Text, nullable=True)
    file_url = Column(Text, nullable=True)
    article_id = Column(Integer, ForeignKey('article.id'), nullable=False)

    # Отношение к статье
    article = relationship("Article", back_populates="artfiles")  # Исправлено на artfiles