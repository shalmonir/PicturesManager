from typing import List, Dict
from werkzeug.datastructures import FileStorage

from src.Handlers.PictureLocalFileHandler import PictureLocalFileHandler
from src.Uploaders.UploaderInterface import UploaderInterface


class LocalUploader(UploaderInterface):
    upload_handler = PictureLocalFileHandler()

    def upload(self, files: List[FileStorage], album: str):
        succeed = {}
        failed = {}
        if files is not None:
            for file in files:
                try:
                    picture_content = file.stream.read()
                    store_path, bytes_written = self.upload_handler.store(file.filename, picture_content)
                    succeed[file.filename] = store_path
                except Exception as e:
                    failed[file.filename] = str(e)
        return succeed, failed
