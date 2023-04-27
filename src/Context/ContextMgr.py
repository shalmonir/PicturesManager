import hashlib
from datetime import datetime
from typing import List

from flask import current_app
from werkzeug.datastructures import FileStorage

from src.DB.DBInterface import DBInterface
from src.Entities.Album import Album
from src.Entities.Picture import Picture
from src.Entities.UploadRequest import UploadRequest
from src.Entities.User import User
from src.Report.ReporterInterface import ReporterInterface
from src.Uploaders.UploaderInterface import UploaderInterface


class Context:
    db_utility: DBInterface
    reporter: ReporterInterface

    def __init__(self):
        self.uploader = None
        self.db_utility = None
        self.reporter = None

    def get_uploader(self) -> UploaderInterface:
        return self.uploader

    def get_db_utility(self) -> DBInterface:
        return self.db_utility

    def get_reporter(self) -> ReporterInterface:
        return self.reporter

    def upload(self, files: List[FileStorage], album_name: str, user: User):
        upload_request = None
        files_upload_success = {}
        files_upload_fail = {}
        status = 'Init'
        try:
            try:
                current_app.logger.debug(f"album: {album_name}, files amount: {len(files)}")
                album = self.get_db_utility().get_else_create_album(album_name=album_name, user_id=user.id)
                status = 'Album entity present'
                upload_request = self.get_db_utility().store(UploadRequest(status=status, time_stamp=f"{datetime.now()}", album_id=album.id, content=f"album: {album.name}"))

                files_upload_success, files_upload_fail = self.upload_pictures(album, files)
                upload_request.status = 'Pictures Upload Action Done'
                upload_request.content = f"#success: {len(files_upload_success)}, #failed: {len(files_upload_fail)}"
                self.get_db_utility().store(upload_request)
                return files_upload_success, files_upload_fail

            except Exception as upload_exception:
                current_app.logger.error(str(upload_exception))
                if upload_request is not None:
                    upload_request.status = status
                    upload_request.content = f"Error details: {str(upload_exception)}"
                    self.get_db_utility().store(upload_request)
                    return files_upload_success, files_upload_fail
        except Exception as e:
            current_app.logger.error(str(e))
            return files_upload_success, files_upload_fail

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
