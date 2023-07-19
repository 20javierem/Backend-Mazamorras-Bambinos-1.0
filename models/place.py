from datetime import datetime
from typing import Optional

from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship

from config.moreno import Moreno


class PlaceBase(SQLModel):
    description: str
    address: str
    active: bool = Field(default=True)
    typePlace_id: int = Field(default=0, foreign_key="type_place_tbl.id")

    @validator('typePlace_id')
    def valid(cls, v):
        if v == 0:
            raise ValueError('debe ingresar un tipo de puesto valido')
        return v


class Place(Moreno, PlaceBase, table=True):
    __tablename__ = 'place_tbl'

    id: Optional[int] = Field(default=None, primary_key=True)
    deleted: bool = Field(default=False)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    typePlace: Optional["TypePlace"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})

    def delete(self):
        self.active = False
        self.save()


class PlaceRead(PlaceBase):
    id: int
    deleted: bool


class PlaceReadWithType(PlaceRead):
    typePlace: Optional["TypePlaceRead"]


class PlaceUpdate(SQLModel):
    description: Optional[str]
    address: Optional[str]
    active: Optional[bool]
    typePlace_id: Optional[int]
