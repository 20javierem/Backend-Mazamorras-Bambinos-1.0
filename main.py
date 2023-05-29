import uvicorn
from fastapi import FastAPI

from config.db import create_db_and_tables
from routes.advances import apiAdvances
from routes.day_sales import apiDaySales
from routes.expenses import apiExpenses
from routes.message_day_sales import apiMessageSales
from routes.place_sales import apiPlaceSales
from routes.places import apiPlaces
from routes.product_day_sales import apiProductDaySales
from routes.product_place_sales import apiProductPlaceSales
from routes.products import apiProducts
from routes.sessions import apiSession
from routes.transfers import apiTransfers
from routes.type_places import apiTypePlaces
from routes.type_workers import apiTypeWorkers
from routes.workers import apiWorkers
create_db_and_tables()
app = FastAPI()


@app.get("/")
async def root():
    return "bienvenido"


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": {"Error": exc.errors()[0]['msg']}}),
#     )

app.include_router(apiTypePlaces, prefix="/type-place")
app.include_router(apiTypeWorkers, prefix="/type-worker")

app.include_router(apiDaySales, prefix="/day-sale")
app.include_router(apiExpenses, prefix="/expense")
app.include_router(apiPlaceSales, prefix="/place-sale")
app.include_router(apiPlaces, prefix="/place")
app.include_router(apiProductDaySales, prefix="/product-day-sale")
app.include_router(apiProductPlaceSales, prefix="/product-place-sale")
app.include_router(apiTransfers, prefix="/transfer")
app.include_router(apiWorkers, prefix="/worker")
app.include_router(apiAdvances, prefix="/advance")
app.include_router(apiMessageSales, prefix="/message")
app.include_router(apiProducts, prefix="/product")
app.include_router(apiSession)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="localhost", port=8000)
