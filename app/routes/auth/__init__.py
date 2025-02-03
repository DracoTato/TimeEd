from flask import (
    Blueprint,
    render_template,
    current_app as ca,
    redirect,
    url_for,
    flash,
)
from app.models import User
from app.forms import RegisterForm
from app.db import db

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="./templates",
    static_folder="./static",
)


@auth_bp.route("register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.query(User).filter_by(email=form.email.data).first():
            flash("This user already exists! please login instead.", "warning")
            form.email.errors.append("This email is already in use.")  # type: ignore (Pylance)
            return render_template("register.html", form=form)

        user = User.create(
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
            flash("Your account has been successfully created! Please login.", "info")
            return redirect(url_for("auth.login"))
        except Exception as e:
            ca.logger.error(f"Error while creating new user: {e}")
            flash(
                "We're sorry, an unknown error occurred while trying to create your account. We'll solve it as fast as we can.",
                "warning",
            )
            return render_template("register.html", form=form)

    return render_template("register.html", form=form)


@auth_bp.route("login", methods=["POST", "GET"])
def login():
    return render_template("login.html")
