from app.dao.base import BaseDAO
from app.users.models import User


class UserDao(BaseDAO):
    model = User