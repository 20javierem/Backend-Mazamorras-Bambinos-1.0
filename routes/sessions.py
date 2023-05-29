from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

import controllers.workers as workers
from config.db import pwd_context
from models.worker import Worker, WorkerRead

SECRET = "ae0a9c1be3af1ad21bdf328547068c14557527eada6e63e0"
manager = LoginManager(SECRET, '/login', default_expiry=timedelta(hours=12))

apiSession = APIRouter()


@manager.user_loader()
async def get_user(username: str):
    return await workers.getByDni(username)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user: Worker = await get_user(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


@apiSession.post('/login')
async def login(data: OAuth2PasswordRequestForm = Depends()):
    dni = data.username
    password = data.password
    if data.username.__contains__('\"'):
        dni = eval(data.username)
        password = eval(data.password)
    user: Worker = await authenticate_user(dni, password)
    if not user:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(data={'sub': dni})
    return {'access_token': access_token, 'worker': WorkerRead.from_orm(user)}
