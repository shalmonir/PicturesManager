from typing import List, Dict

from werkzeug.datastructures import FileStorage

from PictureLocalFileHandler import PictureLocalFileHandler


class Uploader(object):
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            cls.upload_handler = PictureLocalFileHandler()  # inject with respect to environment
        return cls._instance

    def upload(self, files: List[FileStorage]) -> tuple[List[str], Dict[str, Exception]]:
        succeed = []
        failed = {}
        for file in files:
            try:
                self.upload_handler.store(file.filename, file.stream.read())
                succeed.append(file.filename)
            except Exception as e:
                failed[file.filename] = str(e)

        return succeed, failed
