from fastapi import APIRouter, Response, status, Depends, HTTPException

import controllers.expences as expenses
from models.expense import Expense, ExpenseCreate, ExpenseUpdate, ExpenseRead
from routes.sessions import manager

apiExpenses = APIRouter()


@apiExpenses.get("/", response_model=list[ExpenseRead], status_code=status.HTTP_200_OK)
async def all(user=Depends(manager)):
    products_day_sale_list: list[ExpenseRead] = await expenses.all()
    return products_day_sale_list


@apiExpenses.post("/", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
async def create(schema: ExpenseCreate, user=Depends(manager)):
    expense: Expense = Expense.from_orm(schema)
    expense: ExpenseRead = await expenses.save(expense)
    return expense


@apiExpenses.get("/{id}", response_model=ExpenseRead, status_code=status.HTTP_200_OK)
async def get(id: int, user=Depends(manager)):
    expense: ExpenseRead = await expenses.get(id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    return expense


@apiExpenses.patch('/{id}', response_model=Expense, status_code=status.HTTP_202_ACCEPTED)
async def update(id: int, schema: ExpenseUpdate, user=Depends(manager)):
    expense: Expense = await expenses.get(id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(expense, key, value)
    expense: ExpenseRead = await expenses.save(expense)
    return expense


@apiExpenses.delete('/{id}')
async def delete(id: int, user=Depends(manager)):
    expense: Expense = await expenses.get(id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "not found"})
    await expenses.delete(expense)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
