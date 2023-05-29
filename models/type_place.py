from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class TypePlaceCreate(SQLModel):
    description: str


class TypePlace(TypePlaceCreate, table=True):
    __tablename__ = 'type_place_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    delete: bool = Field(default=False)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})


class TypePlaceRead(TypePlaceCreate):
    id: int


class TypePlaceUpdate(SQLModel):
    description: Optional[str]
    active: Optional[bool]
