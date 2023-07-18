from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from config.moreno import Moreno


class ProductPlaceSale(Moreno, SQLModel, table=True):
    __tablename__ = 'product_place_sale_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    deleted: bool = Field(default=False)
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

    def calculate_totals(self):
        quantityTransfer: int = 0
        for transfer in self.placeSale.transfersEntry:
            if transfer.productDaySale_id == self.productDaySale.id:
                quantityTransfer = quantityTransfer + transfer.quantity

        for transfer in self.placeSale.transfersExit:
            if transfer.productDaySale_id == self.productDaySale.id:
                quantityTransfer = quantityTransfer - transfer.quantity

        self.quantitySold = self.quantityInitial + quantityTransfer - self.quantityRest
        self.totalSale = self.quantitySold * float(self.productDaySale.price)

    def delete(self):
        self.quantityInitial = 0
        self.quantityRest = 0
        self.quantitySold = 0
        self.totalSale = 0.0
        self.deleted = True
        self.save()


class ProductPlaceSaleRead(SQLModel):
    id: int
    deleted: bool
    quantityInitial: float
    quantityRest: float
    quantitySold: float
    totalSale: float

    productDaySale_id: int
    placeSale_id: int


class ProductPlaceSaleCreate(SQLModel):
    quantityInitial: float
    quantityRest: float

    productDaySale_id: int
    placeSale_id: int


class ProductPlaceSaleReadDaySaleCreate(SQLModel):
    id: int
    placeSale_id: int
    productDaySale_id: int


class ProductPlaceSaleReadWithDetails(ProductPlaceSaleRead):
    productDaySale: Optional["ProductDaySaleRead"] = None
    placeSale: Optional["PlaceSaleRead"] = None


class ProductPlaceSaleUpdate(SQLModel):
    quantityInitial: float = Field(default=0)
    quantityRest: float = Field(default=0)
