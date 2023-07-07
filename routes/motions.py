from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.motions as expenses
from controllers import place_sales, day_sales
from models import PlaceSale, DaySale
from models.motion import Motion, MotionUpdate, MotionRead, MotionBase
from routes.sessions import manager

apiMotions = APIRouter()


@apiMotions.get("/", response_model=list[MotionRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    products_day_sale_list: list[MotionRead] = await expenses.all()
    return products_day_sale_list


@apiMotions.post("/deletes", response_model=list[int], status_code=status.HTTP_200_OK)
async def get_deletes(ids_motions: list[int], user=Depends(manager)):
    deletes: list[int] = list()
    for id_motion in ids_motions:
        motion: Motion = await expenses.get(id_motion)
        if motion is None:
            deletes.append(id_motion)
    return deletes


@apiMotions.post("/", response_model=MotionRead, status_code=status.HTTP_201_CREATED)
async def create(schema: MotionBase, user=Depends(manager)):
    motion: Motion = Motion.from_orm(schema)
    if motion.placeSale_id is not None:
        motion.daySale_id = None
        await motion.save()
        placeSale: PlaceSale = await place_sales.get(motion.placeSale_id)
        placeSale.calculate_totals()
        await placeSale.save()
        daySale: DaySale = await day_sales.get(motion.placeSale.daySale_id)
        daySale.calculate_totals()
        await daySale.save()
    else:
        await motion.save()
        daySale: DaySale = await day_sales.get(motion.daySale_id)
        daySale.calculate_totals()
        await daySale.save()
    return motion


@apiMotions.get("/{id}", response_model=MotionRead, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    motion: MotionRead = await expenses.get(id)
    if motion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return motion


@apiMotions.patch('/{id}', response_model=Motion, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: MotionUpdate, user=Depends(manager)):
    motion: Motion = await expenses.get(id)
    if not motion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(motion, key, value)
    place_sale_id: int = motion.placeSale_id
    day_sale_id: int = motion.daySale_id
    await motion.save()

    if place_sale_id is not None:
        placeSale: PlaceSale = await place_sales.get(place_sale_id)
        day_sale_id: int = placeSale.daySale_id
        placeSale.calculate_totals()
        await placeSale.save()
    daySale: DaySale = await day_sales.get(day_sale_id)
    daySale.calculate_totals()
    await daySale.save()

    return motion


@apiMotions.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    motion: Motion = await expenses.get(id)
    if not motion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    place_sale_id: int = motion.placeSale_id
    day_sale_id: int = motion.daySale_id
    await motion.delete()

    if place_sale_id is not None:
        placeSale: PlaceSale = await place_sales.get(place_sale_id)
        day_sale_id: int = placeSale.daySale_id
        placeSale.calculate_totals()
        await placeSale.save()
    daySale: DaySale = await day_sales.get(day_sale_id)
    daySale.calculate_totals()
    await daySale.save()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
