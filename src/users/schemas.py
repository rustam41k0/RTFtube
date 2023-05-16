from datetime import datetime
from typing import Optional, List

from fastapi_users import schemas
from pydantic import BaseModel

from src.videos.schemas import GetVideo


class UserRead(schemas.BaseUser[int]):
    username: str
    channel_description: str
    registered_at: datetime


class UserCreate(schemas.BaseUserCreate):
    username: str
    channel_description: str
    registered_at: datetime


class GetUser(BaseModel):
    username: str
    channel_description: str
    registered_at: datetime
    video: List[GetVideo]


class Subscription(BaseModel):
    user_id: int
    subscribed_to_id: int


class UserUpdate(BaseModel):
    username: Optional[str] = None
    channel_description: Optional[str] = None
