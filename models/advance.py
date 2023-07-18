from datetime import datetime
from typing import Optional

from pydantic import condecimal, validator
from sqlmodel import SQLModel, Field, Relationship

from config.moreno import Moreno


class AdvanceBase(SQLModel):
    description: str
    amount: condecimal(decimal_places=1) = Field(default=0)

    daySale_id: int = Field(default=None, foreign_key="day_sale_tbl.id", nullable=True)
    placeSale_id: Optional[int] = Field(default=None, foreign_key="place_sale_tbl.id", nullable=True)
    worker_id: int = Field(default=None, foreign_key="worker_tbl.id")


class Advance(Moreno, AdvanceBase, table=True):
    __tablename__ = 'advance_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    deleted: bool = Field(default=False)
    daySale: Optional["DaySale"] = Relationship(back_populates="advances", sa_relationship_kwargs={"lazy": "subquery"})
    placeSale: Optional["PlaceSale"] = Relationship(back_populates="advances",
                                                    sa_relationship_kwargs={"lazy": "subquery"})
    worker: Optional["Worker"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})

    def delete(self):
        self.amount = 0.0
        self.deleted = True
        self.save()


class AdvanceRead(AdvanceBase):
    id: int
    deleted: bool


class AdvanceReadWithDetails(AdvanceRead):
    daySale: Optional["DaySaleRead"] = None
    placeSale: Optional["PlaceSaleRead"] = None
    worker: Optional["WorkerRead"] = None


class AdvanceUpdate(SQLModel):
    description: Optional[str]
    amount: Optional[condecimal(decimal_places=1)]
    worker_id: Optional[int]
