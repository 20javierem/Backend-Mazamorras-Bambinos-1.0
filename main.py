import uvicorn
from datetime import datetime
from fastapi import FastAPI

from config.db import create_db_and_tables
from controllers import workers, type_workers
from models import TypeWorker, Worker
from routes.advances import apiAdvances
from routes.day_sales import apiDaySales
from routes.motions import apiMotions
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
app.include_router(apiMessageSales, prefix="/message")
app.include_router(apiProducts, prefix="/product")
app.include_router(apiSession)


def main():
    create_db_and_tables()

    if len(type_workers.all()) == 0:
        typeWorker: TypeWorker = TypeWorker()
        typeWorker.description = "VENDEDOR"
        typeWorker.save()

    if len(workers.all()) == 0:
        worker: Worker = Worker()
        worker.typeWorker_id = 1
        worker.dni = "62020554"
        worker.admin = True
        worker.names = "JAVIER ERNESTO"
        worker.lastNames = "MORENO LLOCLLE"
        worker.phone = "940029541"
        worker.salary = 1200.0
        worker.sex = "MASCULINO"
        worker.start = datetime.now()
        worker.birthday = datetime.now()
        worker.save()

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
