from src.Entities.BaseEntity import BaseEntity


class Album(BaseEntity):
    def __init__(self, album_id, name: str, user_id):
        self.album_id = album_id
        self.name = name
        self.owner_id = user_id
