from flask import Blueprint, render_template

from app.utils import join_web, require_role
from app.db.schema.enums import User_Type


teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher",
    template_folder=join_web("templates/routes/teacher"),
)

teacher_bp.before_request(require_role(User_Type.TEACHER))


@teacher_bp.route("/")
def index():
    return render_template("teacher_base.html")
