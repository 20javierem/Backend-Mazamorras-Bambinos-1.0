from typing import Optional
from datetime import datetime

from pydantic import validator
from sqlmodel import Field, SQLModel

from config import auth
from config.moreno import Moreno


class UserBase(SQLModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    admin: bool = Field(default=False)

    @validator('password')
    def valid(cls, v):
        if v is None:
            raise ValueError('debe ingresar un valor valido')
        return auth.get_password_hash(v)


class User(Moreno, UserBase, table=True):
    __tablename__ = 'user_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    deleted: bool = Field(default=False)
    created: Optional[datetime] = Field(default=datetime.now(),
                                        nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(),
                                        nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})

    def delete(self):
        self.deleted = True
        self.save()


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    password: Optional[str]
    admin: Optional[bool]

    @validator('password')
    def valid(cls, v):
        if v is None:
            raise ValueError('debe ingresar un valor valido')
        return auth.get_password_hash(v)
