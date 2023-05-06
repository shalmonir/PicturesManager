from flask import Blueprint, redirect, url_for, flash, render_template, request, session
from flask_login import current_user, login_user, logout_user

from src.Context.LocalContextMgr import LocalContextMgr
from src.Utils.RequestProcessor import RequestProcessor

auth = Blueprint('auth', import_name=__name__)

profile = 'local'
context = LocalContextMgr()


@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        login_request = RequestProcessor.process_login_request(request)
        user = context.get_db_utility().get_user_by_name(login_request['username'])
        if user is not None and user.password == (login_request['password']):
            if login_user(user, False):
                flash('Logged.', 'info')
                session.permanent = True
                session[f"{user.id}"] = {}
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash('Your account is blocked.', 'warning')
                return redirect(url_for('main.index'))
        flash('Invalid email or password.', 'warning')
    return render_template('user_auth/login.html')


@auth.route("/log-out", methods=['POST', 'GET'])
def log_out():
    logout_user()
    return render_template("error.html", error_msg=f"Logged Out")


@auth.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        return render_template("error.html", error_msg=f"Registration is not allowed at the moment")
    return render_template("user_auth/register.html")
