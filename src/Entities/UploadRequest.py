from src.Entities.BaseEntity import BaseEntity


class UploadRequest(BaseEntity):
    def __init__(self, upload_id, album_id: int, status: str, time_stamp):
        self.id = upload_id
        self.album_id = album_id
        self.status = status
        self.time_stamp = time_stamp
