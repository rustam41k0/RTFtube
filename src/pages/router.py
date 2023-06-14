from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, RedirectResponse

from src.comments.models import Comment
from src.database import get_async_session
from src.likes.models import Like
from src.auth.base_config import get_current_user
import urllib.request
import requests

from src.users.models import User, Subscriptions
from src.videos.models import Video

router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse, name='main_page')
def get_base_page(request: Request):
    response = requests.get('http://127.0.0.1:8000/videos')
    videos = response.json()
    return templates.TemplateResponse("main.html", {"request": request, 'videos': videos})


@router.get("/watch/{video_id}", response_class=HTMLResponse, name='single_video_page')
async def get_video_page(video_id: int,
                         request: Request,
                         session: AsyncSession = Depends(get_async_session)):
    video_query = select(Video).filter(Video.id == video_id)
    current_video = await session.execute(video_query)
    current_video = current_video.mappings().all()
    if not current_video:
        return RedirectResponse(url="/404")

    likes_query = select(Like).filter(Like.video_id == video_id)
    likes = await session.execute(likes_query)

    comments_query = select(Comment).filter(Comment.video_id == video_id)
    comments = await session.execute(comments_query)

    return templates.TemplateResponse("single_video_page.html", {"request": request,
                                                                 'video_id': video_id,
                                                                 'title': current_video[0].Video.title,
                                                                 'description': current_video[0].Video.description,
                                                                 'likes': len(likes.mappings().all()),
                                                                 'comments': comments.mappings().all(),
                                                                 })


@router.get("/404", response_class=HTMLResponse)
def error_404(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})

