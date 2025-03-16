from datetime import date, timedelta
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
from app.db.schema.enums import Gender, User_Type


def name_validator(_, field):
    if len(str(field.data).strip().split()) < 2:
        raise ValidationError("Full name must be 2-5 names.")
    elif len(str(field.data).strip().split()) > 5:
        raise ValidationError("Too long.")


def age_validator(_, field):
    # 120 yo max
    today = date.today()
    max_age = today - timedelta(days=365 * 120)
    # 8 yo min
    min_age = today - timedelta(days=365 * 8)

    if field.data > min_age:
        raise ValidationError("You're too young for this platform.")
    if field.data < max_age:
        raise ValidationError("Please enter your real age :|")


def gender_coerce(value: int):
    try:
        return Gender(int(value))
    except ValueError:
        return None


def user_coerce(value: int):
    try:
        return User_Type(int(value))
    except ValueError:
        return None


class RegisterForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[name_validator, validators.DataRequired("Please fill this field.")],
        render_kw={"autocomplete": "name"},
        filters=[lambda s: s.strip() if s else s],
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
        validators=[age_validator, validators.DataRequired("Please fill this field.")],
        render_kw={"autocomplete": "bday"},
    )
    account_type = RadioField(
        "Account Type",
        choices=[
            (t.value, t.name.title())
            for t in list(User_Type)
            if not t.name.startswith("_")
        ],
        validators=[
            validators.DataRequired("Please choose one."),
            validators.AnyOf(
                [t for t in list(User_Type) if not t.name.startswith("_")],
                "Invalid choice.",
            ),
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
        filters=[lambda s: s.strip().lower() if s else s],
    )
    password = PasswordField(
        "Password",
        validators=[
            validators.Length(8, 64, "Password must be 8-64 characters."),
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


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            validators.DataRequired("Please Enter your email address."),
        ],
        render_kw={"autocomplete": "email"},
        filters=[lambda s: s.strip().lower() if s else s],
    )
    password = PasswordField(
        "Password",
        validators=[
            validators.DataRequired("Please enter your password"),
        ],
        render_kw={"autocomplete": "current-password"},
    )
