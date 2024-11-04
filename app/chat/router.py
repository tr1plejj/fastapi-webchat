import asyncio

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket, WebSocketDisconnect

from app import User
from app.chat.dao import MessageDAO
from app.chat.schemas import MessageReadSchema, MessageCreateSchema
from app.users.dao import UserDao
from app.users.dependencies import get_current_user

router = APIRouter(prefix='/chat', tags=['Chat'])

templates = Jinja2Templates(directory='app/templates')

# Активные WebSocket-подключения: {user_id: websocket}
active_connections: dict[int, WebSocket] = {}


# Функция для отправки сообщения пользователю, если он подключен
async def notify_user(user_id: int, message: dict):
    """Отправить сообщение пользователю, если он подключен."""

    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_json(message)


# WebSocket эндпоинт для соединений
@router.websocket('/ws/{user_id}/')
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # Принимаем WebSocket-соединение
    await websocket.accept()
    # Сохраняем активное соединение для пользователя
    active_connections[user_id] = websocket
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        # Удаляем пользователя из активных соединений при отключении
        active_connections.pop(user_id, None)

@router.get('/', response_class=HTMLResponse, summary='Chat Page')
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    users_all = await UserDao.find_all()
    return templates.TemplateResponse('chat.html',
                                      {'request': request, 'user': user_data, 'users_all': users_all})


@router.get('/messages/{user_id}/', response_model=list[MessageReadSchema])
async def get_messages(user_id: int, current_user: User = Depends(get_current_user)):
    return await MessageDAO.get_messages_between_users(user_id_1=user_id, user_id_2=current_user.id) or []


@router.post('/messages/', response_model=MessageCreateSchema)
async def send_message(message: MessageCreateSchema, current_user: User = Depends(get_current_user)):
    # Добавляем новое сообщение в базу данных
    await MessageDAO.add(
        sender_id=current_user.id,
        content=message.content,
        recipient_id=message.recipient_id
    )

    # Подготавливаем данные для отправки сообщения
    message_data = {
        'sender_id': current_user.id,
        'recipient_id': message.recipient_id,
        'content': message.content
    }

    # Уведомляем получателя и отправителя через WebSocket
    await notify_user(message.recipient_id, message_data)
    await notify_user(current_user.id, message_data)

    # Возвращаем подтверждение сохранения сообщения
    return {'recipient_id': message.recipient_id, 'content': message.content, 'status': 201}