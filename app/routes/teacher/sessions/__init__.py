from flask import (
    Blueprint,
    render_template,
    url_for,
    g,
    redirect,
)

from app.forms import SessionForm
from app.db import db
from app.db.schema.models import Session, Group
from app.messages import flash_message, SuccessMessages
from app.utils import join_web, make_rrule

session_bp = Blueprint(
    "sessions",
    __name__,
    url_prefix="/sessions",
    template_folder=join_web("templates/routes/teacher/sessions"),
)


@session_bp.route("/<int:group_id>", methods=["GET", "POST"])
def create(group_id):
    form = SessionForm()

    if form.validate_on_submit():
        session = Session(
            owner=g.user,
            group=db.session.query(Group).filter_by(id=group_id).one(),
            title=form.title.data,
            description=form.description.data,
            start=form.start.data,
            duration=form.duration.data,
            rule=make_rrule(freq=form.freq.data, interval=form.interval.data)
            if form.freq.data.value >= 0
            else None,
        )
        db.session.add(session)
        db.session.commit()

        flash_message(SuccessMessages.SESSION_CREATE_SUCCESS)
        return redirect(url_for("teacher.groups.view", id=session.group_id))
    else:
        return render_template(
            "session_form.html",
            form=form,
            title="Create A Session",
            action=url_for("teacher.sessions.create", group_id=group_id),
            method="post",
            btn_txt="Create",
        )
