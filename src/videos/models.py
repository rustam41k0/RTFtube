from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP

from src.database import Base


class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String(length=5000), nullable=False)
    file = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(), default=datetime.utcnow)
