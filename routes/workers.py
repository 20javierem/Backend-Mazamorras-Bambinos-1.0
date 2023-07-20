from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.workers as workers
from models.worker import Worker, WorkerBase, WorkerUpdate, WorkerReadWithType, WorkerRead
from routes.users import manager

router = APIRouter()


@router.get("/", response_model=list[WorkerRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    workers_list = workers.all()
    return workers_list


@router.post("/", response_model=WorkerRead, status_code=status.HTTP_201_CREATED)
async def create(schema: WorkerBase):
    worker: Worker = Worker.from_orm(schema)
    worker.save()
    return worker


@router.get("/{id}", response_model=WorkerReadWithType, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    worker: WorkerReadWithType = workers.get(id)
    if worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return worker


@router.patch('/{id}', response_model=WorkerRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: WorkerUpdate, user=Depends(manager)):
    worker: Worker = workers.get(id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(worker, key, value)
    worker.save()
    return worker


@router.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    worker: Worker = workers.get(id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    worker.active = False
    worker.save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
