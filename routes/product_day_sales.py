from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.product_day_sales as product_day_sales
from models.product_day_sale import ProductDaySale, ProductDaySaleBase, ProductDaySaleUpdate
from routes.sessions import manager

apiProductDaySales = APIRouter()


@apiProductDaySales.get("/", response_model=list[ProductDaySale], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    products_day_sale_list: list[ProductDaySale] = await product_day_sales.all()
    return products_day_sale_list


@apiProductDaySales.post("/", response_model=ProductDaySale, status_code=status.HTTP_201_CREATED)
async def create(schema: ProductDaySaleBase, user=Depends(manager)):
    product_day_sale: ProductDaySale = ProductDaySale.from_orm(schema)
    product_day_sale = await product_day_sales.save(product_day_sale)
    return product_day_sale


@apiProductDaySales.get("/{id}", response_model=ProductDaySale, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    product_day_sale: ProductDaySale = await product_day_sales.get(id)
    if product_day_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return product_day_sale


@apiProductDaySales.patch('/{id}', response_model=ProductDaySale, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: ProductDaySaleUpdate, user=Depends(manager)):
    product_day_sale: ProductDaySale = await product_day_sales.get(id)
    if not product_day_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(product_day_sale, key, value)
    product_day_sale = await product_day_sales.save(product_day_sale)
    return product_day_sale


@apiProductDaySales.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    product_day_sale: ProductDaySale = await product_day_sales.get(id)
    if not product_day_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await product_day_sales.delete(product_day_sale)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
