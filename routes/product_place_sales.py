from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.product_place_sales as product_place_sales
from models.product_place_sale import ProductPlaceSale, ProductPlaceSaleUpdate
from routes.sessions import manager

apiProductPlaceSales = APIRouter()


@apiProductPlaceSales.get("/", response_model=list[ProductPlaceSale], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    products_place_sale_list: list[ProductPlaceSale] = await product_place_sales.all()
    return products_place_sale_list


@apiProductPlaceSales.get("/{id}", response_model=ProductPlaceSale, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = await product_place_sales.get(id)
    if product_place_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return product_place_sale


@apiProductPlaceSales.patch('/{id}', response_model=ProductPlaceSale, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: ProductPlaceSaleUpdate, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = await product_place_sales.get(id)
    if not product_place_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(product_place_sale, key, value)
    product_place_sale = await product_place_sales.save(product_place_sale)
    return product_place_sale


@apiProductPlaceSales.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = await product_place_sales.get(id)
    if not product_place_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await product_place_sales.delete(product_place_sale)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
