from datetime import datetime, date
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from config.moreno import Moreno


class WorkerBase(SQLModel):
    firstnames: str
    lastnames: str
    dni: str
    sex: str
    phone: str
    start: Optional[date]
    birthday: Optional[date]
    active: bool = Field(default=True)
    typeWorker_id: int = Field(default=None, foreign_key="type_worker_tbl.id")


class Worker(Moreno, WorkerBase, table=True):
    __tablename__ = 'worker_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    deleted: bool = Field(default=False)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    user_id: int = Field(default=None, foreign_key="user_tbl.id")
    typeWorker: Optional["TypeWorker"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})


class WorkerRead(WorkerBase):
    id: int
    deleted: bool


class WorkerReadWithType(WorkerRead):
    typeWorker: Optional["TypeWorkerRead"] = None


class WorkerUpdate(SQLModel):
    firstnames: Optional[str]
    lastnames: Optional[str]
    sex: Optional[str]
    dni: Optional[str]
    phone: Optional[str]
    start: Optional[date]
    birthday: Optional[date]
    active: Optional[bool]
    typeWorker_id: Optional[int]
    user_id: Optional[int]
