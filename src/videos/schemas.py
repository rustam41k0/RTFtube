from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GetVideo(BaseModel):
    id: int
    author_id: int
    title: str
    description: str
    views: int
    url: str
    created_at: datetime
    updated_at: datetime


class UpdateVideo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class UploadVideo(BaseModel):
    title: str
    description: str
    url: str
