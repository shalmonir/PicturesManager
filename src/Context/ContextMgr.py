import hashlib
from datetime import datetime
from typing import List

from flask import current_app
from werkzeug.datastructures import FileStorage

from src.DB.DBInterface import DBInterface
from src.DB.DBUtil import DBUtil
from src.Entities.Album import Album
from src.Entities.Picture import Picture
from src.Entities.UploadRequest import UploadRequest
from src.Entities.User import User
from src.Report.ReporterInterface import ReporterInterface


class Context:
    db_utility: DBInterface
    reporter: ReporterInterface

    def __init__(self):
        self.db_utility = None
        self.reporter = None

    def get_db_utility(self) -> DBInterface:
        return self.db_utility

    def get_reporter(self) -> ReporterInterface:
        return self.reporter

    def upload(self, files: List[FileStorage], album_name: str, user: User):
        upload_request = None
        try:
            try:
                status = 'Init'
                current_app.logger.debug(f"album: {album_name}, files amount: {len(files)}")
                album_query = DBUtil().search_user_albums(user_id=user.id, keyword=album_name)
                if len(album_query) == 0:
                    album = DBUtil().store(Album(name=album_name, owner_id=user.id))
                else:
                    album = album_query[0]
                upload_request = DBUtil().store(UploadRequest(status=status, time_stamp=f"{datetime.now()}", album_id=album.id, content=f"album: {album.name}"))

                files_upload_success, files_upload_fail = self.upload_pictures(album, files)

                upload_request.status = 'Pictures Upload Action Done'
                upload_request.content = f"#success: {len(files_upload_success)}, #failed: {len(files_upload_fail)}"
                DBUtil().store(upload_request)
                return files_upload_success, files_upload_fail

            except Exception as upload_exception:
                current_app.logger.error(str(upload_exception))
                if upload_request is not None:
                    upload_request.status = 'FAIL'
                    upload_request.content = f"Error details: {str(upload_exception)}"
                    DBUtil().store(upload_request)
        except Exception as e:
            current_app.logger.error(str(e))

    def upload_pictures(self, album, files):
        files_upload_success = {}
        files_upload_fail = {}
        for pic in files:
            result, success, fail = self.uploader.upload_single_picture(file=pic)
            if result:
                files_upload_success.update(success)
                file_result = next(iter((success.items())))
                file_name = file_result[0]
                file_path = file_result[1]
                self.db_utility.store(
                    Picture(album.id, file_name, hashlib.sha1(file_name.encode()).hexdigest(), file_path, 1))
            else:
                files_upload_fail.update(fail)
        current_app.logger.debug(f"failed: {str(files_upload_fail)}, success: {str(files_upload_success)}")
        return files_upload_success, files_upload_fail
