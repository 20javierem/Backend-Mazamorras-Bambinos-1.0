from datetime import datetime
from typing import Optional

from pydantic.types import conlist
from pymysql import Date
from sqlmodel import SQLModel, Field, Relationship

from models.place_sale import PlaceSaleBase, PlaceSale
from models.product_day_sale import ProductDaySaleBase, ProductDaySale


class DaySaleBase(SQLModel):
    date: Date
    placeSales: conlist(PlaceSaleBase, min_items=1)
    productDaySales: conlist(ProductDaySaleBase, min_items=1)

    def to_day_sale(self) -> "DaySale":
        day_sale: DaySale = DaySale(date=self.date)
        for place_sale in self.placeSales:
            day_sale.placeSales.append(PlaceSale(worker_id=place_sale.worker_id, place_id=place_sale.place_id))
        for product_day_sale in self.productDaySales:
            day_sale.productDaySales.append(
                ProductDaySale(product_id=product_day_sale.product_id, price=product_day_sale.price))
        return day_sale


class DaySale(SQLModel, table=True):
    __tablename__ = 'day_sale_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    totalSale: float = Field(default=0.0)
    totalExpenses: float = Field(default=0.0)
    totalAdvances: float = Field(default=0.0)
    totalCurrent: float = Field(default=0.0)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    date: Date = Field(unique=True, nullable=False)

    placeSales: list["PlaceSale"] = Relationship(back_populates="daySale", sa_relationship_kwargs={"lazy": "subquery", "order_by": "desc(PlaceSale.totalSale)"})
    productDaySales: list["ProductDaySale"] = Relationship(back_populates="daySale",
                                                         sa_relationship_kwargs={"lazy": "subquery"})
    advances: list["Advance"] = Relationship(back_populates="daySale", sa_relationship_kwargs={"lazy": "subquery"})
    expenses: list["Expense"] = Relationship(back_populates="daySale", sa_relationship_kwargs={"lazy": "subquery"})


class DaySaleRead(SQLModel):
    id: int
    date: Date
    totalSale: float
    totalExpenses: float
    totalAdvances: float
    totalCurrent: float


class DaySaleReadWithDetails(DaySaleRead):
    placeSales: list["PlaceSaleRead"] = []
    productDaySales: list["ProductDaySaleRead"] = []
    advances: list["AdvanceRead"] = []
    expenses: list["Expense"] = []


class DaySaleUpdate(SQLModel):
    date: Date
