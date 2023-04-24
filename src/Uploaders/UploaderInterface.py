from typing import List
from werkzeug.datastructures import FileStorage
from abc import ABC


class UploaderInterface(ABC):
    def upload(self, files: List[FileStorage]):
        pass

    def upload_single_picture(self, file: FileStorage):
        pass
