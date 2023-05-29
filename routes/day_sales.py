from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.day_sales as day_sales
from models.day_sale import DaySale, DaySaleBase, DaySaleUpdate, DaySaleReadWithDetails, DaySaleRead
from routes.sessions import manager

apiDaySales = APIRouter()


@apiDaySales.get("/", response_model=list[DaySaleRead], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    day_sales_list = await day_sales.all()
    return day_sales_list


@apiDaySales.post("/", response_model=DaySaleReadWithDetails, status_code=status.HTTP_201_CREATED)
async def create(schema: DaySaleBase, user=Depends(manager)):
    day_sale = await day_sales.save(schema.to_day_sale())
    return day_sale


@apiDaySales.get("/{id}", response_model=DaySaleReadWithDetails, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    day_sale: DaySale = await day_sales.get(id)
    if day_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return day_sale


@apiDaySales.patch('/{id}', response_model=DaySaleReadWithDetails, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: DaySaleUpdate, user=Depends(manager)):
    day_sale: DaySale = await day_sales.get(id)
    if not day_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(day_sale, key, value)
    day_sale: DaySaleReadWithDetails = await day_sales.save(day_sale)
    return day_sale


@apiDaySales.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    day_sale: DaySale = await day_sales.get(id)
    if not day_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await day_sales.delete(day_sale)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@apiDaySales.get("/date/{date}", response_model=DaySaleReadWithDetails, status_code=status.HTTP_200_OK)
async def get_by_date(date: str, user=Depends(manager)):
    day_sale: DaySaleReadWithDetails = await day_sales.getOfDate(date)
    if day_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return day_sale


@apiDaySales.get("/between/{start}/{end}", response_model=list[DaySale], status_code=status.HTTP_200_OK)
async def get_between(start: str, end: str, user=Depends(manager)):
    day_sales_list: list[DaySale] = await day_sales.getByRangeOfDate(start, end)
    return day_sales_list
