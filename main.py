import uvicorn
from datetime import datetime
from fastapi import FastAPI

from config.db import create_db_and_tables
from controllers import workers, type_workers, users
from models import TypeWorker, Worker
from models.user import User
from routes.advances import apiAdvances
from routes.day_sales import apiDaySales
from routes.motions import apiMotions
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


# para filtrar por atributo on relation_Ship
# "primaryjoin": "Motion.deleted==False"

@app.get("/")
async def root():
    return "bienvenido"


app.include_router(apiTypePlaces, prefix="/type-place")
app.include_router(apiTypeWorkers, prefix="/type-worker")
app.include_router(apiDaySales, prefix="/day-sale")
app.include_router(apiPlaceSales, prefix="/place-sale")
app.include_router(apiPlaces, prefix="/place")
app.include_router(apiProductDaySales, prefix="/product-day-sale")
app.include_router(apiProductPlaceSales, prefix="/product-place-sale")
app.include_router(apiTransfers, prefix="/transfer")
app.include_router(apiWorkers, prefix="/worker")
app.include_router(apiAdvances, prefix="/advance")
app.include_router(apiMotions, prefix="/motion")
app.include_router(apiProducts, prefix="/product")
app.include_router(apiSession)

if __name__ == "__main__":
    create_db_and_tables()

    if len(users.all()) == 0:
        user: User = User()
        user.username = "admin"
        user.password = "admin"
        user.save()

    uvicorn.run(app, host="0.0.0.0", port=8000)
