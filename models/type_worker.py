from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field

from config.moreno import Moreno


class TypeWorkerCreate(SQLModel):
    description: str


class TypeWorker(Moreno, TypeWorkerCreate, table=True):
    __tablename__ = 'type_worker_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    deleted: bool = Field(default=False)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})


class TypeWorkerRead(TypeWorkerCreate):
    id: int
    deleted: bool


class TypeWorkerUpdate(SQLModel):
    description: Optional[str]
    active: Optional[bool]
