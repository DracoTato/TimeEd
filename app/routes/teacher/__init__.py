from flask import Blueprint, render_template, g, request, jsonify
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.utils import join_web, require_role, register_blueprints
from app.db.schema.enums import User_Type
from app.db.schema.models import Group, Session
from app.db import db

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

MODEL_MAP = {
    "Group": Group,
    "Session": Session,
}


@teacher_bp.route("/")
def index():
    return render_template("teacher_base.html")


@teacher_bp.route("/view_all")
def view_all():
    groups = g.user.owned_groups
    # Extract all sessions from each groups
    sessions = [session for group in groups for session in group.sessions]
    # Finally combine them all into a dictionary with a type identifier
    combined_data = [{"type": "Group", "data": g} for g in groups] + [
        {"type": "Session", "data": s} for s in sessions
    ]

    return render_template("view_all.html", title="View All", data=combined_data)


@teacher_bp.route("/delete_all", methods=["POST"])
def delete_all():
    data = request.get_json()
    status = 0

    for entry in data:
        try:
            object = (
                db.session.query(MODEL_MAP[entry["type"]])
                .filter_by(id=entry["id"])
                .one()
            )
            if object.owner_id == g.user.id:
                db.session.delete(object)
            else:
                continue
        except NoResultFound:
            status = 1
        except MultipleResultsFound:
            status = 2

    db.session.commit()

    return jsonify({"status": status})
