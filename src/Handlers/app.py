import hashlib
import logging
import os

from flask import Flask, request, render_template, Request
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy

from src.Configuration.Configuration import PATH_TO_LOCAL_STORAGE, LEGAL_PICTURE_SUFFIX, ALLOWED_EMAIL_REGISTRATION
from src.Configuration.Local import DB_SECRET
from src.Context.LocalContextMgr import LocalContextMgr
from src.Entities.UploadRequest import UploadRequest
from src.Entities.User import User

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
        return render_template('home.html')
    return render_template("login.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        register_request = process_register_request(request)
        email = register_request['email']
        if email not in ALLOWED_EMAIL_REGISTRATION:
            render_template("error.html", error_msg=f"Failed register. Please contact administrator for permissions")
        context.get_db_utility().store_user(User(name=register_request['name'], password_hash=hashlib.sha3_512(str(register_request['password']).encode()).hexdigest(), email=email))
        return render_template("login.html")
    return render_template("register.html")


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        request_internal = process_upload_request(request)
        files_uploaded, files_failed_upload = context.get_uploader().upload(request_internal['files'], request_internal['album_name'])
        context.get_reporter().report(files_uploaded, files_failed_upload)
        return render_template("upload_summary.html",
                               album=f"{request_internal['album_name']}",
                               successfully=f"{', '.join([str(file) + ': ' + str(upload_path)  for file, upload_path in files_uploaded.items()])}",
                               failed=f"{', '.join([str(file) + '(' + reason + '), ' for file, reason in files_failed_upload.items()])}")
    return render_template('upload.html')


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


def process_register_request(register_request: Request) -> UploadRequest:
    try:
        return {'password': register_request.form["password"], 'email': register_request.form['email'], 'name': register_request.form['name']}
    except Exception as e:
        logging.ERROR('register input error: ' + str(e))
        return render_template("error.html", error_msg=f'register failure')


def process_upload_request(user_request: Request) -> UploadRequest:
    try:
        return {'files': user_request.files.getlist("file"), 'album_name': user_request.form['album_name']}
    except Exception as e:
        logging.ERROR('upload input error: ' + str(e))


def process_login_request(login_request: Request):
    try:
        return {'password': login_request.form["password"], 'username': login_request.form['username']}
    except Exception as e:
        logging.ERROR('login input error: ' + str(e))
        return render_template("error.html", error_msg=f'login failure')
