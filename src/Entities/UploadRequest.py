from sqlalchemy import Column, Integer, ForeignKey, String
from src.Entities.BaseEntity import BaseEntity
from . import Album
UPLOADS_TABLE_NAME = 'uploads'


class UploadRequest(BaseEntity):
    __tablename__ = UPLOADS_TABLE_NAME
    id = Column(Integer, primary_key=True)
    status = Column(String)
    time_stamp = Column(String)
    album_id = Column(Integer, ForeignKey('albums.id'))

    def __init__(self, album_id: int, status: str, time_stamp):
        self.album_id = album_id
        self.status = status
        self.time_stamp = time_stamp
