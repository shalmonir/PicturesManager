import logging
import os

from flask import Flask, request, render_template, Request
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy

from src.Configuration.Configuration import PATH_TO_LOCAL_STORAGE, LEGAL_PICTURE_SUFFIX
from src.Configuration.Local import DB_SECRET
from src.Context.LocalContextMgr import LocalContextMgr
from src.Entities.UploadRequest import UploadRequest

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_SECRET
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

profile = 'local'
context = LocalContextMgr()


@app.route('/')
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return render_template('home_page.html', msg='Logged in :)')
    return render_template("login.html")


def process_upload_request(user_request: Request) -> UploadRequest:
    try:
        return {'files': user_request.files.getlist("file"), 'album_name': user_request.form['album_name']}
    except Exception as e:
        logging.ERROR('input error: ' + str(e))


@app.route("/upload", methods=['POST'])
def upload():
    request_internal = process_upload_request(request)
    files_uploaded, files_failed_upload = context.get_uploader().upload(request_internal['files'], request_internal['album_name'])
    context.get_reporter().report(files_uploaded, files_failed_upload)
    return render_template("upload_summary.html",
                           album=f"{request_internal['album_name']}",
                           successfully=f"{', '.join([str(file) + ': ' + str(upload_path)  for file, upload_path in files_uploaded.items()])}",
                           failed=f"{', '.join([str(file) + '(' + reason + '), ' for file, reason in files_failed_upload.items()])}")


@app.route("/show", methods=['POST', 'GET'])
def show():
    album_name = 'todo: put album name here (user select from list)'
    display_pictures = [pic for pic in
                        [PATH_TO_LOCAL_STORAGE + '\\' + pic for pic in
                         tuple(
                             filter(lambda f: os.path.isfile(PATH_TO_LOCAL_STORAGE + '\\' + f), os.listdir(PATH_TO_LOCAL_STORAGE)))]
                        if pic.endswith(tuple(LEGAL_PICTURE_SUFFIX))]
    return render_template("gallery.html", pictures=display_pictures, album_name=album_name)


@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    directory, filename = os.path.split(filepath)
    return send_from_directory(directory, filename, as_attachment=False)
    # TODO: find a way to extend this behavior for this is only ment to be used in 'local' strategy

