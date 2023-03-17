from src.Entities.BaseEntity import BaseEntity


class User(BaseEntity):
    def __init__(self, name: str, user_id):
        self.id = user_id
        self.name = name
