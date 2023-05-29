from fastapi import APIRouter, Response, status, Depends, HTTPException

from controllers import place_sales
from models.place_sale import PlaceSaleReadWithDetails, PlaceSaleBase, PlaceSaleUpdate, PlaceSale, PlaceSaleRead
from routes.sessions import manager

apiPlaceSales = APIRouter()


@apiPlaceSales.get("/", response_model=list[PlaceSaleRead], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    places_sales_list: list[PlaceSaleRead] = await place_sales.all()
    return places_sales_list


@apiPlaceSales.post("/", response_model=PlaceSaleReadWithDetails, status_code=status.HTTP_201_CREATED)
async def create(schema: PlaceSaleBase, user=Depends(manager)):
    place_sale: PlaceSale = PlaceSale.from_orm(schema)
    place_sale: PlaceSaleReadWithDetails = await place_sales.save(place_sale)
    return place_sale


@apiPlaceSales.get("/{id}", response_model=PlaceSaleReadWithDetails, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    place_sale: PlaceSaleReadWithDetails = await place_sales.get(id)
    if place_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return place_sale


@apiPlaceSales.patch('/{id}', response_model=PlaceSaleReadWithDetails, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: PlaceSaleUpdate, user=Depends(manager)):
    place_sale: PlaceSale = await place_sales.get(id)
    if not place_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(place_sale, key, value)
    place_sale: PlaceSaleReadWithDetails = await place_sales.save(place_sale)
    return place_sale


@apiPlaceSales.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    place_sale: PlaceSale = await place_sales.get(id)
    if not place_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await place_sales.delete(place_sale)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@apiPlaceSales.get("/worker/{id}/{start}/{end}", response_model=list[PlaceSaleReadWithDetails], status_code=status.HTTP_200_OK)
async def get_by_worker_between(id: int, start: str, end: str, user=Depends(manager)):
    place_sales_list = await place_sales.getByWorkerBetween(id, start, end)
    return place_sales_list


@apiPlaceSales.get("/place/{id}/{start}/{end}", response_model=list[PlaceSaleReadWithDetails], status_code=status.HTTP_200_OK)
async def get_by_place_between(id: int, start: str, end: str, user=Depends(manager)):
    place_sales_list = await place_sales.getByPlaceBetween(id, start, end)
    return place_sales_list
