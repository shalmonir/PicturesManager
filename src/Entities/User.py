from flask_login import UserMixin
from flask_sqlalchemy.model import Model

from sqlalchemy import Column, Integer, String
from src.external import db

USERS_TABLE_NAME = 'users'


class User(db.Model, UserMixin, Model):
    __tablename__ = USERS_TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    password = Column(String(130))
    email = Column(String(100), unique=True)

    def __init__(self, name: str, password_hash: str, email: str):
        self.name = name
        self.password = password_hash
        self.email = email
