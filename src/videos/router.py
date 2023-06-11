from typing import List, Dict
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import StreamingResponse

from src.auth.base_config import get_current_user
from src.users.models import User
from .models import Video
from src.database import get_async_session
from .schemas import GetVideo, UpdateVideo, UploadVideo
from .services import write_video, open_file

router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)


@router.get("", name='get_all_videos')
async def get_all_videos(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Video)
        result = await session.execute(query)
        return result.mappings().all()

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})


@router.get("/{video_id}", name='get_video')
async def get_streaming_video(request: Request,
                              video_id: int,
                              session: AsyncSession = Depends(get_async_session)) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_id, session)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response


@router.post("", name='upload_video')
async def upload_video(
        title: str,
        description: str,
        file: UploadFile,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        file_name = f'media/{current_user.id}_{uuid4()}.mp4'
        if file.content_type == 'video/mp4':
            await write_video(file_name, file)
        else:
            raise HTTPException(status_code=418, detail="It isn't mp4")
        new_video = Video(author_id=current_user.id,
                          title=title,
                          description=description,
                          url=file_name,
                          views=0)
        session.add(new_video)
        await session.commit()
        return {'file_name': file_name}

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
