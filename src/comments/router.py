from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.comments.schemas import AddComment
from src.auth.base_config import get_current_user
from src.comments.models import Comment
from src.database import get_async_session
from src.users.models import User

router = APIRouter(
    prefix='/videos',
    tags=["Comments"],
)


@router.get("/{video_id}/comments")
async def get_video_comments(video_id: int,
                             session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Comment).where(Comment.video_id == video_id)
        result = await session.execute(query)
        return result.mappings().all()

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})


@router.post("/{video_id}/comments")
async def add_comment(video_id: int,
                      comment: AddComment,
                      current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_async_session)):
    try:
        new_comment = Comment(user_id=current_user.id, video_id=video_id, text=comment.text)
        session.add(new_comment)
        await session.commit()
        return {'comment': comment.text}

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})
