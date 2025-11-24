from sqlalchemy import Column, Integer, Text, Boolean, String, DateTime
from sqlalchemy.orm import  relationship
from sqlalchemy.dialects.postgresql import JSONB

from .App import Base



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uuid = Column(Text, nullable=True)
    active = Column(Boolean, nullable=True)
    last_name = Column(Text, nullable=True)
    name = Column(Text, nullable=True)
    second_name = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    personal_mobile = Column(Text, nullable=True)
    uf_phone_inner = Column(Text, nullable=True)
    personal_city = Column(Text, nullable=True)
    personal_gender = Column(String, nullable=True)
    personal_birthday = Column(DateTime, nullable=True)
    indirect_data = Column(JSONB, nullable=True)

    photo_file_id = Column(Integer, nullable=True)

    # Отношения для лайков и просмотров
    likes = relationship("Likes", back_populates="user")

    usdep = relationship("UsDep", back_populates="user")

    #userFiles = relationship("userFiles", back_populates="user")


    rootsusers = relationship("Roots", back_populates="user")
    peerhistory = relationship("PeerHistory", back_populates="user")

    uservisionsroot = relationship("UservisionsRoot", back_populates="user")


    userfiles = relationship("UserFiles", back_populates="user")
