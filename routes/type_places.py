from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.type_places as type_places
from models.type_place import TypePlace, TypePlaceUpdate, TypePlaceCreate, TypePlaceRead
from routes.sessions import manager

apiTypePlaces = APIRouter()


@apiTypePlaces.get("/", response_model=list[TypePlaceRead], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    types_places_list: list[TypePlaceRead] = await type_places.all()
    return types_places_list


@apiTypePlaces.post("/", response_model=TypePlaceRead, status_code=status.HTTP_201_CREATED)
async def create(schema: TypePlaceCreate, user=Depends(manager)):
    type_place: TypePlace = TypePlace.from_orm(schema)
    type_place = await type_places.save(type_place)
    return type_place


@apiTypePlaces.get("/{id}", response_model=TypePlaceRead, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    type_place: TypePlaceRead = await type_places.get(id)
    if type_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return type_place


@apiTypePlaces.patch('/{id}', response_model=TypePlaceRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: TypePlaceUpdate, user=Depends(manager)):
    type_place: TypePlace = await type_places.get(id)
    if not type_place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(type_place, key, value)
    type_place = await type_places.save(type_place)
    return type_place


@apiTypePlaces.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    type_place: TypePlace = await type_places.get(id)
    if not type_place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await type_places.delete(type_place)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
