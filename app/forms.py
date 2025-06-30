from datetime import date, timedelta
from enum import Enum
from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    RadioField,
    DateField,
    EmailField,
    PasswordField,
    DateTimeLocalField,
    IntegerField,
    SelectField,
)
from wtforms import validators, ValidationError
from re import fullmatch
from typing import Type

from app.db.schema.enums import Gender, User_Type
from app.utils import choices_from_enum, RRULE_FREQS


def display_validator(_, field):
    if not fullmatch(r"[A-Za-z0-9-_\. ]+", field.data):
        raise ValidationError(
            "Display name contains one or more illegal characters. only letters, numbers, -, _, . are allowed"
        )


def username_validator(_, field):
    if not fullmatch(r"[a-z0-9-_\.]+", field.data):
        raise ValidationError(
            "Username contains one or more illegal characters. only lowercase letters, numbers, -, _, . are allowed"
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


def if_other_empty(other_field_name):
    """Require another field to be empty"""

    def _validator(form, field):
        other_field = form._fields.get(other_field_name)
        if not other_field:
            raise Exception(f"No field named '{other_field_name}' in {form.__name__}")

        if other_field.data:
            raise ValidationError(
                f"Please use either {other_field.label.text} or {field.label.text}, but not both!"
            )

    return _validator


def enum_coerce(enum: Type[Enum]):
    def _coerce(value: int):
        try:
            return enum(int(value))
        except (ValueError, TypeError):
            return None

    return _coerce


class TimeDeltaField(StringField):
    def process_formdata(self, valuelist):
        if not valuelist:
            self.data = None
            return

        value = valuelist[0].strip()
        pattern = r"(?:(\d+)[Hh])?\s*(?:(\d+)[Mm])?"
        match = fullmatch(pattern, value)

        if match:
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            self.data = timedelta(days=0, hours=hours, minutes=minutes)
        else:
            self.data = valuelist[0]
            raise ValidationError(
                "Invalid duration format. Try: 2h 30m (order matters)"
            )


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
            username_validator,
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
        choices=choices_from_enum(Gender),
        validators=[
            validators.DataRequired("Please choose one."),
            validators.AnyOf(list(Gender), "Invalid choice."),
        ],
        render_kw={"autocomplete": "sex"},
        coerce=enum_coerce(Gender),
    )
    birthdate = DateField(
        "Birthdate",
        validators=[age_validator, validators.DataRequired("Please fill this field.")],
        render_kw={"autocomplete": "bday"},
    )
    account_type = RadioField(
        "Account Type",
        choices=choices_from_enum(User_Type, startswithout="_"),
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
        coerce=enum_coerce(User_Type),
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

    def is_required(self, field) -> bool:
        return any(isinstance(v, validators.DataRequired) for v in field.validators)


class GroupForm(FlaskForm):
    title = StringField(
        "Group Title",
        validators=[
            validators.DataRequired("Please enter a title for the group."),
            validators.Length(8, 32, "Title must be %(min)d-%(max)d long."),
        ],
    )
    description = StringField(
        "Group Description",
        validators=[
            validators.DataRequired("Please enter a description for the group."),
            validators.Length(8, 64, "Description must be %(min)d-%(max)d long."),
        ],
    )

    def is_required(self, field) -> bool:
        return any(isinstance(v, validators.DataRequired) for v in field.validators)


class SessionForm(FlaskForm):
    title = StringField(
        "Session Title",
        validators=[
            validators.DataRequired("Please enter a title for the session."),
            validators.Length(8, 32, "Title must be %(min)d-%(max)d long."),
        ],
    )
    description = StringField(
        "Session Description",
        validators=[
            validators.DataRequired("Please enter a description for the session."),
            validators.Length(8, 64, "Description must be %(min)d-%(max)d long."),
        ],
    )
    start = DateTimeLocalField(
        "Start Time",
        validators=[validators.DataRequired()],
    )
    duration = TimeDeltaField(
        "Session Duration",
        validators=[validators.DataRequired()],
        render_kw={"placeholder": "2h 30m"},
    )
    freq = SelectField(
        "Frequency",
        choices=choices_from_enum(RRULE_FREQS),
        validators=[validators.Optional()],
        default="None",
        coerce=enum_coerce(RRULE_FREQS),
    )
    interval = IntegerField(
        "Interval",
        validators=[validators.Optional(), validators.NumberRange(min=1)],
        render_kw={
            "title": "Depends on frequency, if it's set to weekly and interval is 2, then repeat every 2 weeks",
            "value": "1",
        },
    )
    until = DateTimeLocalField(
        "Repeat Until",
        validators=[validators.Optional()],
        render_kw={"title": "No further repetitions will occur after this date"},
    )
    count = IntegerField(
        "Repeat Count",
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1),
            if_other_empty("until"),
        ],
        render_kw={"title": "Will only generate the specified number of repetitions"},
    )
    max_students = IntegerField(
        "Max Students",
        validators=[validators.Optional(), validators.NumberRange(min=1)],
    )

    def is_required(self, field) -> bool:
        return any(isinstance(v, validators.DataRequired) for v in field.validators)
