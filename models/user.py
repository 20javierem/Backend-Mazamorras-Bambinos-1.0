from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel

from config import encryption
from config.moreno import Moreno


class UserBase(SQLModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    admin: bool = Field(default=False)

    @password.setter
    def password(self, value):
        self.password = encryption.get_password_hash(value)


class User(Moreno, UserBase, table=True):
    __tablename__ = 'user_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    deleted: bool = Field(default=False)
    created: Optional[datetime] = Field(default=datetime.now(),
                                        nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(),
                                        nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})


class UserRead(UserBase):
    id: int
