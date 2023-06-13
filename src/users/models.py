from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, TIMESTAMP, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Subscriptions(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    subscribed_to = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    channel_description = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
