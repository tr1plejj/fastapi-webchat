from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(description='Электронная почта')
    password: str = Field(min_length=5, max_length=50, description='Пароль, от 5 символов до 50')
    password_check: str = Field(min_length=5, max_length=50, description='Пароль еще раз')
    name: str = Field(min_length=2, max_length=50, description='Имя')


class UserAuthSchema(BaseModel):
    email: EmailStr = Field(description='Электронная почта')
    password: str = Field(min_length=5, max_length=50, description='Пароль, от 5 символов до 50')


class UserReadSchema(BaseModel):
    id: int = Field(description='Идентификатор пользователя')
    name: str = Field(min_length=2, max_length=50, description='Имя')