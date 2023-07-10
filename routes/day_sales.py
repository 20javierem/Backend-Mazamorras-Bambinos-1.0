from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.day_sales as day_sales
from models import PlaceSale, ProductDaySale
from models.day_sale import DaySale, DaySaleBase, DaySaleUpdate, DaySaleReadWithDetails, DaySaleRead, DaySaleReadCreate
from routes.sessions import manager
from models.product_place_sale import ProductPlaceSale

apiDaySales = APIRouter()


@apiDaySales.get("/", response_model=list[DaySaleRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    day_sales_list = day_sales.get_all()
    return day_sales_list


@apiDaySales.post("/", response_model=DaySaleReadCreate, status_code=status.HTTP_201_CREATED)
async def create(schema: DaySaleBase, user=Depends(manager)):
    daySale: DaySale = DaySale.from_orm(schema)
    if day_sales.get_of_date(str(daySale.date)) is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "Date registered"})
    daySale = daySale.save()  # idDaySale

    for product_day_sale in schema.productDaySales:
        productDaySale: ProductDaySale = ProductDaySale.from_orm(product_day_sale)
        productDaySale.daySale_id = daySale.id
        productDaySale.save()  # idProductDaySale

    daySale = day_sales.get(daySale.id)

    for placeSale in schema.placeSales:
        placeSale = PlaceSale.from_orm(placeSale)
        placeSale.daySale_id = daySale.id
        placeSale = placeSale.save()  # idPlaceSale
        for productDaySale in daySale.productDaySales:
            await (ProductPlaceSale(
                productDaySale_id=productDaySale.id,
                placeSale_id=placeSale.id)
            ).save()  # idProductPlaceSale

    daySale = day_sales.get(daySale.id)
    return daySale


@apiDaySales.get("/{id}", response_model=DaySaleReadWithDetails, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    day_sale: DaySale = day_sales.get(id)
    if day_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return day_sale


@apiDaySales.patch('/{id}', response_model=DaySaleReadWithDetails, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: DaySaleUpdate, user=Depends(manager)):
    day_sale: DaySale = day_sales.get(id)
    if not day_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(day_sale, key, value)
    day_sale.save()
    return day_sale

@apiDaySales.get("/date/{date}", response_model=DaySaleReadWithDetails, status_code=status.HTTP_200_OK)
async def get_by_date(date: str, user=Depends(manager)):
    day_sale: DaySale = day_sales.get_of_date(date)
    if day_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return day_sale


@apiDaySales.get("/between/{start}/{end}", response_model=list[DaySale], status_code=status.HTTP_200_OK)
async def get_between(start: str, end: str, user=Depends(manager)):
    day_sales_list: list[DaySale] = day_sales.get_by_range_of_date(start, end)
    return day_sales_list
