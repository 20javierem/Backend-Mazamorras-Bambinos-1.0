from fastapi import APIRouter, Response, status, Depends, HTTPException

from controllers import place_sales, day_sales, product_place_sales, transfers, workers, motions, advances
from models import DaySale, ProductPlaceSale, Worker
from models.place_sale import PlaceSaleReadWithDetails, PlaceSaleUpdate, PlaceSale, PlaceSaleRead, PlaceSaleBase, \
    PlaceSaleReadCreateWithDetails
from routes.sessions import manager

apiPlaceSales = APIRouter()


@apiPlaceSales.get("/", response_model=list[PlaceSaleRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    places_sales_list: list[PlaceSaleRead] = await place_sales.all()
    return places_sales_list


@apiPlaceSales.post("/", response_model=PlaceSaleReadCreateWithDetails, status_code=status.HTTP_201_CREATED)
async def create(schema: PlaceSaleBase, user=Depends(manager)):
    placeSale: PlaceSale = PlaceSale.from_orm(schema)
    await placeSale.save()  # idPlaceSale
    daySale: DaySale = await day_sales.get(schema.daySale_id)
    for productDaySale in daySale.productDaySales:
        await (ProductPlaceSale(
            productDaySale_id=productDaySale.id,
            placeSale_id=placeSale.id)
        ).save()  # idProductPlaceSale
    placeSale = await place_sales.get(placeSale.id)
    return placeSale


@apiPlaceSales.get("/{id}", response_model=PlaceSaleReadWithDetails, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    place_sale: PlaceSaleReadWithDetails = await place_sales.get(id)
    if place_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return place_sale


@apiPlaceSales.patch('/{id}', response_model=PlaceSaleRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: PlaceSaleUpdate, user=Depends(manager)):
    placeSale: PlaceSale = await place_sales.get(id)
    workerOld: Worker = placeSale.worker
    if not placeSale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(placeSale, key, value)
    workerNew: Worker = await workers.get(placeSale.worker_id)
    if workerNew.id != workerOld.id:
        placeSaleModify: PlaceSale = await place_sales.getByDaySaleWorker(placeSale.daySale_id, workerNew.id)
        placeSaleModify.worker_id = workerOld.id
        await placeSaleModify.save()
    return await placeSale.save()


@apiPlaceSales.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    place_sale: PlaceSale = await place_sales.get(id)
    daySale_id = place_sale.daySale_id
    if not place_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    placesSalesModifies: list[int] = list()

    for transfer in place_sale.transfersEntry:
        placesSalesModifies.append(transfer.source_id)
        await (await transfers.get(transfer.id)).delete()
    for transfer in place_sale.transfersExit:
        placesSalesModifies.append(transfer.destiny_id)
        await (await transfers.get(transfer.id)).delete()

    for motion in place_sale.motions:
        await (await motions.get(motion.id)).delete()
    for advance in place_sale.advances:
        await (await advances.get(advance.id)).delete()

    for placeSale_id in placesSalesModifies:
        placeSale = await place_sales.get(placeSale_id)
        for productPlaceSale in placeSale.productPlaceSales:
            productPlaceSale: ProductPlaceSale = await product_place_sales.get(productPlaceSale.id)
            productPlaceSale.calculate_totals()
            await productPlaceSale.save()
        placeSale = await place_sales.get(placeSale_id)
        placeSale.calculate_totals()
        await placeSale.save()

    for productPlaceSale in place_sale.productPlaceSales:
        await (await product_place_sales.get(productPlaceSale.id)).delete()

    await place_sale.delete()
    daySale: DaySale = await day_sales.get(daySale_id)
    daySale.calculate_totals()
    await daySale.save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@apiPlaceSales.get("/worker/{id}/{start}/{end}", response_model=list[PlaceSaleReadWithDetails],
                   status_code=status.HTTP_200_OK)
async def get_by_worker_between(id: int, start: str, end: str, user=Depends(manager)):
    place_sales_list = await place_sales.getByWorkerBetween(id, start, end)
    return place_sales_list


@apiPlaceSales.get("/place/{id}/{start}/{end}", response_model=list[PlaceSaleReadWithDetails],
                   status_code=status.HTTP_200_OK)
async def get_by_place_between(id: int, start: str, end: str, user=Depends(manager)):
    place_sales_list = await place_sales.getByPlaceBetween(id, start, end)
    return place_sales_list
