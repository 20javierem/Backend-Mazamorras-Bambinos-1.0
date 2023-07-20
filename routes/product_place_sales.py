from fastapi import APIRouter, status, Depends, HTTPException

import controllers.product_place_sales as product_place_sales
from controllers import place_sales, product_day_sales, day_sales
from models.product_place_sale import ProductPlaceSale, ProductPlaceSaleUpdate, ProductPlaceSaleCreate, \
    ProductPlaceSaleReadDaySaleCreate, ProductPlaceSaleRead, ProductPlaceSaleReadReport
from routes.users import manager

router = APIRouter()


@router.post("/", response_model=ProductPlaceSaleReadDaySaleCreate, status_code=status.HTTP_201_CREATED)
async def create(schema: ProductPlaceSaleCreate, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = ProductPlaceSale.from_orm(schema)
    product_place_sale.save()

    product_place_sale.calculate_totals()
    product_place_sale.save()

    placeSale = place_sales.get(product_place_sale.placeSale_id)
    placeSale.calculate_totals()
    placeSale.save()

    productDaySale = product_day_sales.get(product_place_sale.productDaySale_id)
    productDaySale.calculate_totals()
    productDaySale.save()

    daySale = day_sales.get(product_place_sale.productDaySale.daySale_id)
    daySale.calculate_totals()
    daySale.save()

    return product_place_sale


@router.get("/{id}", response_model=ProductPlaceSale, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = product_place_sales.get(id)
    if product_place_sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return product_place_sale


@router.patch('/{id}', response_model=ProductPlaceSaleRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: ProductPlaceSaleUpdate, user=Depends(manager)):
    product_place_sale: ProductPlaceSale = product_place_sales.get(id)
    if not product_place_sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(product_place_sale, key, value)

    product_place_sale.calculate_totals()
    product_place_sale.save()

    placeSale = place_sales.get(product_place_sale.placeSale_id)
    placeSale.calculate_totals()
    placeSale.save()

    productDaySale = product_day_sales.get(product_place_sale.productDaySale_id)
    productDaySale.calculate_totals()
    productDaySale.save()

    daySale = day_sales.get(product_place_sale.productDaySale.daySale_id)
    daySale.calculate_totals()
    daySale.save()

    return product_place_sale


@router.get("/worker/{idProduct}/{idWorker}/{start}/{end}", response_model=list[ProductPlaceSaleReadReport],
            status_code=status.HTTP_200_OK)
async def get_by_product_worker(idProduct: int, idWorker: int, start: str, end: str, user=Depends(manager)):
    product_place_sale_list: list[ProductPlaceSaleReadReport] = product_place_sales.get_by_product_and_worker(
        idProduct, idWorker, start, end)
    return product_place_sale_list


@router.get("/place/{idProduct}/{idPlace}/{start}/{end}", response_model=list[ProductPlaceSaleReadReport],
            status_code=status.HTTP_200_OK)
def get_by_product_place(idProduct: int, idPlace: int, start: str, end: str, user=Depends(manager)):
    product_place_sale_list: list[ProductPlaceSaleReadReport] = product_place_sales.get_by_product_and_place(
        idProduct, idPlace, start, end)
    return product_place_sale_list


@router.get("/{idProduct}/{idWorker}/{idPlace}/{start}/{end}", response_model=list[ProductPlaceSaleReadReport],
            status_code=status.HTTP_200_OK)
async def get_by_product_place_worker(idProduct: int, idWorker: int, idPlace: int, start: str, end: str,
                                      user=Depends(manager)):
    product_place_sale_list: list[ProductPlaceSaleReadReport] = product_place_sales.get_by_product_and_place_and_worker(
        idProduct, idWorker, idPlace, start, end)
    print(len(product_place_sale_list))
    return product_place_sale_list


@router.get("/{id}/{start}/{end}", response_model=list[ProductPlaceSaleReadReport], status_code=status.HTTP_200_OK)
async def get_by_product_between(id: int, start: str, end: str, user=Depends(manager)):
    product_place_sale_list: list[ProductPlaceSaleReadReport] = product_place_sales.get_by_product(id, start, end)
    return product_place_sale_list
