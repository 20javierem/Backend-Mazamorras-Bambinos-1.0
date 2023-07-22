import uvicorn
from fastapi import FastAPI

from config.db import create_db_and_tables
from controllers import users
from models.user import User, UserBase
from routes.advances import router as router_advances
from routes.day_sales import router as router_day_sales
from routes.motions import router as router_motions
from routes.place_sales import router as router_place_sales
from routes.places import router as router_places
from routes.product_day_sales import router as router_product_day_sales
from routes.product_place_sales import router as router_product_place_sales
from routes.products import router as router_products
from routes.users import router as router_users
from routes.transfers import router as router_transfers
from routes.type_places import router as router_type_places
from routes.type_workers import router as router_type_workers
from routes.workers import router as router_workers

create_db_and_tables()
app = FastAPI()


# para filtrar por atributo on relation_Ship
# "primaryjoin": "Motion.deleted==False"

@app.get("/")
async def root():
    return "bienvenido"


app.include_router(router_type_places, prefix="/type-place")
app.include_router(router_type_workers, prefix="/type-worker")
app.include_router(router_day_sales, prefix="/day-sale")
app.include_router(router_place_sales, prefix="/place-sale")
app.include_router(router_places, prefix="/place")
app.include_router(router_product_day_sales, prefix="/product-day-sale")
app.include_router(router_product_place_sales, prefix="/product-place-sale")
app.include_router(router_transfers, prefix="/transfer")
app.include_router(router_workers, prefix="/worker")
app.include_router(router_advances, prefix="/advance")
app.include_router(router_motions, prefix="/motion")
app.include_router(router_products, prefix="/product")
app.include_router(router_users, prefix="/user")

if __name__ == "__main__":
    create_db_and_tables()

    if len(users.all()) == 0:
        user: UserBase = User()
        user.firstnames = "admin"
        user.lastnames = "admin"
        user.username = "admin"
        user.password = "admin"
        user.admin = True
        User.from_orm(user).save()

    uvicorn.run(app, host="0.0.0.0", port=8000)
