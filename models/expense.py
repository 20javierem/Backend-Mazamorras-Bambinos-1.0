from datetime import datetime
from typing import Optional

from pydantic import condecimal
from sqlmodel import SQLModel, Field, Relationship


class ExpenseCreate(SQLModel):
    description: str
    amount: condecimal(decimal_places=1) = Field(default=0)
    daySale_id: int = Field(default=None, foreign_key="day_sale_tbl.id")
    placeSale_id: int = Field(default=None, foreign_key="place_sale_tbl.id")


class Expense(ExpenseCreate, table=True):
    __tablename__ = 'expenses_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})

    daySale: Optional["DaySale"] = Relationship(back_populates="expenses", sa_relationship_kwargs={"lazy": "subquery"})
    placeSale: Optional["PlaceSale"] = Relationship(back_populates="expenses",
                                                    sa_relationship_kwargs={"lazy": "subquery"})


class ExpenseRead(ExpenseCreate):
    id: int


class ExpenseWithDetails(ExpenseRead):
    daySale: Optional["DaySaleRead"] = None
    placeSale: Optional["PlaceSaleRead"] = None


class ExpenseUpdate(SQLModel):
    description: Optional[str]
    amount: Optional[condecimal(decimal_places=1)]
