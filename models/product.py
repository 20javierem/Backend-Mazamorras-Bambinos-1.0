from datetime import datetime
from typing import Optional

from pydantic import condecimal, constr
from sqlmodel import Field, SQLModel


class ProductCreate(SQLModel):
    name: constr(min_length=3) = Field(default="nuevo")
    price: condecimal(max_digits=10, decimal_places=1) = Field(default=0)
    active: bool = Field(default=True)


class Product(ProductCreate, table=True):
    __tablename__ = 'product_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    delete: bool = Field(default=False)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})



class ProductRead(ProductCreate):
    id: int


class ProductUpdate(SQLModel):
    name: Optional[str]
    price: Optional[condecimal(max_digits=10, decimal_places=1)]
    active: Optional[bool]
