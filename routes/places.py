from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.places as places
from models.place import Place, PlaceBase, PlaceUpdate, PlaceRead, PlaceReadWithType
from routes.sessions import manager

apiPlaces = APIRouter()


@apiPlaces.get("/", response_model=list[PlaceRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    products_day_sale_list: list[PlaceRead] = places.all()
    return products_day_sale_list


@apiPlaces.post("/", response_model=PlaceRead, status_code=status.HTTP_201_CREATED)
async def create(schema: PlaceBase, user=Depends(manager)):
    place: Place = Place.from_orm(schema)
    place.save()
    return place


@apiPlaces.get("/{id}", response_model=PlaceReadWithType, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    place: PlaceReadWithType = places.get(id)
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return place


@apiPlaces.patch('/{id}', response_model=PlaceRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: PlaceUpdate, user=Depends(manager)):
    place: Place = places.get(id)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(place, key, value)
    place.save()
    return place


@apiPlaces.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    place: Place = places.get(id)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    place.active = False
    place.save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
