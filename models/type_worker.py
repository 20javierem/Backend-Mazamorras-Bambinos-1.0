from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class TypeWorkerCreate(SQLModel):
    description: str


class TypeWorker(TypeWorkerCreate, table=True):
    __tablename__ = 'type_worker_tbl'
    id: Optional[int] = Field(default=None, primary_key=True)
    delete: bool = Field(default=False)
    created: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    updated: Optional[datetime] = Field(default=datetime.now(), nullable=False,
                                        sa_column_kwargs={"onupdate": datetime.now})


class TypeWorkerRead(TypeWorkerCreate):
    id: int


class TypeWorkerUpdate(SQLModel):
    description: Optional[str]
    active: Optional[bool]
