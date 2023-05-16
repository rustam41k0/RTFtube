from sqlalchemy import Column, Integer, ForeignKey

from src.database import Base


class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    video_id = Column(Integer, ForeignKey('video.id'), nullable=True)