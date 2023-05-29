from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.transfers as transfers
from models.transfer import Transfer, TransferUpdate, TransferBase, TransferRead
from routes.sessions import manager

apiTransfers = APIRouter()


@apiTransfers.get("/", response_model=list[TransferRead], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    transfers_list: list[TransferRead] = await transfers.all()
    return transfers_list


@apiTransfers.post("/", response_model=TransferRead, status_code=status.HTTP_201_CREATED)
async def create(schema: TransferBase, user=Depends(manager)):
    transfer: Transfer = Transfer.from_orm(schema)
    transfer: TransferRead = await transfers.save(transfer)
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
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(transfer, key, value)
    transfer: TransferRead = await transfers.save(transfer)
    return transfer


@apiTransfers.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    transfer: Transfer = await transfers.get(id)
    if not transfer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await transfers.delete(transfer)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
