from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.product_place_sales as product_place_sales
from controllers import place_sales, product_day_sales, day_sales
from models.product_place_sale import ProductPlaceSale, ProductPlaceSaleUpdate, ProductPlaceSaleCreate, \
    ProductPlaceSaleReadDaySaleCreate, ProductPlaceSaleRead
from routes.sessions import manager

apiProductPlaceSales = APIRouter()


@apiProductPlaceSales.get("/", response_model=list[ProductPlaceSale], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    products_place_sale_list: list[ProductPlaceSale] = await product_place_sales.all()
    return products_place_sale_list


@apiProductPlaceSales.post("/", response_model=ProductPlaceSaleReadDaySaleCreate, status_code=status.HTTP_201_CREATED)
async def create(schema: ProductPlaceSaleCreate, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = ProductPlaceSale.from_orm(schema)
    await product_place_sale.save()

    product_place_sale.calculate_totals()
    await product_place_sale.save()

    placeSale = await place_sales.get(product_place_sale.placeSale_id)
    placeSale.calculate_totals()
    await placeSale.save()

    productDaySale = await product_day_sales.get(product_place_sale.productDaySale_id)
    productDaySale.calculate_totals()
    await productDaySale.save()

    daySale = await day_sales.get(product_place_sale.productDaySale.daySale_id)
    daySale.calculate_totals()
    await daySale.save()

    return product_place_sale


@apiProductPlaceSales.get("/{id}", response_model=ProductPlaceSale, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = await product_place_sales.get(id)
    if product_place_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return product_place_sale


@apiProductPlaceSales.patch('/{id}', response_model=ProductPlaceSaleRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: ProductPlaceSaleUpdate, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = await product_place_sales.get(id)
    if not product_place_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(product_place_sale, key, value)

    product_place_sale.calculate_totals()
    await product_place_sale.save()

    placeSale = await place_sales.get(product_place_sale.placeSale_id)
    placeSale.calculate_totals()
    await placeSale.save()

    productDaySale = await product_day_sales.get(product_place_sale.productDaySale_id)
    productDaySale.calculate_totals()
    await productDaySale.save()

    daySale = await day_sales.get(product_place_sale.productDaySale.daySale_id)
    daySale.calculate_totals()
    await daySale.save()

    return product_place_sale


@apiProductPlaceSales.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = await product_place_sales.get(id)
    if not product_place_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await product_place_sale.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
