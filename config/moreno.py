from contextlib import contextmanager

from sqlmodel import Session as SQLModelSession, create_engine

engine = create_engine('mysql+pymysql://root@localhost:3306/dbbambinos1', echo=False)


class Moreno:
    __config__ = None

    def save(self):
        with Session() as session:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self


@contextmanager
def Session() -> SQLModelSession:
    session = SQLModelSession(engine)
    try:
        yield session
    finally:
        session.close()
