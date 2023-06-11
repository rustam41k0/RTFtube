from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from src.auth.base_config import fastapi_users, auth_backend, get_current_user
from src.comments.router import router as router_comments
from src.auth.router import router as router_auth
from src.likes.router import router as router_likes
from src.users.router import router as router_users
from src.videos.router import router as router_videos
from src.pages.router import router as router_pages
from src.users.schemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='RTFTube')
app.mount('/static', StaticFiles(directory='src/static'), name='static')

origins = []


# @app.middleware("http")
# async def check_authentication(request: Request, call_next):
#     if not (request.url.path.startswith("/auth") or request.url.path.startswith("/main/login")):
#         try:
#             await get_current_user(request=request)
#         except HTTPException as ex:
#             # print(ex.status_code)
#             return RedirectResponse(url="/main/login")
#     response = await call_next(request)
#     return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

# app.include_router(router_auth)
app.include_router(router_videos)
app.include_router(router_users)
app.include_router(router_likes)
app.include_router(router_pages)
app.include_router(router_comments)
