"""Centralized file to hold all messages used in the application to ease i18n."""

from typing import Union
from enum import Enum
from flask_babel import _
from flask import flash


# Error messages
class ErrorMessages(Enum):
    USER_EXISTS = _("User already exists.")
    USERNAME_INUSE = _("Username is in use, please choose another one.")
    INVALID_CREDENTIALS = _("Invalid email or password.")
    PERMISSION_DENIED = _("You don't have permission to access this page.")
    UNKNOWN_ERROR = _(
        "Sorry, an unknown error occurred. We'll solve it as fast as we can."
    )
    INVALID_FORM = _("Invalid form data.")


class WarningMessages(Enum):
    LOGIN_REQUIRED = _("Please log in first.")


class SuccessMessages(Enum):
    LOGIN_SUCCESS = _("Logged in successfully.")
    LOGOUT_SUCCESS = _("Logged out successfully.")
    ACCOUNT_CREATED = _("Your account has been successfully created.")


class InfoMessages(Enum):
    ALREADY_LOGGED = _("You are already logged in.")


FlashableMessages = Union[ErrorMessages, WarningMessages, SuccessMessages, InfoMessages]


def flash_message(message: FlashableMessages):
    """
    Flashes a message to the user.

    Args:
        message (Enum): An instance of one of the message enums, such as
                        `ErrorMessages`, `WarningMessages`, `SuccessMessages`, or `InfoMessages`.

    Note:
        The category is automatically inferred from the message class name.
        ErrorMessages will be flashed with the "danger" category.
    """

    category = message.__class__.__name__.replace("Messages", "").lower()
    category = "danger" if category == "error" else category
    flash(message.value, category)


__all__ = [
    "ErrorMessages",
    "WarningMessages",
    "SuccessMessages",
    "InfoMessages",
    "flash_message",
]
