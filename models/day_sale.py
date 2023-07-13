from datetime import datetime
from typing import Optional

from pydantic.types import conlist
from pymysql import Date
from sqlmodel import SQLModel, Field, Relationship

from config.moreno import Moreno
from models.place_sale import PlaceSaleCreate
from models.product_day_sale import ProductDaySaleCreate


class DaySaleBase(SQLModel):
    date: Date
    placeSales: conlist(PlaceSaleCreate, min_items=1)
    productDaySales: conlist(ProductDaySaleCreate, min_items=1)


class DaySale(Moreno, SQLModel, table=True):
    __tablename__ = 'day_sale_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    date: Date = Field(unique=True, nullable=False)
    quantitySold: int = Field(default=0)
    totalSale: float = Field(default=0.0)
    totalAdvances: float = Field(default=0.0)
    totalMotions: float = Field(default=0.0)
    totalCurrent: float = Field(default=0.0)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    placeSales: list["PlaceSale"] = Relationship(
        back_populates="daySale",
        sa_relationship_kwargs={"lazy": "subquery",
                                "order_by": "desc(PlaceSale.totalSale)"})
    productDaySales: list["ProductDaySale"] = Relationship(
        back_populates="daySale",
        sa_relationship_kwargs={"lazy": "subquery"})
    advances: list["Advance"] = Relationship(
        back_populates="daySale",
        sa_relationship_kwargs={"lazy": "subquery"})
    motions: list["Motion"] = Relationship(
        back_populates="daySale",
        sa_relationship_kwargs={"lazy": "subquery"})

    def calculate_totals(self):
        self.quantitySold = 0
        self.totalSale = 0.0
        self.totalAdvances = 0.0
        self.totalMotions = 0.0

        for placeSale in self.placeSales:
            self.quantitySold += placeSale.quantitySold
            self.totalSale += placeSale.totalSale
            self.totalAdvances += placeSale.totalAdvances
            self.totalMotions += placeSale.totalMotions
        for advance in self.advances:
            self.totalAdvances -= float(advance.amount)

        for motion in self.motions:
            if motion.income:
                self.totalMotions += float(motion.amount)
            else:
                self.totalMotions -= float(motion.amount)

        self.totalCurrent = self.totalSale + self.totalMotions + self.totalAdvances


class DaySaleRead(SQLModel):
    id: int
    date: Date
    quantitySold: int
    totalSale: float
    totalAdvances: float
    totalMotions: float
    totalCurrent: float


class DaySaleReadCreate(SQLModel):
    id: int
    placeSales: list["PlaceSaleReadCreateWithDetails"] = []
    productDaySales: list["ProductDaySaleRead"] = []


class DaySaleReadWithDetails(DaySaleRead):
    placeSales: list["PlaceSaleReadForDaySale"] = []
    productDaySales: list["ProductDaySaleReadWithDetails"] = []
    advances: list["AdvanceRead"] = []
    motions: list["MotionRead"] = []


class DaySaleUpdate(SQLModel):
    date: Date
