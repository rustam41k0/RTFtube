from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from src.auth.base_config import get_current_user

import requests

from src.users.models import User

router = APIRouter(
    # prefix="/",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse, name='main_page')
def get_base_page(request: Request):  # , current_user: User = Depends(get_current_user)):
    response = requests.get('http://localhost:8000/videos')
    videos = response.json()
    return templates.TemplateResponse("main.html", {"request": request, 'videos': videos})


@router.get("watch/{video_id}", response_class=HTMLResponse, name='single_video_page')
def get_base_page(video_id: int, request: Request):
    response = requests.get(f'http://localhost:8000/videos/{video_id}')
    video = response.json()
    return templates.TemplateResponse("single_video_page.html", {"request": request, 'video': video})


@router.get("/user_subs", response_class=HTMLResponse)
async def user_subs(request: Request):
    return templates.TemplateResponse("user_subs.html", {"request": request})


@router.get("/404", response_class=HTMLResponse)
async def error_404(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})


@router.get("/login", response_class=HTMLResponse, name='login')
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
