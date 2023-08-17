from flask import Blueprint, render_template, request
from flask_login import login_required

from src.Context.AWSContext import AWSContext
from src.Handlers.ImageProcessRequest import ImageProcessRequest
from src.Utils.RequestProcessor import RequestProcessor

image_processing = Blueprint('analyze', import_name=__name__)
context = AWSContext()


@image_processing.route('/face_recognition', methods=['GET'])
@login_required
def dashboard():

    # TODO: get file on-the-fly and send it to image processing service, show the result
    return render_template("home.html")


@image_processing.route('/face_recognition/detect_faces', methods=['POST'])
@login_required
def detect_faces():
    face_recognition_request = RequestProcessor.process_detect_faces_request(request)
    ImageProcessRequest.send_request(face_recognition_request)
    pass