from flask import (
    Blueprint,
    render_template,
    current_app as ca,
    redirect,
    url_for,
    session,
    g,
)
from functools import wraps

from app.db.schema.models import User
from app.forms import RegisterForm, LoginForm
from app.db import db
from app.messages import (
    flash_message,
    ErrorMessages,
    WarningMessages,
    SuccessMessages,
    InfoMessages,
)
from app.utils import join_web, check_unique_cols

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder=join_web("templates/routes/auth"),
)


# Helper functions
@auth_bp.before_app_request
def load_user():
    user_id = session.get("user_id")
    if user_id:
        g.user = db.session.query(User).get(user_id)
    else:
        g.user = None


def logout_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user:
            flash_message(InfoMessages.ALREADY_LOGGED)
            return redirect(url_for("root.index"))

        return view(*args, **kwargs)

    return wrapper


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not g.user:
            flash_message(WarningMessages.LOGIN_REQUIRED)
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapper


@auth_bp.route("register/", methods=["GET", "POST"])
@logout_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not check_unique_cols(
            db=db,
            db_table=User,
            form_fields=[form.email, form.username],
            db_cols=["email", "username"],
            err_msgs=[ErrorMessages.EMAIL_EXISTS, ErrorMessages.USERNAME_EXISTS],
        ):
            return render_template("register.html", form=form)

        user = User(
            email=form.email.data,
            password=form.password.data,
            role=form.account_type.data,
            username=form.username.data,
            display_name=form.display_name.data,
            birthdate=form.birthdate.data,
            gender=form.gender.data,
        )
        db.session.add(user)

        try:
            db.session.commit()
        except Exception as e:
            ca.logger.error(f"Error while creating new user: {e}")
            flash_message(ErrorMessages.UNKNOWN_ERROR)
            return render_template("register.html", form=form)
        else:
            flash_message(SuccessMessages.ACCOUNT_CREATED)
            ca.logger.info(f"New user created: {user.username}")
            return redirect(url_for("auth.login"))
    elif form.errors:
        flash_message(ErrorMessages.INVALID_FORM)

    return render_template("register.html", form=form)


@auth_bp.route("login/", methods=["POST", "GET"])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session.permanent = True
            session["user_id"] = user.id
            flash_message(SuccessMessages.LOGIN_SUCCESS)
            return redirect(url_for("root.index"))
        else:
            flash_message(ErrorMessages.INVALID_CREDENTIALS)

    return render_template("login.html", form=form)


@auth_bp.route("logout/", methods=["GET"])
@login_required
def logout():
    session.pop("user_id")
    g.user = None
    flash_message(SuccessMessages.LOGOUT_SUCCESS)
    return redirect(url_for("auth.login"))
