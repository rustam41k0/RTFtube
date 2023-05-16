from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import get_current_user
from src.database import get_async_session
from src.likes.models import Like
from src.users.models import User

router = APIRouter(
    tags=["Likes"]
)


@router.post("/video/{video_id}/like")
async def like_or_unlike_video(video_id: int,
                               cur_user: User = Depends(get_current_user),
                               session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Like).filter(and_(Like.user_id == cur_user.id, Like.video_id == video_id))
        like = await session.execute(query)
        like = like.mappings().all()
        if not like:
            like_for_add = Like(user_id=cur_user.id, video_id=video_id)
            session.add(like_for_add)
            await session.commit()
            return {'status': 'Add like successfully'}
        else:
            like_for_delete = await session.get(Like, like[0]['Like'].id)
            await session.delete(like_for_delete)
            await session.commit()
            return {'status': 'Delete like successfully'}

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})
