import flask_login
from flask import Blueprint, render_template, request

from src.Configuration.Configuration import SEPERATOR
from src.Context.AWSContext import AWSContext
from src.Utils.RequestProcessor import RequestProcessor, REQUEST_UPLOAD_NAME, REQUEST_UPLOAD_FILES

aws = Blueprint('aws', import_name=__name__)

profile = 'local'
context = AWSContext()


@aws.route("/aws/get", methods=['POST', 'GET'])
def get():
    user = flask_login.current_user
    return render_template("aws_get_page.html", str_printable=f"Files:", files=context.get_files_names(user.name))


@aws.route("/aws/get/<sub_directory>", methods=['POST', 'GET'])
def get_directory(sub_directory):
    user = flask_login.current_user
    if request.method == 'POST' or sub_directory:
        return render_template("aws_get_page.html", str_printable=f"Files:", files=context.get_files_names(user.name + SEPERATOR + sub_directory))
    return render_template("aws_get_page.html", str_printable=f"Files:", files=context.get_files_names(user.name))


@aws.route("/aws/store", methods=['POST', 'GET'])
def store():
    if request.method == 'POST':
        user = flask_login.current_user
        request_internal = RequestProcessor.process_upload_request(request)
        files_uploaded, files_failed_upload = context.upload_files(request_internal[REQUEST_UPLOAD_FILES], f"{user.name}/{request_internal[REQUEST_UPLOAD_NAME]}", user.id)
        return render_template("upload_summary.html",
                               upload_name=f"{request_internal[REQUEST_UPLOAD_NAME]}",
                               successfully=f"{', '.join([str(file) + ': ' + str(upload_path) for file, upload_path in files_uploaded.items()])}",
                               failed=f"{', '.join([str(file) + '(' + reason + '), ' for file, reason in files_failed_upload.items()])}")
    return render_template("aws_store.html", str_printable=f"create user context show-able files")


