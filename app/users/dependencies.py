from datetime import datetime, timezone
from fastapi import Request, HTTPException, status
from fastapi.params import Depends
from jose import jwt, JWTError
from app.config import get_auth_data
from app.exceptions import TokenNotFoundException, NoJwtException, TokenExpiredException, NoUserIdException
from app.users.dao import UserDao


def get_token(request: Request):
    token = request.cookies.get('user_access_token')
    if not token:
        raise TokenNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], auth_data['algorithm'])
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UserDao.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user