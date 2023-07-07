from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.places as places
from models.place import Place, PlaceBase, PlaceUpdate, PlaceRead, PlaceReadWithType
from routes.sessions import manager

apiPlaces = APIRouter()


@apiPlaces.get("/", response_model=list[PlaceRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    products_day_sale_list: list[PlaceRead] = await places.all()
    return products_day_sale_list


@apiPlaces.post("/deletes", response_model=list[int], status_code=status.HTTP_200_OK)
async def get_deletes(ids_places: list[int], user=Depends(manager)):
    deletes: list[int] = list()
    for id_place in ids_places:
        place: PlaceReadWithType = await places.get(id_place)
        if place is None:
            deletes.append(id_place)
    return deletes


@apiPlaces.post("/", response_model=PlaceRead, status_code=status.HTTP_201_CREATED)
async def create(schema: PlaceBase, user=Depends(manager)):
    place: Place = Place.from_orm(schema)
    await place.save()
    return place


@apiPlaces.get("/{id}", response_model=PlaceReadWithType, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    place: PlaceReadWithType = await places.get(id)
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return place


@apiPlaces.patch('/{id}', response_model=PlaceRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: PlaceUpdate, user=Depends(manager)):
    place: Place = await places.get(id)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(place, key, value)
    await place.save()
    return place


@apiPlaces.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    place: Place = await places.get(id)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    if await places.hasDependences(place):
        place.active = False
        await place.save()
    else:
        await place.save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
