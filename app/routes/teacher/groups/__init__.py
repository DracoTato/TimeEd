from flask import (
    Blueprint,
    render_template,
    url_for,
    g,
    redirect,
    current_app as ca,
    abort,
)
from sqlalchemy.orm.exc import MultipleResultsFound

from app.forms import GroupForm
from app.db import db
from app.db.schema.models import Group
from app.messages import flash_message, SuccessMessages
from app.utils import join_web

group_bp = Blueprint(
    "groups",
    __name__,
    url_prefix="/groups",
    template_folder=join_web("templates/routes/teacher/groups"),
)


@group_bp.route("/", methods=["GET", "POST"])
def create():
    form = GroupForm()

    if form.validate_on_submit():
        group = Group(g.user, form.title.data, form.description.data)
        db.session.add(group)
        db.session.commit()

        flash_message(SuccessMessages.GROUP_CREATE_SUCCESS)
        return redirect(url_for("teacher.index"))
    else:
        return render_template(
            "group_form.html",
            form=form,
            title="Create A Group",
            action=url_for("teacher.groups.create"),
            method="post",
            btn_txt="Create",
        )


@group_bp.route("/<int:id>", methods=["GET", "PUT"])
def edit(id):
    try:
        group = db.session.query(Group).filter_by(id=id).one_or_none()
    except MultipleResultsFound:
        ca.logger.error(
            f"Multiple groups found with id {id}, requested by user {g.user.id}"
        )
        return abort(500)

    if not group.owner_id == g.user.id:
        return abort(404)

    form = GroupForm(title=group.title, description=group.description)
    if form.validate_on_submit():
        group.title = form.title.data
        group.description = form.description.data
        db.session.commit()

        flash_message(SuccessMessages.GROUP_UPDATE_SUCCESS)
        return redirect(url_for("teacher.index"))
    else:
        return render_template(
            "group_form.html",
            form=form,
            title="Edit A Group",
            action=url_for("teacher.groups.edit", id=id),
            method="put",
            btn_txt="Update",
        )


@group_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    try:
        group = db.session.query(Group).filter_by(id=id).one_or_none()
    except MultipleResultsFound:
        ca.logger.error(
            f"Multiple groups found with id {id}, requested by user {g.user.id}"
        )
        return abort(500)

    if not group.owner_id == g.user.id:
        return abort(404)

    db.delete(group)
    db.commit()

    ca.logger.info(f"Deleted group with id {group.id}")
