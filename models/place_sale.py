from datetime import datetime
from typing import Optional

from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship

from config.moreno import Moreno


class PlaceSaleBase(SQLModel):
    worker_id: int = Field(default=0, foreign_key="worker_tbl.id")
    place_id: int = Field(default=0, foreign_key="place_tbl.id")
    daySale_id: int = Field(default=0, foreign_key="day_sale_tbl.id")

    @validator('worker_id', 'place_id', 'daySale_id')
    def valid(cls, v):
        if v == 0:
            raise ValueError('debe ingresar un valor valido')
        return v


class PlaceSaleCreate(SQLModel):
    worker_id: int
    place_id: int

    @validator('worker_id', 'place_id')
    def valid(cls, v):
        if v == 0:
            raise ValueError('debe ingresar un valor valido')
        return v


class PlaceSaleCreateWithDetails(PlaceSaleBase):
    productPlaceSales: list["ProductPlaceSaleCreate"]
    transfersExit: list["TransferBase"]
    transfersEntry: list["TransferBase"]
    advances: list["AdvanceBase"]
    expenses: list["MotionBase"]


class PlaceSale(Moreno, PlaceSaleBase, table=True):
    __tablename__ = 'place_sale_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    deleted: bool = Field(default=False)
    quantityRest: int = Field(default=0)
    quantitySold: int = Field(default=0)
    totalSale: float = Field(default=0.0)
    totalMotions: float = Field(default=0.0)
    totalAdvances: float = Field(default=0.0)
    totalCurrent: float = Field(default=0.0)
    totalDelivered: float = Field(default=0.0)

    daySale: Optional["DaySale"] = Relationship(back_populates="placeSales",
                                                sa_relationship_kwargs={"lazy": "subquery"})
    worker: Optional["Worker"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})
    place: Optional["Place"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})
    advances: list["Advance"] = Relationship(back_populates="placeSale", sa_relationship_kwargs={"lazy": "subquery"})
    motions: list["Motion"] = Relationship(back_populates="placeSale", sa_relationship_kwargs={"lazy": "subquery"})

    transfersExit: list["Transfer"] = Relationship(back_populates="source",
                                                   sa_relationship_kwargs={"foreign_keys": "Transfer.source_id",
                                                                           "lazy": "subquery"})
    transfersEntry: list["Transfer"] = Relationship(back_populates="destiny",
                                                    sa_relationship_kwargs={"foreign_keys": "Transfer.destiny_id",
                                                                            "lazy": "subquery"})
    productPlaceSales: list["ProductPlaceSale"] = Relationship(back_populates="placeSale",
                                                               sa_relationship_kwargs={"lazy": "subquery"})

    def calculate_totals(self):
        self.quantityRest = 0
        self.quantitySold = 0
        self.totalSale = 0.0
        self.totalAdvances = 0.0
        self.totalMotions = 0.0

        for productPlaceSale in self.productPlaceSales:
            self.quantityRest += productPlaceSale.quantityRest
            self.quantitySold += productPlaceSale.quantitySold
            self.totalSale += productPlaceSale.totalSale

        for advance in self.advances:
            self.totalAdvances -= float(advance.amount)

        for motion in self.motions:
            if motion.income:
                self.totalMotions += float(motion.amount)
            else:
                self.totalMotions -= float(motion.amount)
        self.totalCurrent = self.totalSale + self.totalMotions + self.totalAdvances

    def delete(self):
        self.deleted = True
        self.quantitySold = 0
        self.quantityRest = 0
        self.totalSale = 0.0
        self.totalAdvances = 0.0
        self.totalCurrent = 0.0
        self.totalMotions = 0.0
        self.totalDelivered = 0.0
        self.save()


class PlaceSaleRead(PlaceSaleBase):
    id: int
    deleted: bool
    quantityRest: int
    quantitySold: int
    totalSale: float
    totalMotions: float
    totalAdvances: float
    totalCurrent: float
    totalDelivered: float


class PlaceSaleReadWithDetails(PlaceSaleRead):
    worker: Optional["WorkerRead"] = None
    place: Optional["PlaceRead"] = None
    daySale: Optional["DaySaleRead"] = None

    advances: list["AdvanceRead"] = []
    motions: list["MotionRead"] = []
    transfersExit: list["TransferRead"] = []
    transfersEntry: list["TransferRead"] = []
    productPlaceSales: list["ProductPlaceSale"] = []


class PlaceSaleReadForReport(PlaceSaleRead):
    worker: Optional["WorkerRead"] = None
    place: Optional["PlaceRead"] = None
    daySale: Optional["DaySaleRead"] = None


class PlaceSaleReadCreateWithDetails(PlaceSaleRead):
    worker_id: int
    place_id: int
    productPlaceSales: list["ProductPlaceSaleReadDaySaleCreate"] = []


class PlaceSaleReadForDaySale(PlaceSaleRead):
    transfersExit: list["TransferRead"] = []
    motions: list["MotionRead"] = []
    advances: list["AdvanceRead"] = []


class PlaceSaleUpdate(SQLModel):
    totalDelivered: float
    worker_id: int
