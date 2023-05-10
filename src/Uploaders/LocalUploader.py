from werkzeug.datastructures import FileStorage

from src.Handlers.PictureLocalFileHandler import PictureLocalFileHandler
from src.Uploaders.UploaderInterface import UploaderInterface


class LocalUploader(UploaderInterface):
    upload_handler = PictureLocalFileHandler()

    def upload_single_picture(self, file: FileStorage, store_path=None):
        if file is not None:
            try:
                picture_content = file.stream.read()
                store_path, _ = self.upload_handler.store(file.filename, picture_content)
                return True, {file.filename: store_path}, {}
            except Exception as e:
                return False, {}, {file.filename: str(e)}
        return False, {}, {'': 'File is None - Invalid input'}

    def get_files_names(self, prefix):
        return self.upload_handler.get_all_files(prefix=prefix)
