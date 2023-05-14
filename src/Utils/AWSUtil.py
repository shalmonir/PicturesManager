import boto3

from src.Configuration.Configuration import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_NAME


class AWSUtil:
    @staticmethod
    def create_aws_s3_client():
        client = boto3.client(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            service_name=AWS_S3_NAME)
        return client

    @staticmethod
    def create_aws_s3_resource():
        s3_resource = boto3.resource(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            service_name=AWS_S3_NAME)
        return s3_resource
