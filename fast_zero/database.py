from sqlalchemy import create_engine

from fast_zero.settings import Settings

engine =


def create_engine():
    with Session(engine) as session:
        return session
