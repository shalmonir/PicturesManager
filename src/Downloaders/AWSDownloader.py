from src.Configuration.Configuration import AWS_FILES_BUCKET, AWS_VIDEO_BUCKET
from src.Utils.AWSUtil import AWSUtil


class AWSDownloader:
    def __init__(self):
        pass

    @staticmethod
    def download(path):
        file = AWSUtil.get_file(path, AWS_FILES_BUCKET)
        file.seek(0)
        return file

    @staticmethod
    def video(path):
        file = AWSUtil.get_file(path, AWS_VIDEO_BUCKET)
        file.seek(0)
        return file
