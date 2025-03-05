from os import environ
import click
from flask.cli import with_appcontext

from . import db


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
    from .schema.models import User, User_Type, Gender
    from datetime import date

    sudo_data: dict[str, str] = get_admin_data()

    # Check if the admin user already exists
    if db.session.query(User).filter_by(email=sudo_data["email"]).first():
        click.echo("Superadmin user already exists, Doing nothing.")
        return

    gender_str = sudo_data["gender"].upper()
    if gender_str not in Gender.__members__:
        raise ValueError(f"Invalid gender value: {gender_str}")

    # Create a new admin user
    admin = User.create(
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


COMMANDS = [init_superadmin, init_db, reset_db]

def register_commands(app):
    """Register CLI commands with a flask instance"""
    for command in COMMANDS:
        app.cli.add_command(command)
