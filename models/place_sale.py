from datetime import datetime
from typing import Optional

from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship


class PlaceSaleBase(SQLModel):
    worker_id: int = Field(default=0, foreign_key="worker_tbl.id")
    place_id: int = Field(default=0, foreign_key="place_tbl.id")
    daySale_id: Optional[int] = Field(default=0, foreign_key="day_sale_tbl.id")

    @validator('worker_id', 'place_id', 'daySale_id')
    def valid(cls, v):
        if v == 0:
            raise ValueError('debe ingresar un valor valido')
        return v


class PlaceSale(PlaceSaleBase, table=True):
    __tablename__ = 'place_sale_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    totalSale: float = Field(default=0.0)
    totalExpenses: float = Field(default=0.0)
    totalAdvances: float = Field(default=0.0)
    totalCurrent: float = Field(default=0.0)
    totalDelivered: float = Field(default=0.0)

    daySale: Optional["DaySale"] = Relationship(back_populates="placeSales", sa_relationship_kwargs={"lazy": "subquery"})
    worker: Optional["Worker"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})
    place: Optional["Place"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})
    advances: list["Advance"] = Relationship(back_populates="placeSale", sa_relationship_kwargs={"lazy": "subquery"})
    expenses: list["Expense"] = Relationship(back_populates="placeSale", sa_relationship_kwargs={"lazy": "subquery"})

    transfersExit: list["Transfer"] = Relationship(back_populates="source",
                                                   sa_relationship_kwargs={"foreign_keys": "Transfer.source_id", "lazy": "subquery"})
    transfersEntry: list["Transfer"] = Relationship(back_populates="destiny",
                                                    sa_relationship_kwargs={"foreign_keys": "Transfer.destiny_id", "lazy": "subquery"})
    productPlaceSales: list["ProductPlaceSale"] = Relationship(back_populates="placeSale", sa_relationship_kwargs={"lazy": "subquery"})


class PlaceSaleRead(PlaceSaleBase):
    id: int
    totalSale: float
    totalExpenses: float
    totalAdvances: float
    totalCurrent: float
    totalDelivered: float


class PlaceSaleReadWithDetails(PlaceSaleRead):
    worker: Optional["WorkerRead"] = None
    place: Optional["PlaceRead"] = None
    daySale: Optional["DaySaleRead"] = None

    advances: list["AdvanceRead"] = []
    expenses: list["ExpenseRead"] = []
    transfersExit: list["TransferRead"] = []
    transfersEntry: list["TransferRead"] = []
    productPlaceSales: list["ProductPlaceSale"] = []


class PlaceSaleUpdate(SQLModel):
    worker_id: int
