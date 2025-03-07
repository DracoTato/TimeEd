from flask import (
    Blueprint,
    render_template,
    current_app as ca,
    redirect,
    url_for,
    flash,
    session,
    g,
    abort,
)
from functools import wraps
from app.db.schema.models import User
from app.db.schema.enums import User_Type
from typing import Sequence
from app.forms import RegisterForm, LoginForm
from app.db import db

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="../../web/templates/routes/auth",
    static_folder="../../web/static/",
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
            flash("Logged in successfully.", "info")
            # TODO Redirect to dashboard

        return view(*args, **kwargs)

    return wrapper


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not g.user:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapper


def role_required(type: User_Type | Sequence[User_Type]):
    """Return a 403 error if the user accessing the page is not in `type`."""

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if not g.user:
                flash("Please log in first.", "error")
                return redirect(url_for("auth.login"))

            allowed_roles = {type} if isinstance(type, User_Type) else set(type)

            if not isinstance(allowed_roles, set) or not all(
                isinstance(role, User_Type) for role in allowed_roles
            ):
                raise TypeError(
                    "Invalid role type. Expected User_Types or list/tuple of User_Types."
                )

            if g.user.role not in allowed_roles:
                flash("You don't have permission to access this page.", "warning")
                return abort(403)
            return view(*args, **kwargs)

        return wrapper

    return decorator


@auth_bp.route("register/", methods=["GET", "POST"])
@logout_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.query(User).filter_by(email=form.email.data).first():
            flash("This user already exists! please login instead.", "warning")
            form.email.errors.append("This email is already in use.")  # type: ignore (Pylance)
            return render_template("register.html", form=form)

        user = User(
            email=form.email.data,  # type: ignore (Pylance)
            password=form.password.data,  # type: ignore (Pylance)
            role=form.account_type.data,
            full_name=form.full_name.data,  # type: ignore (Pylance)
            birthdate=form.birthdate.data,  # type: ignore (Pylance)
            gender=form.gender.data,
        )
        db.session.add(user)

        try:
            db.session.commit()
        except Exception as e:
            ca.logger.error(f"Error while creating new user: {e}")
            flash(
                "We're sorry, an unknown error occurred while trying to create your account. We'll solve it as fast as we can.",
                "warning",
            )
            return render_template("register.html", form=form)
        else:
            print("User created successfully.")
            flash("Your account has been successfully created! Please login.", "info")
            return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("login/", methods=["POST", "GET"])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):  # type: ignore (Pylance)
            session["user_id"] = user.id
            flash("Logged in successfully.", "info")
            return redirect(url_for("index"))  # TODO Redirect to dashboard
        else:
            flash("Wrong email or password.", "warning")

    return render_template("login.html", form=form)


@auth_bp.route("logout/", methods=["GET"])
@login_required
def logout():
    session.pop("user_id")
    g.user = None
    flash("Logged out successfully. Please log in to use the application.", "info")
    return redirect(url_for("auth.login"))
