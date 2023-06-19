import io
import os

import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, send_from_directory, current_app, send_file
from flask_login import login_required

from src.Configuration.Configuration import AWS_VIDEO_BUCKET, AWS_FILES_BUCKET
from src.Utils.AWSUtil import AWSUtil

ERROR_RESPONSE = 'fail'

download = Blueprint('download', import_name=__name__)


@download.route('/cdn/<path:filepath>')
@login_required
def cdn(filepath):
    directory, filename = os.path.split(filepath)
    current_app.logger.debug(f"dir: {directory}, filename: {filename}, filepath: {filepath}")
    if os.name != 'nt':
        directory = f"/{str(directory)}"
    return send_from_directory(directory, filename, as_attachment=False)


@download.route('/aws/<path:filepath>')
@login_required
def aws_download(filepath):
    try:
        file, metadata = get_file_from_s3(filepath, AWS_FILES_BUCKET)
        file.seek(0)
        return send_file(file, mimetype=metadata)
    except ClientError as client_error:
        current_app.logger.error(f"retrieving filepath: {filepath}, error type 'ClientError', details: {client_error}")
        return ERROR_RESPONSE
    except Exception as e:
        current_app.logger.error(f"retrieving filepath: {filepath}, details: {e}")
        return ERROR_RESPONSE


@download.route('/aws/video/<path:filepath>')
def aws_video(filepath):
    try:
        file, metadata = get_file_from_s3(filepath, AWS_VIDEO_BUCKET)
        file.seek(0)
        return send_file(file, mimetype=metadata)
    except ClientError as client_error:
        current_app.logger.error(f"retrieving filepath: {filepath}, error type 'ClientError', details: {client_error}")
        return ERROR_RESPONSE
    except Exception as e:
        current_app.logger.error(f"retrieving filepath: {filepath}, details: {e}")
        return ERROR_RESPONSE


def get_file_from_s3(file_path: str, bucket: str):
    s3_client = AWSUtil.create_aws_s3_client()
    file_stream = io.BytesIO()
    metadata = s3_client.head_object(Bucket=bucket, Key=file_path)
    s3_client.download_fileobj(bucket, file_path, file_stream)
    return file_stream, metadata['ContentType']
