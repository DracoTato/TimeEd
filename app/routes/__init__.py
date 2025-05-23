from flask import Blueprint, redirect, url_for

from app.utils import get_user_home
from .auth import auth_bp
from .teacher import teacher_bp

root_bp = Blueprint("root", __name__)

# list of blueprints to be registered in app/__init__.py
BLUEPRINTS = [root_bp, auth_bp, teacher_bp]


# routes
@root_bp.route("/")
def index():
    user_home = get_user_home()
    if not user_home:
        return redirect(url_for("auth.login"))
    else:
        return redirect(user_home)
