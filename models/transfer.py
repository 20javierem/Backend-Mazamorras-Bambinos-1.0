from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class TransferBase(SQLModel):
    source_id: int
    destiny_id: int
    quantity: int
    product_id: int


class Transfer(SQLModel, table=True):
    __tablename__ = 'transfer_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    received: bool = Field(default=True)
    confirmed_by_admin: bool = Field(default=False)
    quantity: int = Field(default=0)
    source_id: int = Field(default=None, foreign_key="place_sale_tbl.id")
    destiny_id: int = Field(default=None, foreign_key="place_sale_tbl.id")
    product_id: Optional[int] = Field(default=None, foreign_key="product_tbl.id")

    product: Optional["Product"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})
    source: Optional["PlaceSale"] = Relationship(
        sa_relationship_kwargs={"primaryjoin": "Transfer.source_id==PlaceSale.id", "lazy": "subquery"})
    destiny: Optional["PlaceSale"] = Relationship(
        sa_relationship_kwargs={"primaryjoin": "Transfer.destiny_id==PlaceSale.id", "lazy": "subquery"})


class TransferRead(SQLModel):
    id: int
    source_id: int
    destiny_id: int
    product_id: int
    quantity: int
    confirmed_by_admin: bool


class TransferUpdate(SQLModel):
    source_id: Optional[int]
    destiny_id: Optional[int]
