from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.advances as advances
from controllers import day_sales, place_sales
from models import DaySale, PlaceSale
from models.advance import Advance, AdvanceBase, AdvanceUpdate, AdvanceReadWithDetails, AdvanceRead
from routes.sessions import manager

apiAdvances = APIRouter()


@apiAdvances.post("/", response_model=AdvanceRead, status_code=status.HTTP_201_CREATED)
async def create(schema: AdvanceBase, user=Depends(manager)):
    advance: Advance = Advance.from_orm(schema)
    day_sale_id: int = advance.daySale_id
    advance.save()

    if advance.placeSale_id is not None:
        placeSale: PlaceSale = place_sales.get(advance.placeSale_id)
        day_sale_id: int = placeSale.daySale_id
        placeSale.calculate_totals()
        placeSale.save()
    daySale: DaySale = day_sales.get(day_sale_id)
    daySale.calculate_totals()
    daySale.save()
    return advance


@apiAdvances.get("/{id}", response_model=AdvanceReadWithDetails, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    advance: AdvanceReadWithDetails = advances.get(id)
    if advance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return advance


@apiAdvances.patch('/{id}', response_model=AdvanceRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: AdvanceUpdate, user=Depends(manager)):
    advance: Advance = advances.get(id)
    if not advance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(advance, key, value)

    day_sale_id: int = advance.daySale_id
    advance.save()

    if advance.placeSale_id is not None:
        placeSale: PlaceSale = place_sales.get(advance.placeSale_id)
        day_sale_id: int = placeSale.daySale_id
        placeSale.calculate_totals()
        placeSale.save()
    daySale: DaySale = day_sales.get(day_sale_id)
    daySale.calculate_totals()
    daySale.save()

    return advance


@apiAdvances.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    advance: Advance = advances.get(id)
    if not advance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})

    place_sale_id: int = advance.placeSale_id
    day_sale_id: int = advance.daySale_id
    advance.amount = 0.0
    advance.deleted = True
    advance.save()

    if place_sale_id is not None:
        placeSale: PlaceSale = place_sales.get(place_sale_id)
        day_sale_id: int = placeSale.daySale_id
        placeSale.calculate_totals()
        placeSale.save()
    daySale: DaySale = day_sales.get(day_sale_id)
    daySale.calculate_totals()
    daySale.save()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
