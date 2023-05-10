from werkzeug.datastructures import FileStorage
from abc import ABC


class UploaderInterface(ABC):
    def upload_single_picture(self, file: FileStorage, store_path=None):
        pass
