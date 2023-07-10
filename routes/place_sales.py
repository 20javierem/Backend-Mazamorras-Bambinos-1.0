from fastapi import APIRouter, Response, status, Depends, HTTPException

from controllers import place_sales, day_sales, product_place_sales, transfers, motions, advances
from models import DaySale, ProductPlaceSale, Transfer, Motion
from models.place_sale import PlaceSaleReadWithDetails, PlaceSaleUpdate, PlaceSale, PlaceSaleRead, PlaceSaleBase, \
    PlaceSaleReadCreateWithDetails
from routes.sessions import manager

apiPlaceSales = APIRouter()


@apiPlaceSales.get("/", response_model=list[PlaceSaleRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    places_sales_list: list[PlaceSaleRead] = place_sales.all()
    return places_sales_list


@apiPlaceSales.post("/", response_model=PlaceSaleReadCreateWithDetails, status_code=status.HTTP_201_CREATED)
async def create(schema: PlaceSaleBase, user=Depends(manager)):
    placeSale: PlaceSale = PlaceSale.from_orm(schema)
    placeSale.save()  # idPlaceSale
    daySale: DaySale = day_sales.get(schema.daySale_id)
    for productDaySale in daySale.productDaySales:
        (ProductPlaceSale(productDaySale_id=productDaySale.id, placeSale_id=placeSale.id)).save()  # idProductPlaceSale
    placeSale = place_sales.get(placeSale.id)
    return placeSale


@apiPlaceSales.get("/{id}", response_model=PlaceSaleReadWithDetails, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    place_sale: PlaceSaleReadWithDetails = place_sales.get(id)
    if place_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return place_sale


@apiPlaceSales.patch('/{id}', response_model=PlaceSaleRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: PlaceSaleUpdate, user=Depends(manager)):
    placeSale: PlaceSale = place_sales.get(id)
    if not placeSale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    workerOld_id: int = placeSale.worker_id
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(placeSale, key, value)

    if placeSale.worker_id != workerOld_id:
        placeSaleModify: PlaceSale = \
            place_sales.get_by_day_sale_and_worker(placeSale.daySale_id, placeSale.worker_id)
        if placeSaleModify:
            placeSaleModify.worker_id = workerOld_id
            placeSaleModify.save()
    return placeSale.save()


@apiPlaceSales.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    placeSale: PlaceSale = place_sales.get(id)
    if not placeSale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    daySale_id = placeSale.daySale_id
    placesSalesModifies: list[int] = list()

    for transfer in placeSale.transfersEntry:
        placesSalesModifies.append(transfer.source_id)
        transfer: Transfer = transfers.get(transfer.id)
        transfer.quantity = 0
        transfer.deleted = True
        transfer.save()
    for transfer in placeSale.transfersExit:
        placesSalesModifies.append(transfer.destiny_id)
        transfer: Transfer = transfers.get(transfer.id)
        transfer.quantity = 0
        transfer.deleted = True
        transfer.save()

    for motion in placeSale.motions:
        motion: Motion = motions.get(motion.id)
        motion.amount = 0
        motion.deleted = True
        motion.save()
    for advance in placeSale.advances:
        advance: Motion = advances.get(advance.id)
        advance.amount = 0
        advance.deleted = True
        advance.save()

    for placeSale_id in placesSalesModifies:
        placeSale = place_sales.get(placeSale_id)
        for productPlaceSale in placeSale.productPlaceSales:
            productPlaceSale: ProductPlaceSale = product_place_sales.get(productPlaceSale.id)
            productPlaceSale.calculate_totals()
            productPlaceSale.save()
        placeSale = place_sales.get(placeSale_id)
        placeSale.calculate_totals()
        placeSale.save()

    for productPlaceSale in placeSale.productPlaceSales:
        productPlaceSale: ProductPlaceSale = product_place_sales.get(productPlaceSale.id)
        productPlaceSale.quantityInitial = 0
        productPlaceSale.quantityRest = 0
        productPlaceSale.quantitySold = 0
        productPlaceSale.totalSale = 0.0
        productPlaceSale.deleted = True
        productPlaceSale.save()

    placeSale.deleted = True
    placeSale.totalSale = 0.0
    placeSale.totalAdvances = 0.0
    placeSale.totalCurrent = 0.0
    placeSale.totalMotions = 0.0
    placeSale.totalDelivered = 0.0
    placeSale.save()

    daySale: DaySale = day_sales.get(daySale_id)
    daySale.calculate_totals()
    daySale.save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@apiPlaceSales.get("/worker/{id}/{start}/{end}", response_model=list[PlaceSaleReadWithDetails],
                   status_code=status.HTTP_200_OK)
async def get_by_worker_between(id: int, start: str, end: str, user=Depends(manager)):
    place_sales_list = place_sales.get_by_worker_between(id, start, end)
    return place_sales_list


@apiPlaceSales.get("/place/{id}/{start}/{end}", response_model=list[PlaceSaleReadWithDetails],
                   status_code=status.HTTP_200_OK)
async def get_by_place_between(id: int, start: str, end: str, user=Depends(manager)):
    place_sales_list = place_sales.get_by_place_between(id, start, end)
    return place_sales_list
