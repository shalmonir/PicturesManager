import json

from src.DB.DBInterface import DBInterface
from src.Entities import UploadRequest, Picture, Album
from src.Entities.BaseEntity import BaseEntity
from src.Entities.User import User
from src.Entities.Engine import get_session


class LocalDB(DBInterface):
    def __init__(self):
        pass

    def store_album(self, album: Album):
        self.store(album)

    def store_picture(self, picture: Picture):
        self.store(picture)

    def store_user(self, user: User):
        self.store(user)

    def store_upload_request(self, upload_request: UploadRequest):
        self.store(upload_request)

    def store(self, entity: BaseEntity):
        session = get_session()
        session.add(entity)
        session.commit()

    def general_read(self, db_file: str):
        res = []
        with open(self.local_db_directory + db_file, "r") as db:
            lines = db.readlines()
            for line in lines:
                res.append(line)
        return res

    def read_albums(self):
        return self.general_read()

    def read_pictures(self):
        return self.general_read()

    def read_users(self):
        return self.general_read()

    def read_uploads(self):
        return self.general_read()


