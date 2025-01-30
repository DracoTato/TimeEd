from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    RadioField,
    DateField,
    EmailField,
    PasswordField,
    validators,
    ValidationError,
)
from app.models import Gender, User_Types


def name_validator(_, field):
    if len(str(field.data).strip().split()) < 3:
        raise ValidationError("Full name must be 3 names or more.")


def gender_coerce(value: int):
    return list(Gender)[int(value)]


def user_coerce(value: int):
    return list(User_Types)[int(value)]


class RegisterForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[name_validator, validators.DataRequired("Please fill this field.")],
        render_kw={"autocomplete": "name"},
        # filters=[str.strip],
    )
    gender = RadioField(
        "Gender",
        choices=[(g.value, g.name.title()) for g in list(Gender)],
        validators=[
            validators.DataRequired("Please choose one."),
            validators.AnyOf(list(Gender), "Invalid choice."),
        ],
        render_kw={"autocomplete": "sex"},
        coerce=gender_coerce,
    )
    birthdate = DateField(
        "Birthdate",
        validators=[validators.DataRequired("Please fill this field.")],
        render_kw={"autocomplete": "bday"},
    )
    account_type = RadioField(
        "Account Type",
        choices=[(t.value, t.name.title()) for t in list(User_Types)],
        validators=[
            validators.DataRequired("Please choose one."),
            validators.AnyOf(list(User_Types), "Invalid choice."),
        ],
        render_kw={"autocomplete": "off"},
        coerce=user_coerce,
    )
    email = EmailField(
        "Email",
        validators=[
            validators.Email("Invalid email address."),
            validators.DataRequired("Please Enter your Email."),
        ],
        render_kw={"autocomplete": "email"},
        # filters=[str.strip, str.lower],
    )
    password = PasswordField(
        "Password",
        validators=[
            validators.Length(12, 64, "Password must be more than 8 and less than 64."),
            validators.DataRequired("Please create a password."),
        ],
        render_kw={"autocomplete": "new-password"},
    )
    confirm_password = PasswordField(
        "Confirm Your Password",
        validators=[
            validators.DataRequired("Please confirm your password."),
            validators.EqualTo("password", "Passwords don't match."),
        ],
        render_kw={"autocomplete": "new-password"},
    )
