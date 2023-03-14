from src.Entities.BaseEntity import BaseEntity


class UploadRequest(BaseEntity):
    def __init__(self, album_name: str, status: str, date):
        self.album_name = album_name
        self.status = status
        self.date = date
