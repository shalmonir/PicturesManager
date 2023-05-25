import io

import boto3

from src.Configuration.Configuration import AWS_FILES_BUCKET
from src.Utils.AWSUtil import AWSUtil


class AWSDownloader:
    @staticmethod
    def download(self, path):
        s3 = AWSUtil.create_aws_s3_client()
        file = io.BytesIO()
        metadata = s3.head_object(Bucket=AWS_FILES_BUCKET, Key=path)
        conf = boto3.s3.transfer.TransferConfig(use_threads=False)
        s3.download_fileobj(AWS_FILES_BUCKET, path, file)
        file.seek(0)
        return file, metadata
