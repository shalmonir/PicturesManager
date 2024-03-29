from werkzeug.datastructures import FileStorage

from src.Handlers.PictureLocalFileHandler import PictureLocalFileHandler
from src.Uploaders.CommunicationInterface import CommunicationInterface


class LocalCommunicator(CommunicationInterface):
    upload_handler = PictureLocalFileHandler()

    def pre_upload(self, files):
        if files is None:
            raise Exception('Empty upload')

    def upload_single_picture(self, file: FileStorage, store_path=None):
        if file is not None:
            try:
                picture_content = file.stream.read()
                store_path, _ = self.upload_handler.store(file.filename, picture_content)
                return {file.filename: store_path}, {}
            except Exception as e:
                return {}, {file.filename: str(e)}
        return {}, {'': 'File is None - Invalid input'}

    def get_files_names(self, prefix):
        return self.upload_handler.get_all_files(prefix=prefix)

    def create_store_path(self, user_name: str, album_name: str):
        return f"{user_name}/{album_name}"

    def upload_single_file(self, file, store_path):
        raise NotImplementedError

    def get_files_names(self, prefix):
        raise NotImplementedError
