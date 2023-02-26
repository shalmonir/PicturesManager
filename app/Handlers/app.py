from flask import Flask, request, render_template

from Uploader import Uploader

app = Flask(__name__, template_folder='template')


@app.route("/")
def home():
    return render_template("home_page.html")
    return render_template("login_page.html")


@app.route("/upload", methods=['POST'])
def upload():
    files_uploaded, files_uploaded_failed = Uploader.instance().upload(request.files.getlist("file"))  # Wrap with DTO creation
    files_names = ""
    for file in request.files.getlist("file"):
        files_names = files_names + "<br>" + file.filename
    return "<h1>Files Upload Report</h1><body><b>Pictures Failed</b>:" + \
           "failed with reason (f.e format is not supported)" + str(files_uploaded_failed) + \
           "<br><br>" + \
           "<b>Pictures Succeed</b>:" + files_names + "</body>"
