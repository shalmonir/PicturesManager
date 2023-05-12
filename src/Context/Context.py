from datetime import datetime
from typing import List

from flask import current_app
from werkzeug.datastructures import FileStorage

from src.DB.DBInterface import DBInterface
from src.Entities.File import File
from src.Entities.Picture import Picture
from src.Entities.UploadRequest import UploadRequest
from src.Entities.User import User
from src.Report.ReporterInterface import ReporterInterface
from src.Uploaders.Constants import UPLOAD_STATUS_INIT, UPLOAD_STATUS_PRE_COMPLETED, UPLOAD_STATUS_UPLOADED, \
    UPLOAD_STATUS_COMPLETED
from src.Uploaders.UploaderInterface import UploaderInterface

ALBUM_FETCH_FAILED_ERROR = "Unable to create/retrieve album"


class Context:
    db_utility: DBInterface
    reporter: ReporterInterface
    uploader: UploaderInterface

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
        upload_request = self.create_upload_request(user_id=user.id)

        self.get_uploader().pre_upload(files)
        self.update_upload_request_pre_completed(upload_request)

        album = self.get_db_utility().fetch_album(album_name=album_name, user_id=user.id)
        if album is None:
            self.update_upload_request_failed(upload_request, ALBUM_FETCH_FAILED_ERROR)
            raise Exception(f"FAILED: {ALBUM_FETCH_FAILED_ERROR}")

        succeed, failed = self._upload(files, store_path=self.get_uploader().create_store_path(user, album), album_id=album.id)
        upload_request.status = UPLOAD_STATUS_UPLOADED
        self.get_db_utility().store(upload_request)

        self.update_upload_request_completed(upload_request, len(succeed), len(failed))
        return succeed, failed

    def _upload(self, files: List[FileStorage], store_path, album_id: int):
        files_upload_success = {}
        files_upload_fail = {}
        for pic in files:
            success, fail = self.get_uploader().upload_single_picture(file=pic, store_path=store_path)
            files_upload_success.update(success)
            files_upload_fail.update(fail)
            if len(success) == 1:
                file_result = next(iter((success.items())))
                file_name, file_path = file_result[0], file_result[1]
                self.db_utility.store(Picture(album_id, file_name, file_path))
        return files_upload_success, files_upload_fail

    def get_files_names(self, user_id: int):
        return self.get_uploader().get_files_names(user_id)

    def create_upload_request(self, user_id: int):
        return self.get_db_utility().store(
            UploadRequest(status=UPLOAD_STATUS_INIT, time_stamp=f"{datetime.now()}", user_id=user_id, content=f""))

    def update_upload_request_pre_completed(self, request: UploadRequest):
        request.status = UPLOAD_STATUS_PRE_COMPLETED
        self.get_db_utility().store(request)

    def update_upload_request_completed(self, request: UploadRequest, num_success, num_failed):
        request.status = UPLOAD_STATUS_COMPLETED
        request.content = f"success: {num_success}, fail: {num_failed}"
        self.get_db_utility().store(request)

    def upload_files(self, files, store_path: str, user_id: int):
        self.get_uploader().upload_files(files=files, store_path=store_path, user_id=user_id)

    def upload_files(self, files, store_path: str, user_id: int):
        files_upload_success = {}
        files_upload_fail = {}
        for file in files:
            success, fail = self.get_uploader().upload_single_file(file=file, store_path=store_path)
            if len(success) == 1:
                files_upload_success.update(success)
                file_result = next(iter((success.items())))
                file_name, file_path = file_result[0], file_result[1]
                self.db_utility.store(File(user_id=user_id, file_name=file_name, path=file_path))
            else:
                files_upload_fail.update(fail)
        return files_upload_success, files_upload_fail
