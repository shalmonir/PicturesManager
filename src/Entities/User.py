from sqlalchemy import Column, Integer, Text, Sequence

from src.Entities.BaseEntity import BaseEntity

USERS_TABLE_NAME = 'users'


class User(BaseEntity):
    __tablename__ = USERS_TABLE_NAME
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(Text)

    def __init__(self, name: str):
        self.name = name
