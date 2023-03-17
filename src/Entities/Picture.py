from src.Entities.BaseEntity import BaseEntity


class Picture(BaseEntity):
    def __init__(self, picture_id, album_id, file_name: str, picture_hash: str, local_path: str, upload_id: str):
        self.picture_id = picture_id
        self.album_id = album_id
        self.file_name = file_name
        self.picture_hash = picture_hash
        self.local_path = local_path
        self.upload_id = upload_id
