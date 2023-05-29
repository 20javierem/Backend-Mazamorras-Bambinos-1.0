from datetime import datetime, date
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class WorkerBase(SQLModel):
    names: str
    lastNames: str
    sex: str
    dni: str
    phone: str
    salary: float
    start: Optional[date]
    birthday: Optional[date]
    active: bool = Field(default=True)
    admin: bool = Field(default=False)
    typeWorker_id: int = Field(default=None, foreign_key="type_worker_tbl.id")


class Worker(WorkerBase, table=True):
    __tablename__ = 'worker_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    delete: bool = Field(default=False)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    password: str = Field(default=None)
    typeWorker: Optional["TypeWorker"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})


class WorkerRead(WorkerBase):
    id: int


class WorkerReadWithType(WorkerRead):
    typeWorker: Optional["TypeWorkerRead"] = None


class WorkerUpdate(SQLModel):
    names: Optional[str]
    lastNames: Optional[str]
    sex: Optional[str]
    dni: Optional[str]
    phone: Optional[str]
    salary: Optional[float]
    start: Optional[date]
    birthday: Optional[date]
    active: Optional[bool]
    admin: Optional[bool]
    typeWorker_id: Optional[int]
