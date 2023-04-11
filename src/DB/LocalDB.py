import json

from sqlalchemy.orm import scoped_session

from src.DB.DBInterface import DBInterface
from src.Entities import UploadRequest, Picture, Album
from src.Entities.BaseEntity import BaseEntity
from src.Entities.User import User
from src.Entities.Engine import get_session


class LocalDB(DBInterface):
    db_session: scoped_session

    def __init__(self):
        self.db_session = None

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def get_db_session(self):
        if not self.db_session or not self.db_session.is_active:
            self.db_session = get_session()
        return self.db_session

    def store_album(self, album: Album):
        self.store(album)

    def store_picture(self, picture: Picture):
        self.store(picture)

    def store_user(self, user: User):
        self.store(user)

    def store_upload_request(self, upload_request: UploadRequest):
        self.store(upload_request)

    def store(self, entity: BaseEntity):
        self.db_session.add(entity)
        self.db_session.commit()

    def get_album_by_id(self, _id: int):
        return self.db_session.query(Album).filter_by(id=_id)

    def read_albums(self):
        return self.db_session.query(Album).all()

    def read_users(self):
        return self.db_session.query(User).all()
