from flask import Flask, request, render_template
from Uploader import Uploader
from Reporter import Reporter

app = Flask(__name__, template_folder='template')


@app.route('/')
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return render_template('home_page.html', msg='Logged in :)')
    return render_template("login.html")


@app.route("/upload", methods=['POST'])
def upload():
    request_files = request.files.getlist("file")
    files_uploaded, files_failed_upload = Uploader.instance().upload(request_files)
    Reporter.instance().report_upload_process(files_uploaded, files_failed_upload)
    return render_template("upload_summary.html", successfully=f"{', '.join([str(file) for file in files_uploaded])}",
                           failed=f"{', '.join([str(file) + '(' + reason + '), ' for file, reason in files_failed_upload.items()])}")
