from werkzeug.datastructures import FileStorage


class UploaderInterface:

    def upload_single_picture(self, file: FileStorage, store_path=None):
        pass

    def pre_upload(self, files):
        pass

    def create_store_path(self, user_name: str, album: str):
        pass

    def upload_single_file(self, file, store_path):
        pass

    def get_files_names(self, prefix):
        pass
