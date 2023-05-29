from datetime import datetime
from typing import Optional

from pydantic import condecimal, validator
from sqlmodel import SQLModel, Field, Relationship


class AdvanceBase(SQLModel):
    description: str
    amount: condecimal(decimal_places=1) = Field(default=0)
    active: bool = True

    daySale_id: int = Field(default=0, foreign_key="day_sale_tbl.id")
    placeSale_id: Optional[int] = Field(default=0, foreign_key="place_sale_tbl.id")
    worker_id: int = Field(default=0, foreign_key="worker_tbl.id")

    @validator('daySale_id', 'placeSale_id', 'worker_id')
    def valid(cls, v):
        if v == 0:
            raise ValueError('debe ingresar un valor valido')
        return v


class Advance(AdvanceBase, table=True):
    __tablename__ = 'advance_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})

    daySale: Optional["DaySale"] = Relationship(back_populates="advances", sa_relationship_kwargs={"lazy": "subquery"} )
    placeSale: Optional["PlaceSale"] = Relationship(back_populates="advances", sa_relationship_kwargs={"lazy": "subquery"})
    worker: Optional["Worker"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})


class AdvanceRead(AdvanceBase):
    id: int


class AdvanceReadWithDetails(AdvanceRead):
    id: int

    daySale: Optional["DaySaleRead"] = None
    placeSale: Optional["PlaceSaleRead"] = None
    worker: Optional["WorkerRead"] = None


class AdvanceUpdate(SQLModel):
    description: Optional[str]
    amount: Optional[condecimal(decimal_places=1)]
    active: Optional[bool]
    worker_id: Optional[int]


