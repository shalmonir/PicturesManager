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
    content = Column(String)

    def __init__(self,  status: str, time_stamp: str, album_id: int, content: str):
        self.status = status
        self.time_stamp = time_stamp
        self.album_id = album_id
        self.content = content
