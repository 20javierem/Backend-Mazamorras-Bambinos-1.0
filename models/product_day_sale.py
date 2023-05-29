from datetime import datetime
from typing import Optional

from pydantic import condecimal
from sqlmodel import SQLModel, Field, Relationship


class ProductDaySaleBase(SQLModel):
    price: condecimal(decimal_places=1) = Field(default=0)
    daySale_id: Optional[int] = Field(default=None, foreign_key="day_sale_tbl.id")
    product_id: Optional[int] = Field(default=None, foreign_key="product_tbl.id")


class ProductDaySale(ProductDaySaleBase, table=True):
    __tablename__ = 'product_day_sale_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    quantityInitial: float = Field(default=0)
    quantityRest: float = Field(default=0)
    quantitySold: float = Field(default=0)
    totalSale: float = Field(default=0)

    daySale: Optional["DaySale"] = Relationship(back_populates="productDaySales",
                                                sa_relationship_kwargs={"lazy": "subquery"})
    product: Optional["Product"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})
    productPlaceSales: list["ProductPlaceSale"] = Relationship(back_populates="productDaySale",
                                                               sa_relationship_kwargs={"lazy": "subquery"})


class ProductDaySaleRead(ProductDaySaleBase):
    id: int
    quantityInitial: float
    quantityRest: float
    quantitySold: float
    totalSale: float


class ProductDaySaleReadWithDetails(ProductDaySaleRead):
    product: Optional["ProductRead"] = None
    productPlaceSales: list["ProductPlaceSaleRead"] = []


class ProductDaySaleUpdate(SQLModel):
    price: Optional[condecimal(decimal_places=1)]
