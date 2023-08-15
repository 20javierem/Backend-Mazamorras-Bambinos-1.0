from contextlib import contextmanager

from sqlmodel import Session as SQLModelSession, create_engine

<<<<<<< HEAD
engine = create_engine('mysql+pymysql://root:Ernestomoreno1@localhost:3306/dbbambinos', echo=False)
=======
engine = create_engine('mysql+pymysql://root@localhost:3306/dbbambinos1', echo=False)
>>>>>>> 7945d381b3570241468b98c54ca3b0840c8e7b6d


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
