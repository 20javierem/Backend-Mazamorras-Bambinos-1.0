from datetime import datetime
from typing import Optional
from pydantic import condecimal
from sqlmodel import SQLModel, Field, Relationship

from config.moreno import Moreno


class MotionBase(SQLModel):
    description: str
    amount: condecimal(max_digits=10, decimal_places=1) = Field(default=0)
    income: bool
    daySale_id: int = Field(default=None, foreign_key="day_sale_tbl.id")
    placeSale_id: int = Field(default=None, foreign_key="place_sale_tbl.id")


class Motion(Moreno, MotionBase, table=True):
    __tablename__ = 'motion_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    deleted: bool = Field(default=False)
    daySale: Optional["DaySale"] = Relationship(back_populates="motions", sa_relationship_kwargs={"lazy": "subquery"})
    placeSale: Optional["PlaceSale"] = Relationship(back_populates="motions",
                                                    sa_relationship_kwargs={"lazy": "subquery"})

    def delete(self):
        self.amount = 0.0
        self.deleted = True
        self.save()


class MotionRead(MotionBase):
    id: int
    deleted: bool


class MotionWithDetails(MotionRead):
    daySale: Optional["DaySaleRead"] = None
    placeSale: Optional["PlaceSaleReadWithDaySale"] = None


class MotionUpdate(SQLModel):
    description: Optional[str]
    income: Optional[bool]
    amount: Optional[condecimal(max_digits=10, decimal_places=1)]
