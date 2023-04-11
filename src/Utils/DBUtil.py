from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src import DB_SECRET
from src.Entities.Album import Album
from src.Entities.Picture import Picture
from src.Entities.User import User


class DBUtil:
    db: SQLAlchemy

    def __init__(self):
        engine = create_engine(DB_SECRET)
        db_session = scoped_session(sessionmaker())
        db_session.configure(bind=engine)
        self.db = db_session

    def set_db(self, db):
        self.db = db

    def get_user_by_id(self, user_id: int):
        user = self.db.execute(self.db.query(User).filter_by(id=user_id)).scalar()
        if user:
            return user
        raise Exception('non exist user')

    def get_user_by_name(self, username: str):
        user = self.db.execute(self.db.query(User).filter_by(name=username)).scalar()
        if user:
            return user
        raise Exception('non exist user')

    def get_user_albums(self, user_id: int):
        albums = self.db.execute(self.db.query(Album).filter_by(owner_id=user_id)).scalars()
        if albums:
            return albums.all()
        raise Exception('non exist user')

    def get_album_pictures(self, album_id: int):
        pictures = self.db.execute(self.db.query(Picture).filter_by(album_id=album_id)).scalars()
        if pictures:
            return pictures.all()
        raise Exception('Album can not be fetched')
