from flask import Blueprint, render_template

from app.utils import join_web, require_role, register_blueprints
from app.db.schema.enums import User_Type

from .groups import group_bp

teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher",
    template_folder=join_web("templates/routes/teacher"),
)

teacher_bp.before_request(require_role(User_Type.TEACHER))

BLUEPRINTS = [group_bp]
register_blueprints(teacher_bp, BLUEPRINTS)


@teacher_bp.route("/")
def index():
    return render_template("teacher_base.html")
