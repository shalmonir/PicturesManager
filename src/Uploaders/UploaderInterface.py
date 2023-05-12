from werkzeug.datastructures import FileStorage

from src.Entities import Album, User


class UploaderInterface:

    def upload_single_picture(self, file: FileStorage, store_path=None):
        pass

    def pre_upload(self, files):
        pass

    def upload(self, files: list[FileStorage]):
        pass

    def create_store_path(self, user: User, album: Album):
        pass

    def upload_single_file(self, file, store_path):
        pass
