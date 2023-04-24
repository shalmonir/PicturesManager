import os

from flask import Blueprint, send_from_directory, current_app, send_file
from flask_login import login_required


download = Blueprint('download', import_name=__name__)


@download.route('/cdn/<path:filepath>')
@login_required
def cdn(filepath):
    directory, filename = os.path.split(filepath)
    current_app.logger.debug(f"dir: {directory}, filename: {filename}, filepath: {filepath}")
    if os.name != 'nt':
        directory = f"/{str(directory)}"
    return send_from_directory(directory, filename, as_attachment=False)
