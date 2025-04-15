from .db.schema.enums import User_Type
from app.messages import flash_message, ErrorMessages, WarningMessages
from flask import g, redirect, url_for, abort, current_app as ca
from os import getcwd, path

WEB_PATH = path.join(getcwd(), "app/web")


def require_role(user_type: User_Type | list[User_Type]):
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


def join_web(dir_path: str):
    """Combine `dir_path` with the path of the web folder.
    Returns: str
    """
    return path.join(WEB_PATH, dir_path)
