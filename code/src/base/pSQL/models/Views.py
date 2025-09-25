from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import  relationship

from .App import Base

class Views(Base):
    """
    Класс для хранения просмотров пользователями статей.
    Связывает пользователей (User) и статьи (Article) многие-ко-многим.
    """
    __tablename__ = 'views'

    id = Column(Integer, primary_key=True)
    #user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID пользователя
    article_id = Column(Integer, ForeignKey('article.id', ondelete="CASCADE"), nullable=False)  # ID статьи
    viewes_count = Column(Integer, nullable=False)  # Время просмотра

    # Опциональные отношения для удобства доступа
    #user = relationship("User", back_populates="views")
    article = relationship("Article", back_populates="views")