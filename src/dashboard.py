from string import Template

import flask_login
from flask import Blueprint, render_template, request, session
from flask_login import login_required

from src.Configuration.Configuration import VIDEO_PARTS
from src.Context.AWSContext import AWSContext
from src.Utils.RequestProcessor import RequestProcessor, REQUEST_UPLOAD_NAME, REQUEST_UPLOAD_FILES


dash = Blueprint('dashboard', import_name=__name__)
context = AWSContext()


@dash.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("home.html")


@dash.route("/upload", methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        request_internal = RequestProcessor.process_upload_request(request)
        files_uploaded, files_failed_upload = \
            context.upload(request_internal[REQUEST_UPLOAD_FILES], request_internal[REQUEST_UPLOAD_NAME], flask_login.current_user)
        return render_template("upload_summary.html",
                               upload_name=f"{request_internal[REQUEST_UPLOAD_NAME]}",
                               successfully=f"{', '.join([str(file) + ': ' + str(upload_path)  for file, upload_path in files_uploaded.items()])}",
                               failed=f"{', '.join([str(file) + '(' + reason + '), ' for file, reason in files_failed_upload.items()])}")
    return render_template('upload.html')


@dash.route("/user_albums", methods=['POST', 'GET'])
@login_required
def search_user_albums():
    search_request = RequestProcessor.process_search_request(request)
    user = flask_login.current_user
    user_albums = context.get_db_utility().search_user_albums(user_id=user.id, keyword=search_request['album_keyword'])
    return render_template("albums.html", user_name=user.name, albums=user_albums)


@dash.route("/albums_menu", methods=['POST', 'GET'])
@login_required
def show_user_albums():
    user = flask_login.current_user
    user_albums = context.get_db_utility().get_albums_by_user(user_id=user.id)
    return render_template("albums.html", user_name=user.name, albums=user_albums)


@dash.route("/album/<album_id>/<album_name>", methods=['POST', 'GET'])
@login_required
def show_album(album_id, album_name):
    user_id = flask_login.current_user.id
    current_user_session = session[f"{user_id}"]
    current_user_session[album_id] = 0
    return render_gallery(album_id=album_id, album_name=album_name, page=0)


@dash.route("/next_page/<album_id>/<album_name>", methods=['POST', 'GET'])
@login_required
def next_page(album_id, album_name):
    current_session = session[f"{flask_login.current_user.id}"]
    page = current_session.get(album_id) + 1
    if page == context.get_db_utility().get_album_pictures_pages_amount(album_id=album_id):
        page = 0
    current_session[album_id] = page
    return render_gallery(album_id=album_id, album_name=album_name, page=page)


@dash.route("/previous_page/<album_id>/<album_name>", methods=['POST', 'GET'])
@login_required
def previous_page(album_id, album_name):
    current_session = session[f"{flask_login.current_user.id}"]
    page = current_session.get(album_id) - 1
    if page < 0:
        page = context.get_db_utility().get_album_pictures_pages_amount(album_id=album_id) - 1
    current_session[album_id] = page
    return render_gallery(album_id=album_id, album_name=album_name, page=page)


def render_gallery(album_id, album_name, page):
    return render_template("gallery.html", album_name=album_name,
                           pictures=context.get_db_utility().get_album_pictures_page(album_id, page), album_id=album_id)


@dash.route("/saba", methods=['POST', 'GET'])
@dash.route("/saba/<part>", methods=['POST', 'GET'])
@login_required
def saba(part=1):
    part_number = int(part)
    if part_number > VIDEO_PARTS:
        part = part % VIDEO_PARTS
    if part_number < 1:
        render_template("content_pages/saba_haim.html", video_url='Saba_Haim_Part_1.mp4',
                        next='2', prev='0')
    video_template = Template('Saba_Haim_Part_$num.mp4')
    nextp = part_number + 1
    prevp = part_number - 1
    return render_template("content_pages/saba_haim.html",
                           video_url=video_template.substitute(num=str(part)), next=str(nextp), prev=str(prevp))


@dash.route("/about", methods=['POST', 'GET'])
@login_required
def about():
    return render_template("about.html")


@dash.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    return render_template("main.html")
