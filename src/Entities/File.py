from sqlalchemy import Column, Integer, ForeignKey, String

from src.external import db

FILES_TABLE_NAME = 'files'


class File(db.Model):
    __tablename__ = FILES_TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_name = Column(String)
    path = Column(String)
    data = Column(String)

    def __init__(self, user_id: int, file_name: str, path: str, data=''):
        self.user_id = user_id
        self.file_name = file_name
        self.path = path
        self.data = data
