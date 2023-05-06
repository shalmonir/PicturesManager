import logging
from typing import List

from flask_sqlalchemy import SQLAlchemy

from src.Configuration.Configuration import PICTURES_IN_PAGE
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

    def match_user_albums(self, user_id: int, match_name: str) -> List[Album]:
        return self.get_db().session.query(Album).filter(Album.owner_id == user_id).filter(Album.name == match_name).all()

    def get_album_pictures(self, album_id: int):
        return self.get_db().session.query(Picture).filter(Picture.album_id == album_id).all()

    def store(self, entity):
        self.get_db().session.add(entity)
        self.get_db().session.commit()
        return entity

    def get_else_create_album(self, album_name: str, user_id: int):
        album_query = self.match_user_albums(user_id=user_id, match_name=album_name)
        if len(album_query) == 0:
            return self.store(Album(name=album_name, owner_id=user_id))
        else:
            return album_query[0]

    def get_album_pictures_page(self, album_id: int, page: int):
        pictures = self.get_album_pictures(album_id=album_id)
        divided = [pictures[i:i + PICTURES_IN_PAGE] for i in range(0, len(pictures), PICTURES_IN_PAGE)]
        if page >= len(divided):
            logging.ERROR(f"required page is out of bounds for given album. album id: {album_id}, page: {page}")
            page = 0
        return divided[page]

    def get_album_pictures_pages_amount(self, album_id: int):
        pictures_amount = len(self.get_album_pictures(album_id=album_id))
        return int(pictures_amount / PICTURES_IN_PAGE) + (pictures_amount % PICTURES_IN_PAGE > 0)
