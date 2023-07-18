from config.moreno import Session
from models.motion import Motion


def get(id: int):
    with Session() as session:
        return session.get(Motion, id)
