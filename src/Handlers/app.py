import os

from flask import render_template, Blueprint
from flask import send_from_directory

from src.Context.LocalContextMgr import LocalContextMgr

# db = SQLAlchemy()
main_api = Blueprint("main_api", __name__, template_folder="templates", static_folder="static")


# def create_app():
#     app = Flask(__name__, template_folder='template')
#     app.config['SQLALCHEMY_DATABASE_URI'] = DB_SECRET
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#     db.init_app(app)
#     app.register_blueprint(main_api)
#     with app.app_context():
#         db.create_all()
#     return app


profile = 'local'
context = LocalContextMgr()


@main_api.route("/show2", methods=['POST', 'GET'])
def show_pictures_in_album():
    from src.DB.DBUtil import DBUtil
    album_id = 2
    util = DBUtil()
    display_pictures = util.get_album_pictures(album_id=album_id)
    string_print = f"{', '.join([pic.file_name  for pic in display_pictures])}"
    return render_template("test.html", str_printable=string_print)


@main_api.route('/cdn/<path:filepath>')
def download_file(filepath):
    directory, filename = os.path.split(filepath)
    return send_from_directory(directory, filename, as_attachment=False)
