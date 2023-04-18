import json

from src.Configuration.Configuration import PATH_TO_LOCAL_DB_DIRECTORY
from src.DB.DBInterface import DBInterface
from src.Entities import UploadRequest, Picture, Album
from src.Entities.User import User

UPLOAD_STR = "upload"
USER_STR = "user"
PICTURE_STR = "picture"
ALBUM_STR = "album"


class LocalFileDB(DBInterface):  #  TODO: Fix test cases -> remove this
    def __init__(self):
        self.local_db_directory = PATH_TO_LOCAL_DB_DIRECTORY
        self.init_indexes()

    def init_indexes(self):
        pass

    def store_album(self, album: Album):
        with open(self.local_db_directory + ALBUM_STR, "a+") as db:
            db.write(json.dumps({"id": album.album_id, "name": album.name, "owner_id": album.owner_id}) + "\n")

    def store_picture(self, picture: Picture):
        with open(self.local_db_directory + PICTURE_STR, "a+") as db:
            db.write(json.dumps({"id": picture.picture_id, "album_id": picture.album_id,
                                                  "hash": picture.picture_hash, "file_name": picture.file_name,
                                                  "upload_id": picture.upload_id, "local_path": picture.local_path}) + "\n")

    def store_user(self, user: User):
        with open(self.local_db_directory + USER_STR, "a+") as db:
            db.write(json.dumps({"id": user.id, "name": user.name}) + "\n")

    def store_upload_request(self, upload_request: UploadRequest):
        with open(self.local_db_directory + UPLOAD_STR, "a+") as db:
            db.write(json.dumps({"id": upload_request.id, "album_id": upload_request.album_id,
                                                         "status": upload_request.status,
                                                         "time_stamp": upload_request.time_stamp}) + "\n")

    def general_read(self, db_file: str):
        res = []
        with open(self.local_db_directory + db_file, "r") as db:
            lines = db.readlines()
            for line in lines:
                res.append(line)
        return res

    def read_albums(self):
        return self.general_read(ALBUM_STR)

    def read_pictures(self):
        return self.general_read(PICTURE_STR)

    def read_users(self):
        return self.general_read(USER_STR)

    def read_uploads(self):
        return self.general_read(UPLOAD_STR)


