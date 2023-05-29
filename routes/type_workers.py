from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.type_workers as types_workers
from models.type_worker import TypeWorker, TypeWorkerCreate, TypeWorkerUpdate
from routes.sessions import manager

apiTypeWorkers = APIRouter()


@apiTypeWorkers.get("/", response_model=list[TypeWorker], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    list_types_workers = await types_workers.all()
    return list_types_workers


@apiTypeWorkers.post("/", response_model=TypeWorker, status_code=status.HTTP_201_CREATED)
async def create(schema: TypeWorkerCreate):
    type_worker: TypeWorker = TypeWorker.from_orm(schema)
    type_worker = await types_workers.save(type_worker)
    return type_worker


@apiTypeWorkers.get("/{id}", response_model=TypeWorker, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    type_worker: TypeWorker = await types_workers.get(id)
    if type_worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return type_worker


@apiTypeWorkers.patch('/{id}', response_model=TypeWorker, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: TypeWorkerUpdate, user=Depends(manager)):
    type_worker: TypeWorker = await types_workers.get(id)
    if not type_worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(type_worker, key, value)
    type_worker = await types_workers.save(type_worker)
    return type_worker


@apiTypeWorkers.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    type_worker: TypeWorker = await types_workers.get(id)
    if not type_worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await types_workers.delete(type_worker)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
