from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.product_day_sales as product_day_sales
from controllers import day_sales, place_sales, product_place_sales
from models import ProductPlaceSale, PlaceSale
from models.product_day_sale import ProductDaySale, ProductDaySaleBase, ProductDaySaleUpdate, ProductDaySaleReadCreate, \
    ProductDaySaleRead, ProductDaySaleReadReport
from routes.users import manager

router = APIRouter()


@router.post("/", response_model=ProductDaySaleReadCreate, status_code=status.HTTP_201_CREATED)
async def create(schema: ProductDaySaleBase, user=Depends(manager)):
    productDaySale: ProductDaySale = ProductDaySale.from_orm(schema)
    productDaySale = productDaySale.save()  # idProductDaySale

    for placeSale in productDaySale.daySale.placeSales:
        ProductPlaceSale(productDaySale_id=productDaySale.id, placeSale_id=placeSale.id).save()  # idProductPlaceSale
    productDaySale = product_day_sales.get(productDaySale.id)
    return productDaySale


@router.get("/{id}", response_model=ProductDaySale, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    product_day_sale: ProductDaySale = product_day_sales.get(id)
    if product_day_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return product_day_sale


@router.patch('/{id}', response_model=ProductDaySaleRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: ProductDaySaleUpdate, user=Depends(manager)):
    productDaySale: ProductDaySale = product_day_sales.get(id)
    if not productDaySale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(productDaySale, key, value)
    print(productDaySale.price)
    productDaySale.save()
    print(productDaySale.price)
    for productPlaceSale in productDaySale.productPlaceSales:
        productPlaceSale: ProductPlaceSale = product_place_sales.get(productPlaceSale.id)
        productPlaceSale.calculate_totals()
        productPlaceSale.save()

    productDaySale.calculate_totals()
    productDaySale.save()

    daySale = day_sales.get(productDaySale.daySale_id)
    for placeSale in daySale.placeSales:
        placeSale: PlaceSale = place_sales.get(placeSale.id)
        placeSale.calculate_totals()
        placeSale.save()
    daySale = day_sales.get(productDaySale.daySale_id)
    daySale.calculate_totals()
    daySale.save()

    return productDaySale


@router.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    productDaySale: ProductDaySale = product_day_sales.get(id)
    if not productDaySale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    day_sale_id: int = productDaySale.daySale_id

    for productPlaceSale in productDaySale.productPlaceSales:
        productPlaceSale: ProductPlaceSale = product_place_sales.get(productPlaceSale.id)
        productPlaceSale.delete()

    productDaySale.delete()

    daySale = day_sales.get(day_sale_id)
    for placeSale in daySale.placeSales:
        placeSale: PlaceSale = place_sales.get(placeSale.id)
        placeSale.calculate_totals()
        placeSale.save()
    daySale = day_sales.get(day_sale_id)
    daySale.calculate_totals()
    daySale.save()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id}/{start}/{end}", response_model=list[ProductDaySaleReadReport], status_code=status.HTTP_200_OK)
async def get_by_product_between(id: int, start: str, end: str, user=Depends(manager)):
    product_day_sale_list: list[ProductDaySaleReadReport] = product_day_sales.get_by_product_between(id, start, end)
    return product_day_sale_list
