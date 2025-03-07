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
def init_db():
    """Create the db tables"""
    db.create_all()
    click.echo("Database initialized successfully.")


@click.command("reset-db")
def reset_db():
    """Drop all tables and create new ones"""
    if click.confirm("Are you sure? this action is irreversible"):
        db.drop_all()
        db.create_all()
        click.echo("Database reset successfully.")
    else:
        click.echo("Action cancelled.")


def get_admin_data():
    """Load admin data from env
    Required variables (all in the form ADMIN_*):
    -EMAIL(account email)
    -PASSWORD(account pass)
    -NAME(the username)
    -GENDER(male, female)
    """
    data = {}

    for key, value in environ.items():
        if key.startswith("ADMIN_"):
            data[key.removeprefix("ADMIN_").lower()] = value

    required_data = {"email", "password", "name", "gender"}
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
        sudo_data["email"],
        sudo_data["password"],
        User_Type._SUPER_ADMIN,
        sudo_data["name"],
        date.today(),
        Gender[gender_str],
    )

    db.session.add(admin)
    db.session.commit()

    click.echo("Superadmin created successfully.")


@click.command("create-seed")
@click.option("--users", type=int, default=10, help="Number of users to create")
@click.option("--groups", type=int, default=10, help="Number of groups to create")
def create_seed(users, groups):
    """Create seed data for development and testing"""
    user_template = {
        "email": "user@example.com",
        "password": "password",
        "role": User_Type.STUDENT,
        "full_name": "John Doe",
        "birthdate": date(1990, 1, 1),
        "gender": Gender.MALE,
    }

    if not current_app.config["DEBUGGING"] and not current_app.config["TESTING"]:
        if not click.confirm(
            "Are you sure you want to create seed data in production?"
        ):
            return

    if db.session.query(User).filter_by(email="user0@example.com").first():
        click.echo("Seed data already exists.")
        click.echo("Aborting.")
        return

    seed_users = []
    for i in range(users):
        data = user_template
        data.update(email=f"user{i}@example.com")
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
