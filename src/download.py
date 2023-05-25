import io
import os

import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, send_from_directory, current_app, send_file
from flask_login import login_required

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
        s3_client = AWSUtil.create_aws_s3_client()
        file = io.BytesIO()
        S3_BUCKET = 'nirpicturestest'
        metadata = s3_client.head_object(Bucket=S3_BUCKET, Key=filepath)
        conf = boto3.s3.transfer.TransferConfig(use_threads=False)
        s3_client.download_fileobj(S3_BUCKET, filepath, file)
        current_app.logger.debug(f"retrieving filepath: {filepath}")
        file.seek(0)
        return send_file(file, mimetype=metadata['ContentType'])
    except ClientError:
        return ERROR_RESPONSE
    except Exception:
        return ERROR_RESPONSE
