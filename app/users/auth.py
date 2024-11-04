from datetime import datetime, timezone, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import get_auth_data
from app.users.dao import UserDao


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({'exp': expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], auth_data['algorithm'])
    return encode_jwt


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def authenticate_user(email: EmailStr, password: str):
    user = await UserDao.find_one_or_none(email=email)
    if not user or verify_password(password=password, hashed_password=user.hashed_password) is False:
        return None
    return user