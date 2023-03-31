from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.Configuration.Local import DB_SECRET
from src.Entities.BaseEntity import BaseEntity


def create():
    engine = create_engine(DB_SECRET)
    db_session = scoped_session(sessionmaker())
    db_session.configure(bind=engine)
    BaseEntity.metadata.create_all(engine)
