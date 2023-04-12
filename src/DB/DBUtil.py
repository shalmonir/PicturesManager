from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src import DB_SECRET
from src.DB.DBInterface import DBInterface
from src.Entities import UploadRequest
from src.Entities.Album import Album
from src.Entities.Picture import Picture
from src.Entities.User import User


class DBUtil(DBInterface):
    db: SQLAlchemy

    def __init__(self):
        engine = create_engine(DB_SECRET)
        db_session = scoped_session(sessionmaker())
        db_session.configure(bind=engine)
        self.db = db_session

    def get_user(self, user_id: int):
        return self.db.execute(self.db.query(User).filter_by(id=user_id)).scalar()

    def get_album(self, album_id: int):
        return self.db.execute(self.db.query(Album).filter_by(id=album_id)).scalar()

    def get_user_by_name(self, username: str):
        return self.db.execute(self.db.query(User).filter_by(name=username)).scalar()

    def get_user_albums(self, user_id: int):
        return self.db.execute(self.db.query(Album).filter_by(owner_id=user_id)).scalars()

    def get_album_pictures(self, album_id: int):
        return self.db.execute(self.db.query(Picture).filter_by(album_id=album_id)).scalars().all()

    def store_picture(self, picture: Picture):
        pass

    def store_user(self, user: User):
        pass

    def store_upload_request(self, upload_request: UploadRequest):
        pass

    def store_album(self, album: Album):
        pass
