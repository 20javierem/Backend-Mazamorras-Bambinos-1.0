from sqlmodel import select
from config.moreno import Session
from models.user import User


def all():
    with Session() as session:
        statement = select(User)
        return session.exec(statement).all()


def getByUsername(username: str):
    with Session() as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()
