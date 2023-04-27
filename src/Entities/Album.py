from sqlalchemy import Column, String, Integer, ForeignKey

from src.external import db
ALBUMS_TABLE_NAME = 'albums'


class Album(db.Model):
    __tablename__ = ALBUMS_TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, name: str, owner_id: int):
        self.name = name
        self.owner_id = owner_id
