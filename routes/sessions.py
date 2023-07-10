from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

import controllers.workers as workers
from config.encryption import decrypt
from models.worker import WorkerReadWithType

SECRET = "ae0a9c1be3af1ad21bdf328547068c14557527eada6e63e0"
manager = LoginManager(SECRET, '/login', default_expiry=timedelta(hours=12))

apiSession = APIRouter()


@manager.user_loader()
def get_user(username: str):
    worker: WorkerReadWithType = workers.getByDni(username)
    return worker


def verify_password(plain_password, hashed_password):
    return decrypt(hashed_password).__eq__(plain_password)


def authenticate_user(username: str, password: str):
    user: WorkerReadWithType = get_user(username)
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
    user: WorkerReadWithType = authenticate_user(dni, password)
    if not user:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(data={'sub': dni})
    return {'access_token': access_token, 'worker': WorkerReadWithType.from_orm(user)}
