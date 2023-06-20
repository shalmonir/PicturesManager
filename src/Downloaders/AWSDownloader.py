from src.Configuration.Configuration import AWS_FILES_BUCKET, AWS_VIDEO_BUCKET
from src.Utils.AWSUtil import AWSUtil


class AWSDownloader:
    def __init__(self):
        pass

    @staticmethod
    def download(path):
        return AWSDownloader.AWS_fetch(path, AWS_FILES_BUCKET)

    @staticmethod
    def video(path):
        return AWSDownloader.AWS_fetch(path, AWS_VIDEO_BUCKET)

    @staticmethod
    def AWS_fetch(path, bucket):
        file = AWSUtil.get_file(path, bucket)
        file.seek(0)
        return file
