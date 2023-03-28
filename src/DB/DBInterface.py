from src.Entities import User, Album, Picture, UploadRequest
from abc import ABC, abstractmethod


class DBInterface(ABC):
    @abstractmethod
    def store_album(self, album: Album):
        pass

    @abstractmethod
    def store_picture(self, picture: Picture):
        pass

    @abstractmethod
    def store_user(self, user: User):
        pass

    @abstractmethod
    def store_upload_request(self, upload_request: UploadRequest):
        pass
