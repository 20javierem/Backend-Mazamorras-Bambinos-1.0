from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.workers as workers
from models.worker import Worker, WorkerBase, WorkerUpdate, WorkerReadWithType, WorkerRead
from routes.sessions import manager

apiWorkers = APIRouter()


@apiWorkers.get("/", response_model=list[WorkerRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    workers_list = await workers.all()
    return workers_list


@apiWorkers.post("/", response_model=WorkerRead, status_code=status.HTTP_201_CREATED)
async def create(schema: WorkerBase):
    worker: Worker = Worker.from_orm(schema)
    await worker.save()
    return worker


@apiWorkers.get("/{id}", response_model=WorkerReadWithType, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    worker: WorkerReadWithType = await workers.get(id)
    if worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return worker


@apiWorkers.patch('/{id}', response_model=WorkerRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: WorkerUpdate, user=Depends(manager)):
    worker: Worker = await workers.get(id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(worker, key, value)
    await worker.save()
    return worker


@apiWorkers.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    worker: Worker = await workers.get(id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    if await workers.hasDependences(worker):
        worker.active = False
        await worker.save()
    else:
        await worker.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
