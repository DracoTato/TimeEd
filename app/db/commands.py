from os import environ
import click
from sqlalchemy.exc import OperationalError
from random import choice
from flask import current_app

from . import db
from .schema.models import User, Group
from .schema.enums import User_Type, Gender
from datetime import date


@click.command("init-db")
@click.pass_context
def init_db(ctx):
    """Create the db tables"""
    db.create_all()
    click.echo("Database initialized successfully.")

    if click.confirm("Would you like to initialize the admin account as well?"):
        ctx.invoke(init_superadmin)


@click.command("reset-db")
@click.pass_context
def reset_db(ctx):
    """Drop all tables and create new ones"""
    if click.confirm("Are you sure? this action is irreversible"):
        db.drop_all()
        db.create_all()
        click.echo("Database reset successfully.")

        if click.confirm("Would you like to initialize the admin account as well?"):
            ctx.invoke(init_superadmin)
    else:
        click.echo("Action cancelled.")


def get_admin_data():
    """Load admin data from env
    Required variables (all in the form ADMIN_*):
    - EMAIL (account email)
    - PASSWORD (account pass)
    - USERNAME (the username)
    - DISPLAY (the display name)
    - GENDER (male, female)

    Note: this function will return any variable in the form ADMIN_*
    """
    data = {}

    for key, value in environ.items():
        if key.startswith("ADMIN_"):
            data[key.removeprefix("ADMIN_").lower()] = value

    required_data = {"email", "password", "username", "display", "gender"}
    missing_fields = required_data - data.keys()

    if missing_fields:
        raise ValueError(
            f"Missing required admin fields: {missing_fields}, please add these env variables."
        )

    return data


# Create a new admin user
@click.command("init-superadmin")
def init_superadmin():
    """Read superadmin credentials from env and add it to the db"""

    sudo_data: dict[str, str] = get_admin_data()

    # Check if the admin user already exists
    try:
        if db.session.query(User).filter_by(email=sudo_data["email"]).first():
            click.echo("Superadmin user already exists, Doing nothing.")
            return
    except OperationalError:
        if click.confirm(
            "It looks the DB tables don't exist, would you like to create them?"
        ):
            db.create_all()
            pass
        else:
            return

    gender_str = sudo_data["gender"].upper()
    if gender_str not in Gender.__members__:
        raise ValueError(f"Invalid gender value: {gender_str}")

    # Create a new admin user
    admin = User(
        email=sudo_data["email"],
        password=sudo_data["password"],
        role=User_Type._SUPER_ADMIN,
        username=sudo_data["username"],
        display_name=sudo_data["display"],
        birthdate=date.today(),
        gender=Gender[gender_str],
    )

    db.session.add(admin)
    db.session.commit()

    click.echo("Superadmin created successfully.")


@click.command("create-seed")
@click.option("--teacher", help="Create teachers account", is_flag=True)
@click.option("--users", type=int, default=10, help="Number of users to create")
@click.option("--groups", type=int, default=10, help="Number of groups to create")
def create_seed(teacher, users, groups):
    """Create seed data for development and testing"""
    user_template = {
        "email": "user@example.com",
        "username": "user",
        "password": "password",
        "role": User_Type.STUDENT,
        "display_name": "John Doe",
        "birthdate": date(1990, 1, 1),
        "gender": Gender.MALE,
    }
    start_index = 0

    if teacher:
        user_template["role"] = User_Type.TEACHER

    if not current_app.config["DEBUG"] and not current_app.config["TESTING"]:
        if not click.confirm(
            "Are you sure you want to create seed data in production?"
        ):
            return

    existing_seed = (
        db.session.query(User)
        .filter(User.email.regexp_match(r"user[0-9]+@example\.com"))
        .all()
    )
    if existing_seed:
        click.echo("Seed data already exists.")
        if click.confirm("Would you like to append on the existing seed data?"):
            start_index = len(existing_seed)
        else:
            click.echo("Aborting.")
            return

    seed_users = []
    data = user_template
    for i in range(start_index, start_index + users):
        data.update(email=f"user{i}@example.com", username=f"user{i}")
        user = User(**data)
        db.session.add(user)
        seed_users.append(user)

    for i in range(groups):
        group = Group(choice(seed_users), f"Group {i + 1}", "Group Description")
        db.session.add(group)

    db.session.commit()

    click.echo(f"{users} users, {groups} groups created successfully.")


COMMANDS = [init_superadmin, init_db, reset_db, create_seed]


def register_commands(app):
    """Register CLI commands with a flask instance"""
    for command in COMMANDS:
        app.cli.add_command(command)
