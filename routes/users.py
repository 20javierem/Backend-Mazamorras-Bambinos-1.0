from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from starlette import status

from config.auth import verify_password
from controllers import users
from models.user import User, UserRead, UserUpdate, UserBase

SECRET: str = "ae0a9c1be3af1ad21bdf328547068c14557527eada6e63e0"
manager: LoginManager = LoginManager(SECRET, 'user/login', default_expiry=timedelta(hours=12))

router: APIRouter = APIRouter()


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


@router.post('/login')
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


@router.post("/", response_model=UserRead, status_code=status.HTTP_202_ACCEPTED)
async def create(schema: UserBase, user=Depends(manager)):
    user: User = User.from_orm(schema)
    if users.getByUsername(user.username) is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "nombre de usuario ya registrado"})
    user.save()
    return user


@router.patch("/{id}", response_model=UserRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: UserUpdate, user=Depends(manager)):
    user: User = users.get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(user, key, value)
    user.save()
    return user


@router.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    user: User = users.get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    user.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
