import flask_login
from flask import Blueprint, render_template, request, session
from flask_login import login_required
from src.Context.LocalContextMgr import LocalContextMgr
from src.Utils.RequestProcessor import RequestProcessor

dash = Blueprint('dashboard', import_name=__name__)
context = LocalContextMgr()


@dash.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("home.html", str_printable='dash aaaaa')


@dash.route("/upload", methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        request_internal = RequestProcessor.process_upload_request(request)
        files_uploaded, files_failed_upload = context.upload(request_internal['files'], request_internal['album_name'], flask_login.current_user.id)
        return render_template("upload_summary.html",
                               album=f"{request_internal['album_name']}",
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
    user_albums = context.get_db_utility().get_user_albums(user_id=user.id)
    return render_template("albums.html", user_name=user.name, albums=user_albums)


@dash.route("/album/<album_id>/<album_name>", methods=['POST', 'GET'])
@login_required
def show_album(album_id, album_name):
    user_id = flask_login.current_user.id
    current_user_session = session[f"{user_id}"]
    current_user_session[album_id] = 0
    return render_template("gallery.html", album_name=album_name,
                           pictures=context.get_db_utility().get_album_pictures_page(album_id, 0), album_id=album_id)


@dash.route("/next_page/<album_id>/<album_name>", methods=['POST', 'GET'])
@login_required
def next_page(album_id, album_name):
    current_session = session[f"{flask_login.current_user.id}"]
    page = current_session.get(album_id) + 1
    if page == context.get_db_utility().get_album_pictures_pages_amount(album_id=album_id):
        page = 0
    current_session[album_id] = page
    return render_template("gallery.html", album_name=album_name,
                           pictures=context.get_db_utility().get_album_pictures_page(album_id, page), album_id=album_id)


@dash.route("/previous_page/<album_id>/<album_name>", methods=['POST', 'GET'])
@login_required
def previous_page(album_id, album_name):
    current_session = session[f"{flask_login.current_user.id}"]
    page = current_session.get(album_id) - 1
    if page < 0:
        page = context.get_db_utility().get_album_pictures_pages_amount(album_id=album_id) - 1
    current_session[album_id] = page
    return render_template("gallery.html", album_name=album_name,
                           pictures=context.get_db_utility().get_album_pictures_page(album_id, page), album_id=album_id)
