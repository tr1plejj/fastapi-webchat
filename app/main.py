from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from app.exceptions import TokenExpiredException, TokenNotFoundException
from app.users.router import router as users_router
from app.chat.router import router as chat_router

app = FastAPI()
app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(
    users_router
)

app.include_router(
    chat_router
)


@app.get('/')
async def redirect_to_auth():
    return RedirectResponse(url='/auth')


@app.exception_handler(TokenExpiredException)
async def token_exp_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url='/auth')


@app.exception_handler(TokenNotFoundException)
async def token_not_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url='/auth')

