from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.exceptions import UserAlreadyExistsException, PasswordMismatchException, IncorrectEmailOrPasswordException
from app.users.auth import hash_password, authenticate_user, create_access_token
from app.users.dao import UserDao
from app.users.schemas import UserRegisterSchema, UserAuthSchema, UserReadSchema

router = APIRouter(prefix='/auth', tags=['Auth'])

templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse, summary='Страница авторизации')
async def get_categories(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


@router.post('/register/')
async def register_user(user_data: UserRegisterSchema):
    user = await UserDao.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException

    hashed_password = hash_password(user_data.password)
    await UserDao.add(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    return {'message': 'Регистрация прошла успешно!'}


@router.post('/login/')
async def login(response: Response, user_data: UserAuthSchema):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(check.id)})
    response.set_cookie(key='user_access_token', value=access_token, httponly=True)
    return {'access_token': access_token}


@router.post('/logout/')
async def logout(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Вы вышли из системы.'}


@router.get('/users/', response_model=list[UserReadSchema])
async def get_users():
    users_all = await UserDao.find_all()
    return [{'id': user.id, 'name': user.name} for user in users_all]
