from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.advances as advances
from models.advance import Advance, AdvanceBase, AdvanceUpdate, AdvanceReadWithDetails
from routes.sessions import manager

apiAdvances = APIRouter()


@apiAdvances.get("/", response_model=list[AdvanceReadWithDetails], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    day_sales_list = await advances.all()
    return day_sales_list


@apiAdvances.post("/", response_model=AdvanceReadWithDetails, status_code=status.HTTP_201_CREATED)
async def create(schema: AdvanceBase, user=Depends(manager)):
    advance: Advance = Advance.from_orm(schema)
    await advances.save(advance)
    return advance


@apiAdvances.get("/{id}", response_model=AdvanceReadWithDetails, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    advance: AdvanceReadWithDetails = await advances.get(id)
    if advance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return advance


@apiAdvances.patch('/{id}', response_model=AdvanceReadWithDetails, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: AdvanceUpdate, user=Depends(manager)):
    advance: Advance = await advances.get(id)
    if not advance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(advance, key, value)
    advance: AdvanceReadWithDetails = await advances.save(advance)
    return advance


@apiAdvances.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    advance: Advance = await advances.get(id)
    if not advance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await advances.delete(advance)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
