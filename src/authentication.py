import hashlib

from flask import Blueprint, redirect, url_for, flash, render_template, request, session
from flask_login import current_user, login_user, logout_user

from src.Configuration.Configuration import ALLOWED_REGISTER_EMAILS
from src.Context.AWSContext import AWSContext
from src.Entities.User import User
from src.Utils.RequestProcessor import RequestProcessor, REQUEST_USER_NAME, REQUEST_USER_PHRASE, REQUEST_USER_EMAIL
from src.validators.AuthInputSanitizer import AuthInputSanitizer

auth = Blueprint('auth', import_name=__name__)

profile = 'local'
context = AWSContext()


@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        login_request = AuthInputSanitizer.sanitize_login_request(RequestProcessor.process_login_request(request))
        user = context.get_db_utility().get_user_by_name(login_request[REQUEST_USER_NAME])
        if user is not None and user.password == hashlib.sha3_512((login_request[REQUEST_USER_PHRASE].encode())).hexdigest():
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
        register_request = RequestProcessor.process_register_request(request)
        if register_request[REQUEST_USER_EMAIL] in ALLOWED_REGISTER_EMAILS:
            try:
                register_name = register_request[REQUEST_USER_NAME]
                register_email = register_request[REQUEST_USER_EMAIL]
                if context.get_db_utility().get_user_by_name(register_name):
                    return render_template("error.html", error_msg=f"User name exist - choose different one")
                if context.get_db_utility().get_user_by_email(register_email):
                    return render_template("error.html", error_msg=f"Email address already registered")

                context.get_db_utility().store(User(name=register_request[REQUEST_USER_NAME],
                                                    password_hash=hashlib.sha3_512(register_request[REQUEST_USER_PHRASE].encode()).hexdigest(),
                                                    email=register_email))
            except Exception as e:
                return render_template("error.html", error_msg=f"Registration Failed :(, reason: {e}")
            return render_template("error.html", error_msg=f"Registration Succeed :)")
        return render_template("error.html", error_msg=f"Registration is not allowed at the moment")
    return render_template("user_auth/register.html")
