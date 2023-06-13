from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    user_id: int
    video_id: int
    parent_id: int
    text: str
    created_at: datetime
    updated_at: datetime


class AddComment(BaseModel):
    text: str
