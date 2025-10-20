from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import  relationship

from .App import Base
from .Article import Article



class UserFiles(Base):
    __tablename__ = 'userFiles'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=True)
    original_name = Column(Text, nullable=True)
    stored_name = Column(Text, nullable=True)
    b24_url = Column(Text, nullable=True)
    active = Column(Boolean, nullable=True)
    content_type = Column(Text, nullable=True)

    article_id = Column(Integer, ForeignKey('article.id'), nullable=False)

    # Отношения файлоы и статей
    article = relationship("Article", back_populates="articleFiles")