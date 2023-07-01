from contextlib import contextmanager

from sqlmodel import Session as SQLModelSession, create_engine

engine = create_engine('mysql+pymysql://root@localhost:3306/dbPrueba-1.0', echo=False)


class Moreno:
    __config__ = None

    async def save(self):
        with Session() as session:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self

    async def delete(self):
        with Session() as session:
            session.delete(self)
            session.commit()


@contextmanager
def Session() -> SQLModelSession:
    session = SQLModelSession(engine)
    try:
        yield session
    finally:
        session.close()
