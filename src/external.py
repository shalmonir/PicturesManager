from flask_login import LoginManager, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from src.Entities import User
    user = db.session.execute(db.session.query(User.User).filter_by(id=user_id)).scalar()
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message = 'welcome :)'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
login_manager.needs_refresh_message = 'Please refresh'
login_manager.needs_refresh_message_category = 'warning'


class Guest(AnonymousUserMixin):
    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False


login_manager.anonymous_user = Guest