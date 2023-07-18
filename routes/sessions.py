from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from config.encryption import verify_password
from controllers import users
from models.user import User, UserRead

SECRET: str = "ae0a9c1be3af1ad21bdf328547068c14557527eada6e63e0"
manager: LoginManager = LoginManager(SECRET, '/login', default_expiry=timedelta(hours=12))

apiSession: APIRouter = APIRouter()


@manager.user_loader()
def get_user(username: str):
    user: User = users.getByUsername(username)
    return user


def authenticate_user(username: str, password: str):
    user: User = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


@apiSession.post('/login')
async def login(data: OAuth2PasswordRequestForm = Depends()):
    username: str = data.username
    password: str = data.password
    if data.username.__contains__('\"'):
        username = eval(data.username)
        password = eval(data.password)
    user: User = authenticate_user(username, password)
    if not user:
        raise InvalidCredentialsException
    access_token: str = manager.create_access_token(data={'sub': username})
    return {'access_token': access_token, 'user': UserRead.from_orm(user)}
