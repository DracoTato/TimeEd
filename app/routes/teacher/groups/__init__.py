from flask import (
    Blueprint,
    render_template,
    url_for,
    g,
    redirect,
    current_app as ca,
    abort,
    jsonify,
)
from sqlalchemy.exc import MultipleResultsFound

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
        return redirect(url_for("teacher.groups.view", id=group.id))
    else:
        return render_template(
            "group_form.html",
            form=form,
            title="Create A Group",
            action=url_for("teacher.groups.create"),
            method="post",
            btn_txt="Create",
        )


@group_bp.route("/<int:id>", methods=["GET", "POST"])
def edit(id):
    try:
        group = db.session.query(Group).filter_by(id=id).one()
    except MultipleResultsFound:
        ca.logger.error(
            f"Multiple groups found with id {id}, requested by user {g.user.id}"
        )
        return abort(500)

    if not group.owner_id == g.user.id or not group:
        return abort(404)

    form = GroupForm(title=group.title, description=group.description)
    if form.validate_on_submit():
        group.title = form.title.data
        group.description = form.description.data
        db.session.commit()

        flash_message(SuccessMessages.GROUP_UPDATE_SUCCESS)
        return redirect(url_for("teacher.groups.view", id=group.id))
    else:
        return render_template(
            "group_form.html",
            form=form,
            title="Edit A Group",
            action=url_for("teacher.groups.edit", id=id),
            method="post",
            btn_txt="Update",
        )


@group_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    if not id:
        return abort(400)

    try:
        group = db.session.query(Group).filter_by(id=id).one()
    except MultipleResultsFound:
        ca.logger.error(
            f"Multiple groups found with id {id}, requested by user {g.user.id}"
        )
        return abort(500)

    if not group.owner_id == g.user.id:
        return abort(404)

    db.session.delete(group)
    db.session.commit()

    ca.logger.info(f"Deleted group with id {group.id}")

    flash_message(SuccessMessages.GROUP_DELETE_SUCCESS)
    return jsonify({"url": str(url_for("teacher.index"))})


@group_bp.route("/view/<int:id>", methods=["GET"])
def view(id):
    try:
        group = db.session.query(Group).filter_by(id=id).one()
    except MultipleResultsFound:
        ca.logger.error(
            f"Multiple groups found with id {id}, requested by user {g.user.id}"
        )
        return abort(500)

    if not group:
        return abort(404)

    is_owner = False
    if group.owner_id == g.user.id:
        is_owner = True

    return render_template(
        "view_group.html", title="View A Group", is_owner=is_owner, group=group
    )
