from pydantic import BaseModel


class Like(BaseModel):
    id: int
    user_id: int
    video_id: int
