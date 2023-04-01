import logging
from src.Configuration.Configuration import PATH_TO_LOCAL_STORAGE, SEPERATOR


class ReadLocalFileException(Exception):
    def __init__(self):
        message = 'error reading file'
        super().__init__(message)


class WriteLocalFileException(Exception):
    def __init__(self):
        super().__init__('error reading file')


class PictureLocalFileHandler:
    def store(self, picture_file_name, picture_content):
        try:
            destination_path = PATH_TO_LOCAL_STORAGE + SEPERATOR + picture_file_name
            with open(destination_path, "wb") as pic:
                payload_bytes = pic.write(picture_content)
                return destination_path, payload_bytes
        except Exception as exception:
            logging.error("Failed reading file, Error details: " + exception.__str__())
            raise WriteLocalFileException()

    def read(self, picture_file_path: str):
        try:
            with open(PATH_TO_LOCAL_STORAGE + SEPERATOR + picture_file_path, "rb") as pic:
                return pic.read()
        except Exception:
            logging.error("Failed reading file: " + picture_file_path)
            raise ReadLocalFileException()
