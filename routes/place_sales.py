from fastapi import APIRouter, Response, status, Depends, HTTPException

from controllers import place_sales, day_sales, product_place_sales, transfers, motions, advances
from models import DaySale, ProductPlaceSale, Transfer, Motion, Advance
from models.place_sale import PlaceSaleReadWithDetails, PlaceSaleUpdate, PlaceSale, PlaceSaleRead, PlaceSaleBase, \
    PlaceSaleReadCreateWithDetails, PlaceSaleReadForReport
from routes.users import manager

router = APIRouter()


@router.post("/", response_model=PlaceSaleReadCreateWithDetails, status_code=status.HTTP_201_CREATED)
async def create(schema: PlaceSaleBase, user=Depends(manager)):
    placeSale: PlaceSale = PlaceSale.from_orm(schema)
    placeSale.save()  # idPlaceSale
    daySale: DaySale = day_sales.get(schema.daySale_id)
    for productDaySale in daySale.productDaySales:
        (ProductPlaceSale(productDaySale_id=productDaySale.id, placeSale_id=placeSale.id)).save()  # idProductPlaceSale
    placeSale = place_sales.get(placeSale.id)
    return placeSale


@router.get("/{id}", response_model=PlaceSaleReadWithDetails, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    place_sale: PlaceSaleReadWithDetails = place_sales.get(id)
    if place_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return place_sale


@router.patch('/{id}', response_model=PlaceSaleRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: PlaceSaleUpdate, user=Depends(manager)):
    placeSale: PlaceSale = place_sales.get(id)
    if not placeSale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    workerOld_id: int = placeSale.worker_id
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(placeSale, key, value)

    if placeSale.worker_id != workerOld_id:
        placeSaleModify: PlaceSale = place_sales.get_by_day_sale_and_worker(placeSale.daySale_id, placeSale.worker_id)
        if placeSaleModify:
            placeSaleModify.worker_id = workerOld_id
            placeSaleModify.save()
    return placeSale.save()


@router.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    placeSale: PlaceSale = place_sales.get(id)
    if not placeSale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    daySale_id = placeSale.daySale_id
    placesSalesModifies: list[int] = list()

    for transfer in placeSale.transfersEntry:
        delete_transfer(placesSalesModifies, transfer.id)
    for transfer in placeSale.transfersExit:
        delete_transfer(placesSalesModifies, transfer.id)

    for motion in placeSale.motions:
        motion: Motion = motions.get(motion.id)
        motion.delete()
    for advance in placeSale.advances:
        advance: Advance = advances.get(advance.id)
        advance.delete()

    for productPlaceSale in placeSale.productPlaceSales:
        productPlaceSale: ProductPlaceSale = product_place_sales.get(productPlaceSale.id)
        productPlaceSale.delete()

    placeSale.delete()

    for placeSale_id in placesSalesModifies:
        placeSale = place_sales.get(placeSale_id)
        for productPlaceSale in placeSale.productPlaceSales:
            productPlaceSale: ProductPlaceSale = product_place_sales.get(productPlaceSale.id)
            productPlaceSale.calculate_totals()
            productPlaceSale.save()
        placeSale = place_sales.get(placeSale_id)
        placeSale.calculate_totals()
        placeSale.save()

    daySale: DaySale = day_sales.get(daySale_id)
    daySale.calculate_totals()
    daySale.save()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/worker/{id}/{start}/{end}", response_model=list[PlaceSaleReadForReport],
            status_code=status.HTTP_200_OK)
async def get_by_worker_between(id: int, start: str, end: str, user=Depends(manager)):
    place_sales_list = place_sales.get_by_worker_between(id, start, end)
    return place_sales_list


@router.get("/place/{id}/{start}/{end}", response_model=list[PlaceSaleReadForReport],
            status_code=status.HTTP_200_OK)
async def get_by_place_between(id: int, start: str, end: str, user=Depends(manager)):
    place_sales_list = place_sales.get_by_place_between(id, start, end)
    return place_sales_list


@router.get("/{start}/{end}", response_model=list[PlaceSaleReadForReport],
            status_code=status.HTTP_200_OK)
async def get_between(start: str, end: str, user=Depends(manager)):
    place_sales_list = place_sales.get_between(start, end)
    return place_sales_list


@router.get("/{idWorker}/{idPlace}/{start}/{end}", response_model=list[PlaceSaleReadForReport],
            status_code=status.HTTP_200_OK)
async def get_by_place_worker_between(idWorker: int, idPlace: int, start: str, end: str, user=Depends(manager)):
    place_sales_list = place_sales.get_by_place_worker_between(idWorker, idPlace, start, end)
    return place_sales_list


def delete_transfer(placesSalesModifies: list[int], idTransfer: int):
    if idTransfer not in placesSalesModifies:
        placesSalesModifies.append(idTransfer)
    transfer: Transfer = transfers.get(idTransfer)
    transfer.delete()
