from flask_login import LoginManager
from werkzeug.security import check_password_hash

from .database import User


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.get(id=int(user_id))


def authenticate_user(username, password):

    try:
        user = User.get(username=username)
    except User.DoesNotExit:
        return None

    if check_password_hash(user.password, password):
        return user
    else:
        return None
