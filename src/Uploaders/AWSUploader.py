from werkzeug.datastructures import FileStorage

from src.Configuration.Configuration import AWS_FILES_BUCKET, AWS_FILES_LIMIT
from src.Uploaders.UploaderInterface import UploaderInterface
from src.Utils.AWSUtil import AWSUtil

INVALID_INPUT_RESPONSE = {'': 'File is None - Invalid input'}


class AWSUploader(UploaderInterface):
    def upload_single_picture(self, file: FileStorage, store_path=None):
        if file is not None:
            try:
                aws_path = f"{store_path}/{file.filename}"
                self.store(file, aws_path)
                return {file.filename: aws_path}, {}
            except Exception as e:
                return {}, {file.filename: str(e)}
        return {}, INVALID_INPUT_RESPONSE

    def upload_single_file(self, file, store_path):
        if file is not None:
            try:
                aws_path = f"{store_path}/{file.filename}"
                self.store(file, aws_path)
                return {file.filename: aws_path}, {}
            except Exception as e:
                return {}, {file.filename: str(e)}
        return {}, INVALID_INPUT_RESPONSE

    def get_files_names(self, prefix):
        s3 = AWSUtil.create_aws_s3_resource()
        my_bucket = s3.Bucket(AWS_FILES_BUCKET)
        res = []
        for objects in my_bucket.objects.filter(Prefix=prefix):
            res.append(objects.key)
        return res

    def pre_upload(self, files):
        if len(files) > AWS_FILES_LIMIT:
            raise Exception('upload files limit exceed')

    def store(self, file, store_path: str):
        AWSUtil.create_aws_s3_client().upload_fileobj(file, AWS_FILES_BUCKET, store_path)
