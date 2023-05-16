from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import get_current_user
from src.database import get_async_session
from src.users.models import User, Subscriptions
from src.users.schemas import GetUser, UserUpdate
from src.videos.models import Video

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}")  # , response_model=List[GetUser])
async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        user_info_query = select(User).where(User.id == user_id)
        user_videos_query = select(Video).where(Video.author_id == user_id)
        user_info = await session.execute(user_info_query)
        user_videos = await session.execute(user_videos_query)
        return {
            **user_info.mappings().first(),
            'videos': user_videos.mappings().all()
        }

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})


@router.post('/{user_id}/subscribe')
async def sub_or_unsub_user(user_id: int,
                            current_user: User = Depends(get_current_user),
                            session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Subscriptions).filter(
            and_(Subscriptions.user == current_user.id, Subscriptions.subscribed_to == user_id))
        subscriber = await session.execute(query)
        subscriber = subscriber.mappings().all()
        if not subscriber:
            new_subscriber = Subscriptions(user=current_user.id, subscribed_to=user_id)
            session.add(new_subscriber)
            await session.commit()
            return {'status': 'Subscribe successfully'}
        else:
            unubscribe = await session.get(Subscriptions, subscriber[0]['Subscriptions'].id)
            await session.delete(unubscribe)
            await session.commit()
            return {'status': 'Unubscribe successfully'}

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})


@router.put("/{user_id}", name='update_profile')
async def update_profile(
        profile: UserUpdate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        profile_for_update = await session.get(User, current_user.id)
        if not profile_for_update:
            return {"error": "User not found"}
        if profile.username:
            profile_for_update.username = profile.username
        if profile.channel_description:
            profile_for_update.channel_description = profile.channel_description
        await session.commit()
        await session.refresh(profile_for_update)
        return {"message": "Profile updated successfully",
                "user": profile_for_update}

    except Exception as ex:
        raise HTTPException(status_code=500, detail={"data": str(ex)})
