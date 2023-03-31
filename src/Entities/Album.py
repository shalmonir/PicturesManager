from sqlalchemy import Column, String, Integer, ForeignKey

from src.Entities.BaseEntity import BaseEntity

ALBUMS_TABLE_NAME = 'albums'


class Album(BaseEntity):
    __tablename__ = ALBUMS_TABLE_NAME
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, name: str, user_id):
        self.name = name
        self.owner_id = user_id
