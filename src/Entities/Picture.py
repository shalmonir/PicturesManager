from sqlalchemy import Column, Integer, ForeignKey, String

from src.Entities.BaseEntity import BaseEntity
from . import Album
from . import UploadRequest

PICTURES_TABLE_NAME = 'pictures'


class Picture(BaseEntity):
    __tablename__ = PICTURES_TABLE_NAME
    id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey('albums.id'))
    file_name = Column(String)
    picture_hash = Column(String)
    local_path = Column(String)
    upload_id = Column(Integer, ForeignKey('uploads.id'))

    def __init__(self, album_id: int, file_name: str, picture_hash: str, local_path: str, upload_id: int):
        self.album_id = album_id
        self.file_name = file_name
        self.picture_hash = picture_hash
        self.local_path = local_path
        self.upload_id = upload_id
