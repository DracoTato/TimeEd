from enum import Enum


class User_Type(Enum):
    _SUPER_ADMIN = 0  # Restricted type
    _ADMIN = 1  # Restricted type
    TEACHER = 2
    STUDENT = 3


class Gender(Enum):
    MALE = 0
    FEMALE = 1


class Account_Status(Enum):
    BANNED = 0
    UNVERIFIED = 1
    PENDING = 2
    VERIFIED = 3


class Request_Status(Enum):
    PENDING = 0
    DENIED = 1
    ACCEPTED = 2


class Question_Status(Enum):
    OPEN = 0
    CLOSED = 2
