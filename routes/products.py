from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.products as products
from models.product import Product, ProductUpdate, ProductCreate, ProductRead
from routes.sessions import manager

apiProducts = APIRouter()


@apiProducts.get("/", response_model=list[ProductRead], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    places_list: list[ProductRead] = await products.all()
    return places_list


@apiProducts.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create(schema: ProductCreate, user=Depends(manager)):
    product: Product = Product.from_orm(schema)
    product: ProductRead = await products.save(product)
    return product


@apiProducts.get("/{id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    product: ProductRead = await products.get(id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return product


@apiProducts.patch('/{id}', response_model=ProductRead, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: ProductUpdate, user=Depends(manager)):
    product: Product = await products.get(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(product, key, value)
    product: ProductRead = await products.save(product)
    return product


@apiProducts.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    product: Product = await products.get(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    if products.hasDependences(product):
        product.active = False
        await products.save(product)
    else:
        await products.delete(product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
