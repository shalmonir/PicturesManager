from typing import List, Dict
from werkzeug.datastructures import FileStorage

from src.Handlers.PictureLocalFileHandler import PictureLocalFileHandler
from src.Uploaders.UploaderInterface import UploaderInterface


class LocalUploader(UploaderInterface):
    upload_handler = PictureLocalFileHandler()

    def upload(self, files: List[FileStorage], album: str) -> tuple[List[str], Dict[str, Exception]]:
        succeed = []
        failed = {}
        if files is not None:
            for file in files:
                try:
                    picture_content = file.stream.read()
                    _, bytes_written = self.upload_handler.store(file.filename, picture_content)
                    succeed.append(file.filename)
                except Exception as e:
                    failed[file.filename] = str(e)
        return succeed, failed
