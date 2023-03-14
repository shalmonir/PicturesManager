from src.Entities.BaseEntity import BaseEntity


class User(BaseEntity):
    def __init__(self, name: str):
        self.name = name
