from flask_sqlalchemy import SQLAlchemy
from flask import g, redirect, url_for, abort, current_app as ca
from wtforms import Field
from os import getcwd, path
from typing import Sequence, Callable

from .db.schema.enums import User_Type
from app.messages import flash_message, ErrorMessages, WarningMessages

WEB_PATH = path.join(getcwd(), "app/web")


def require_role(user_type: User_Type | list[User_Type]) -> Callable:
    def check_roles():
        allowed_roles = user_type if isinstance(user_type, list) else [user_type]

        if not isinstance(allowed_roles, list) or not all(
            isinstance(role, User_Type) for role in allowed_roles
        ):
            ca.logger.warning("Invalid role type given to require_role method.")
            raise TypeError(
                "Invalid role type. Expected User_Types or list of User_Types."
            )

        if g.user is None:
            flash_message(WarningMessages.LOGIN_REQUIRED)
            return redirect(url_for("auth.login"))
        elif g.user.role not in allowed_roles:
            flash_message(ErrorMessages.PERMISSION_DENIED)
            return abort(403)

    return check_roles


def join_web(dir_path: str) -> str:
    """Combine `dir_path` with the path of the web folder.
    Returns: str
    """
    return path.join(WEB_PATH, dir_path)


def check_unique_cols(
    db: SQLAlchemy,
    db_table,
    form_fields: Sequence[Field],
    db_cols: Sequence[str],
    err_msgs: Sequence[str],
) -> bool:
    """Checks the values of form_fields in db_cols if they're unique.

    db: The db.
    db_table: The db entity to query on.
    form_fields: The actual form fields whose values are checked.
    db_cols: The db columns which the form fields are checked against.
    err_msgs: Error messages to append to fields in case of failure.

    Note: form_fields, db_cols, err_msgs must be of the same length, as they're zipped together.
    form_fields[0] is queried against db_cols[0] on failure it appends err_msgs[0] to the field error list,
    and so on for all other items.
    """
    zipped = zip(db_cols, form_fields, err_msgs)

    is_unique = True
    for row in zipped:
        try:
            if db.session.query(db_table).filter_by(**{row[0]: row[1].data}).first():
                flash_message(row[2])
                row[1].errors.append(row[2].value)
                is_unique = False
        except Exception as e:
            ca.logger.error(e)

    return is_unique


def get_user_home():
    """Return user's home url, if user is logged in"""
    user = g.get("user")
    return (
        url_for(f"{user.role.name.lower().removeprefix('_')}.index") if user else None
    )


def register_blueprints(parent, blueprints: list):
    """Register blueprints with a flask instance or a another blueprint."""
    for bp in blueprints:
        parent.register_blueprint(bp)
