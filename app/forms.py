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
from re import fullmatch
from app.db.schema.enums import Gender, User_Type


def display_validator(_, field):
    if not fullmatch(r"^[A-Za-z0-9-_\.\s]$"):
        raise ValidationError(
            "Display name contains one or more illegal characters. only letters, numbers, -, _, . are allowed"
        )


def username_validator(_, field):
    if not fullmatch(r"^[a-z0-9-]$"):
        raise ValidationError(
            "Username contains one or more illegal characters. only letters, numbers, -, _, . are allowed"
        )


def password_validator(_, field):
    if not len(set(field.data)) > 5:
        raise ValidationError("Password must contain at least 5 unique character.")


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
    display_name = StringField(
        "Display Name",
        validators=[
            display_validator,
            validators.DataRequired("Please fill this field."),
        ],
        render_kw={"autocomplete": "name", "title": "Name shown on your profile."},
        filters=[lambda s: s.strip() if s else s],
    )
    username = StringField(
        "Username",
        validators=[
            display_validator,
            validators.DataRequired("Please fill this field."),
        ],
        render_kw={
            "autocomplete": "name",
            "title": "Your unique username, can't be changed.",
        },
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
        render_kw={
            "autocomplete": "off",
            "title": "Different account types have different permissions.",
        },
        coerce=user_coerce,
    )
    email = EmailField(
        "Email",
        validators=[
            validators.Email("Invalid email address."),
            validators.DataRequired("Please Enter your Email."),
        ],
        render_kw={
            "autocomplete": "email",
            "title": "Your email, e.g. example@gmail.com",
        },
        filters=[lambda s: s.strip().lower() if s else s],
    )
    password = PasswordField(
        "Password",
        validators=[
            password_validator,
            validators.Length(8, 64, "Password must be 8-64 characters."),
            validators.DataRequired("Please create a password."),
        ],
        render_kw={
            "autocomplete": "new-password",
            "title": "Your account password, the stronger, the better.",
        },
    )
    confirm_password = PasswordField(
        "Confirm Your Password",
        validators=[
            validators.DataRequired("Please confirm your password."),
            validators.EqualTo("password", "Passwords don't match."),
        ],
        render_kw={
            "autocomplete": "new-password",
            "title": "Repeat your password again.",
        },
    )

    def is_required(self, field):
        return any(isinstance(v, validators.DataRequired) for v in field.validators)


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

    def is_required(self, field):
        return any(isinstance(v, validators.DataRequired) for v in field.validators)
