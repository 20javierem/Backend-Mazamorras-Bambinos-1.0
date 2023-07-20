from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.products as products
from models.product import Product, ProductUpdate, ProductCreate, ProductRead
from routes.users import manager

router = APIRouter()


@router.get("/", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
async def get_all(user=Depends(manager)):
    places_list: list[ProductRead] = products.all()
    return places_list


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create(schema: ProductCreate, user=Depends(manager)):
    product: Product = Product.from_orm(schema)
    product.save()
    return product


@router.get("/{id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    product: ProductRead = products.get(id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return product


@router.patch('/{id}', response_model=ProductRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: ProductUpdate, user=Depends(manager)):
    product: Product = products.get(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(product, key, value)
    product.save()
    return product


@router.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    product: Product = products.get(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    product.active = False
    product.save()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
