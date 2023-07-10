from datetime import datetime, date
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from config.encryption import encrypt
from config.moreno import Moreno


class WorkerBase(SQLModel):
    names: str
    lastNames: str
    dni: str
    sex: str
    phone: str
    salary: float
    start: Optional[date]
    birthday: Optional[date]
    active: bool = Field(default=True)
    admin: bool = Field(default=False)
    typeWorker_id: int = Field(default=None, foreign_key="type_worker_tbl.id")


class Worker(Moreno, WorkerBase, table=True):
    __tablename__ = 'worker_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    deleted: bool = Field(default=False)
    password: str = Field(default=None)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})
    typeWorker: Optional["TypeWorker"] = Relationship(sa_relationship_kwargs={"lazy": "joined"})

    def save(self):
        if self.password is None:
            self.password = encrypt(self.dni)
        return super().save()


class WorkerRead(WorkerBase):
    id: int
    deleted: bool
    password: str


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
