from config.moreno import Session
from models.advance import Advance


def get(id: int):
    with Session() as session:
        return session.get(Advance, id)
