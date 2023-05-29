from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class ProductPlaceSale(SQLModel, table=True):
    __tablename__ = 'product_place_sale_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    quantityInitial: float = Field(default=0)
    quantityRest: float = Field(default=0)
    quantitySold: float = Field(default=0)
    totalSale: float = Field(default=0)

    productDaySale_id: int = Field(default=None, foreign_key="product_day_sale_tbl.id")
    productDaySale: Optional["ProductDaySale"] = Relationship(back_populates="productPlaceSales",
                                                            sa_relationship_kwargs={"lazy": "subquery"})

    placeSale_id: int = Field(default=None, foreign_key="place_sale_tbl.id")
    placeSale: Optional["PlaceSale"] = Relationship(back_populates="productPlaceSales",
                                                    sa_relationship_kwargs={"lazy": "subquery"})


class ProductPlaceSaleRead(SQLModel):
    id: int
    quantityInitial: float
    quantityRest: float
    quantitySold: float
    totalSale: float

    productDaySale_id: int
    placeSale_id: int


class ProductPlaceSaleReadWithDetails(ProductPlaceSaleRead):
    productDaySale: Optional["ProductDaySaleRead"] = None
    placeSale: Optional["PlaceSaleRead"] = None


class ProductPlaceSaleUpdate(SQLModel):
    quantityInitial: float = Field(default=0)
    quantityRest: float = Field(default=0)

