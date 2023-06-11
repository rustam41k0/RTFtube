from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, RedirectResponse

from src.comments.models import Comment
from src.database import get_async_session
from src.likes.models import Like
from src.auth.base_config import get_current_user

import requests

from src.users.models import User
from src.videos.models import Video

router = APIRouter(
    # prefix="/",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse, name='main_page')
async def get_base_page(request: Request):  # , current_user: User = Depends(get_current_user)):
    response = requests.get('http://localhost:8000/videos')
    videos = response.json()
    return templates.TemplateResponse("main.html", {"request": request, 'videos': videos})


@router.get("/watch/{video_id}", response_class=HTMLResponse, name='single_video_page')
async def get_base_page(video_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    likes_query = select(Like).filter(Like.video_id == video_id)
    likes = await session.execute(likes_query)
    comments_query = select(Comment).filter(Comment.video_id == video_id)
    comments = await session.execute(comments_query)

    return templates.TemplateResponse("single_video_page.html",
                                      {"request": request,
                                       'video_id': video_id,
                                       'likes': len(likes.mappings().all()),
                                       'comments': comments.mappings().all(),
                                       })


@router.get("/user_subs", response_class=HTMLResponse)
async def user_subs(request: Request):
    return templates.TemplateResponse("user_subs.html", {"request": request})


@router.get("/404", response_class=HTMLResponse)
async def error_404(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})


@router.get("/login", response_class=HTMLResponse, name='login')
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
