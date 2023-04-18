from typing import List, Dict
from werkzeug.datastructures import FileStorage
from abc import ABC


class UploaderInterface(ABC):
    def upload(self, files: List[FileStorage], album: str):
        pass
