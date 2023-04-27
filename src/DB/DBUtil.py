import uuid
from typing import List

from flask_sqlalchemy import SQLAlchemy

from src.DB.DBInterface import DBInterface
from src.Entities.Album import Album
from src.Entities.Picture import Picture
from src.Entities.User import User


class DBUtil(DBInterface):
    def get_db(self) -> SQLAlchemy:
        from src import DBConnectionMgr
        return DBConnectionMgr().get_connection()

    def get_user(self, user_id: int):
        return self.get_db().session.query(User).filter_by(id=user_id).scalar()

    def get_album(self, album_id: int):
        return self.get_db().session.query(Album).filter_by(id=album_id).scalar()

    def get_user_by_name(self, username: str):
        return self.get_db().session.query(User).filter(User.name == username).first()

    def get_user_albums(self, user_id: int):
        return self.get_db().session.query(Album).filter(Album.owner_id == user_id).all()

    def search_user_albums(self, user_id: int, keyword: str) -> List[Album]:
        res = []
        for album in self.get_user_albums(user_id=user_id):
            if keyword in album.name:
                res.append(album)
        return res

    def get_album_pictures(self, album_id: int):
        return self.get_db().session.query(Picture).filter(Picture.album_id == album_id).all()

    def store(self, entity):
        self.get_db().session.add(entity)
        self.get_db().session.commit()
        return entity