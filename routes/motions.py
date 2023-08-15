from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.motions as motions
from controllers import place_sales, day_sales
from models import PlaceSale, DaySale
from models.motion import Motion, MotionUpdate, MotionRead, MotionBase, MotionWithDetails
from routes.users import manager

router = APIRouter()


@router.post("/", response_model=MotionRead, status_code=status.HTTP_201_CREATED)
async def create(schema: MotionBase, user=Depends(manager)):
    motion: Motion = Motion.from_orm(schema)
    if motion.placeSale_id is not None:
        motion.daySale_id = None
        motion.save()
        placeSale: PlaceSale = place_sales.get(motion.placeSale_id)
        placeSale.calculate_totals()
        placeSale.save()
        daySale: DaySale = day_sales.get(motion.placeSale.daySale_id)
        daySale.calculate_totals()
        daySale.save()
    else:
        motion.save()
        daySale: DaySale = day_sales.get(motion.daySale_id)
        daySale.calculate_totals()
        daySale.save()
    return motion


@router.get("/{id}", response_model=MotionRead, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    motion: MotionRead = motions.get(id)
    if motion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return motion


@router.patch('/{id}', response_model=Motion, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: MotionUpdate, user=Depends(manager)):
    motion: Motion = motions.get(id)
    if not motion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(motion, key, value)
    place_sale_id: int = motion.placeSale_id
    day_sale_id: int = motion.daySale_id
    motion.save()

    if place_sale_id is not None:
        placeSale: PlaceSale = place_sales.get(place_sale_id)
        day_sale_id: int = placeSale.daySale_id
        placeSale.calculate_totals()
        placeSale.save()
    daySale: DaySale = day_sales.get(day_sale_id)
    daySale.calculate_totals()
    daySale.save()

    return motion


@router.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    motion: Motion = motions.get(id)
    if not motion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    place_sale_id: int = motion.placeSale_id
    day_sale_id: int = motion.daySale_id
    motion.delete()

    if place_sale_id is not None:
        placeSale: PlaceSale = place_sales.get(place_sale_id)
        day_sale_id: int = placeSale.daySale_id
        placeSale.calculate_totals()
        placeSale.save()
    daySale: DaySale = day_sales.get(day_sale_id)
    daySale.calculate_totals()
    daySale.save()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{start}/{end}", response_model=list[MotionWithDetails], status_code=status.HTTP_200_OK)
async def get_between(start: str, end: str, user=Depends(manager)):
    motions_list: list[Motion] = motions.get_between(start, end)
    motions_list.extend(motions.get_between2(start, end))
    motions_list.sort(key=lambda x: (x.placeSale.daySale.date, x.daySale.date))
    return motions_list

