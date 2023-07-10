from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.type_workers as types_workers
from models.type_worker import TypeWorker, TypeWorkerCreate, TypeWorkerUpdate, TypeWorkerRead
from routes.sessions import manager

apiTypeWorkers = APIRouter()


@apiTypeWorkers.get("/", response_model=list[TypeWorkerRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    list_types_workers = types_workers.all()
    return list_types_workers


@apiTypeWorkers.post("/", response_model=TypeWorkerRead, status_code=status.HTTP_201_CREATED)
async def create(schema: TypeWorkerCreate):
    type_worker: TypeWorker = TypeWorker.from_orm(schema)
    type_worker.save()
    return type_worker


@apiTypeWorkers.get("/{id}", response_model=TypeWorkerRead, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    type_worker: TypeWorker = types_workers.get(id)
    if type_worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return type_worker


@apiTypeWorkers.patch('/{id}', response_model=TypeWorkerRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: TypeWorkerUpdate, user=Depends(manager)):
    type_worker: TypeWorker = types_workers.get(id)
    if not type_worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(type_worker, key, value)
    type_worker.save()
    return type_worker


@apiTypeWorkers.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    type_worker: TypeWorker = types_workers.get(id)
    if not type_worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    type_worker.deleted = True
    type_worker.save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
