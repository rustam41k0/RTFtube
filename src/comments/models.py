from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP

from src.database import Base


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    video_id = Column(Integer, ForeignKey('video.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('comment.id'), nullable=True)
    text = Column(String(length=1000), nullable=False)
    created_at = Column(TIMESTAMP(), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(), default=datetime.utcnow)
