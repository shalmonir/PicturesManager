from sqlalchemy import Column, Integer, ForeignKey, String

from src.external import db

PICTURES_TABLE_NAME = 'pictures'


class Picture(db.Model):
    __tablename__ = PICTURES_TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey('albums.id'))
    file_name = Column(String)
    path = Column(String)
    data = Column(String)

    def __init__(self, album_id: int, file_name: str, path: str):
        self.album_id = album_id
        self.file_name = file_name
        self.path = path
        self.data = ''
