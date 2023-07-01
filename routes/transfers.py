from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.transfers as transfers
from controllers import place_sales, product_place_sales
from models import PlaceSale, ProductPlaceSale
from models.transfer import Transfer, TransferUpdate, TransferBase, TransferRead
from routes.sessions import manager

apiTransfers = APIRouter()


@apiTransfers.get("/", response_model=list[TransferRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    transfers_list: list[TransferRead] = await transfers.all()
    return transfers_list


@apiTransfers.post("/", response_model=TransferRead, status_code=status.HTTP_201_CREATED)
async def create(schema: TransferBase, user=Depends(manager)):
    transfer: Transfer = Transfer.from_orm(schema)
    await transfer.save()

    source: PlaceSale = await place_sales.get(transfer.source_id)
    await update_totals(source, transfer.productDaySale_id)

    destiny: PlaceSale = await place_sales.get(transfer.destiny_id)
    await update_totals(destiny, transfer.productDaySale_id)

    return transfer


@apiTransfers.get("/{id}", response_model=TransferRead, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    transfer: TransferRead = await transfers.get(id)
    if transfer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return transfer


@apiTransfers.patch('/{id}', response_model=TransferRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: TransferUpdate, user=Depends(manager)):
    transfer: Transfer = await transfers.get(id)
    if not transfer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})

    source: PlaceSale = await place_sales.get(transfer.source_id)
    destiny: PlaceSale = await place_sales.get(transfer.destiny_id)

    transfer: Transfer = await transfers.get(id)
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(transfer, key, value)
    await transfer.save()

    await update_totals(source, transfer.productDaySale_id)
    await update_totals(destiny, transfer.productDaySale_id)

    source: PlaceSale = await place_sales.get(transfer.source_id)
    destiny: PlaceSale = await place_sales.get(transfer.destiny_id)

    await update_totals(source, transfer.productDaySale_id)
    await update_totals(destiny, transfer.productDaySale_id)

    return transfer


@apiTransfers.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    transfer: Transfer = await transfers.get(id)
    if not transfer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})

    source: PlaceSale = await place_sales.get(transfer.source_id)
    destiny: PlaceSale = await place_sales.get(transfer.destiny_id)
    await transfer.delete()

    await update_totals(source, transfer.productDaySale_id)
    await update_totals(destiny, transfer.productDaySale_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def update_totals(placeSale: PlaceSale, productDaySale_id: int):
    productPlaceSale: ProductPlaceSale = list(
        filter(lambda productPlaceSale1: productPlaceSale1.productDaySale_id == productDaySale_id,
               placeSale.productPlaceSales)).__getitem__(0)

    productPlaceSale = await product_place_sales.get(productPlaceSale.id)
    productPlaceSale.calculate_totals()
    await productPlaceSale.save()

    placeSale: PlaceSale = await place_sales.get(placeSale.id)
    placeSale.calculate_totals()
    await placeSale.save()
