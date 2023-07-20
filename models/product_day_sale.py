from datetime import datetime
from typing import Optional

from pydantic import condecimal
from sqlmodel import SQLModel, Field, Relationship

from config.moreno import Moreno


class ProductDaySaleBase(SQLModel):
    price: condecimal(max_digits=10, decimal_places=1) = Field(default=0)
    daySale_id: Optional[int] = Field(default=None, foreign_key="day_sale_tbl.id")
    product_id: Optional[int] = Field(default=None, foreign_key="product_tbl.id")


class ProductDaySaleCreate(SQLModel):
    price: condecimal(max_digits=10, decimal_places=1) = Field(default=0)
    product_id: Optional[int]


class ProductDaySale(Moreno, ProductDaySaleBase, table=True):
    __tablename__ = 'product_day_sale_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    deleted: bool = Field(default=False)
    quantityInitial: float = Field(default=0)
    quantityRest: float = Field(default=0)
    quantitySold: float = Field(default=0)
    totalSale: float = Field(default=0)

    daySale: Optional["DaySale"] = Relationship(back_populates="productDaySales",
                                                sa_relationship_kwargs={"lazy": "subquery"})
    product: Optional["Product"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})
    productPlaceSales: list["ProductPlaceSale"] = Relationship(back_populates="productDaySale",
                                                               sa_relationship_kwargs={"lazy": "subquery"})

    def calculate_totals(self):
        self.quantityInitial = 0
        self.quantityRest = 0
        self.quantitySold = 0
        self.totalSale = 0.0
        for productPlaceSale in self.productPlaceSales:
            self.quantityInitial += productPlaceSale.quantityInitial
            self.quantityRest += productPlaceSale.quantityRest
            self.quantitySold += productPlaceSale.quantitySold
            self.totalSale += productPlaceSale.totalSale

    def delete(self):
        self.quantityInitial = 0
        self.quantityRest = 0
        self.quantitySold = 0
        self.totalSale = 0.0
        self.deleted = True
        self.save()


class ProductDaySaleRead(ProductDaySaleBase):
    id: int
    deleted: bool
    quantityInitial: float
    quantityRest: float
    quantitySold: float
    totalSale: float


class ProductDaySaleReadReport(ProductDaySaleRead):
    daySale: Optional["DaySaleRead"] = None


class ProductDaySaleReadCreate(ProductDaySaleRead):
    product_id: int
    productPlaceSales: list["ProductPlaceSaleReadDaySaleCreate"] = []


class ProductDaySaleReadWithDetails(ProductDaySaleRead):
    product_id: int
    productPlaceSales: list["ProductPlaceSaleRead"] = []


class ProductDaySaleUpdate(SQLModel):
    price: condecimal(decimal_places=1)
