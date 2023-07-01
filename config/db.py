from contextlib import contextmanager

from passlib.context import CryptContext

from config.moreno import engine
from models.type_worker import TypeWorker
from models.worker import Worker
from models.type_place import TypePlace
from models.place import Place
from models.product import Product
from models.day_sale import DaySale
from models.advance import Advance
from models.place_sale import PlaceSale
from models.motion import Motion
from models.product_day_sale import ProductDaySale
from models.transfer import Transfer
from models.product_place_sale import ProductPlaceSale
from sqlmodel import Session as SQLModelSession
from sqlmodel import create_engine, SQLModel


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
