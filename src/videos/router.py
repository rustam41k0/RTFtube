from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import get_current_user
from src.users.models import User
from .models import Video
from src.database import get_async_session
from .schemas import GetVideo, UpdateVideo, UploadVideo

router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)


@router.get("", name='get_all_videos')  # , response_model=List[GetVideo])
async def get_all_videos(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Video)
        result = await session.execute(query)
        return result.mappings().all()

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})


@router.get("/{video_id}", name='get_video')  # , response_model=GetVideo)
async def get_video(video_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        video = await session.get(Video, video_id)
        return video

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})


@router.post("", name='upload_video')
async def upload_video(
        video_info: UploadVideo,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_video = Video(author_id=current_user.id,
                          title=video_info.title,
                          description=video_info.description,
                          url=video_info.url,
                          views=0)
        session.add(new_video)
        await session.commit()
        return {'status': 'Success'}

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})


@router.put("/{video_id}", name='update_video')
async def update_video(
        video_id: int,
        video: UpdateVideo,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        updated_video = await session.get(Video, video_id)
        if not updated_video:
            return {"error": "Video not found"}
        if video.title:
            updated_video.title = video.title
        if video.description:
            updated_video.description = video.description
        await session.commit()
        await session.refresh(updated_video)
        return {"message": "Video updated successfully",
                "video": updated_video}

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})


@router.delete("/{video_id}", name='delete_video')
async def delete_video(
        video_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        video_for_delete = await session.get(Video, video_id)
        if video_for_delete.author_id != current_user.id:
            return {"error": "Oops, you are not allowed to do that!"}
        if not video_for_delete:
            return {"error": "Video not found"}
        await session.delete(video_for_delete)
        await session.commit()
        return {"message": f'Video "{video_for_delete.title}" deleted successfully'}

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})
