from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

import datetime
from datetime import datetime

from .App import Base
from .User import User


class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)  # ID пользователя
    article_id = Column(Integer, ForeignKey('article.id', ondelete="CASCADE"), nullable=False)  # ID статьи
    created_at = Column(DateTime, default=datetime.utcnow)  # Время создания лайка
    is_active = Column(Boolean, default=True)  # Флаг активности лайка (можно убирать лайки)

    # Опциональные отношения для удобства доступа
    user = relationship("User", back_populates="likes")
    article = relationship("Article", back_populates="likes")
