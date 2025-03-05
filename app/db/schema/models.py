from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime
from uuid import uuid4

from .enums import *
from .. import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(default=lambda: str(uuid4()), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    role: Mapped[User_Type]
    status: Mapped[Account_Status] = mapped_column(default=Account_Status.UNVERIFIED)
    full_name: Mapped[str]
    birthdate: Mapped[date]
    gender: Mapped[Gender]
    bio: Mapped[str | None]

    owned_groups: Mapped[list["Group"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    enrolled_groups: Mapped[list["Enroll"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    absence_requests: Mapped[list["AbsenceRequest"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    questions: Mapped[list["Question"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        email: str,
        password: str,
        role: User_Type,
        full_name: str,
        birthdate: date,
        gender: Gender,
        bio: str | None = None,
    ):
        self.email = email
        self.role = role
        self.full_name = full_name
        self.birthdate = birthdate
        self.gender = gender
        self.bio = bio
        self.__set_password(password)

    def __set_password(self, value: str):
        """Store the password as a hash.
        Note: Use `create` instead of directly using this method!
        """
        self.password_hash = generate_password_hash(value)

    def check_password(self, value: str):
        """Check the given password against the stored hash."""
        return check_password_hash(self.password_hash, value)

    def __repr__(self) -> str:
        return f"<User {self.id!r} (email: {self.email!r}, role: {self.role!r})>"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(256))

    owner: Mapped["User"] = relationship(back_populates="owned_groups")
    enrolls: Mapped[list["Enroll"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )
    questions: Mapped[list["Question"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )

    def __init__(self, owner: User, title: str, description: str):
        self.title = title
        self.description = description

        self.owner = owner

    def __repr__(self) -> str:
        return (
            f"<Group {self.id!r} (title: {self.title!r}, owner_id: {self.owner_id!r}>"
        )


class Enroll(Base):
    __tablename__ = "enrolls"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    user: Mapped["User"] = relationship(back_populates="enrolled_groups")
    group: Mapped["Group"] = relationship(back_populates="enrolls")

    def __init__(self, user: User, group: Group):
        self.user = user
        self.group = group

    def __repr__(self) -> str:
        return f"<Enroll {self.id!r} (user_id: {self.user_id!r}, group_id: {self.group_id!r})>"


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    repeat_until: Mapped[date]
    repeat_interval: Mapped[int]  # No. of days
    title: Mapped[str]
    description: Mapped[str]
    start: Mapped[datetime]
    end: Mapped[datetime]
    max_students: Mapped[int | None]
    properties: Mapped[str | None]  # JSON

    group: Mapped["Group"] = relationship(back_populates="sessions")
    absence_requests: Mapped[list["AbsenceRequest"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    occurrences: Mapped[list["SessionOccurrence"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        group: Group,
        repeat_until: date,
        repeat_interval: int,
        title: str,
        description: str,
        start: datetime,
        end: datetime,
        max_students: int | None = None,
        properties: str | None = None,
    ):
        """Note: properties is json data"""
        self.repeat_until = repeat_until
        self.repeat_interval = repeat_interval
        self.title = title
        self.description = description
        self.start = start
        self.end = end
        self.max_students = max_students
        self.properties = properties

        self.group = group

    def __repr__(self) -> str:
        return f"<Session {self.id!r} (title: {self.title!r}, group_id: {self.group_id!r})>"


class SessionOccurrence(Base):
    __tablename__ = "session_occurrences"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    title: Mapped[str | None]
    description: Mapped[str | None]
    start: Mapped[datetime | None]
    end: Mapped[datetime | None]
    max_students: Mapped[int | None]
    properties: Mapped[str | None]  # JSON

    session: Mapped["Session"] = relationship(back_populates="occurrences")

    def __init__(
        self,
        title: str,
        description: str,
        start: datetime,
        end: datetime,
        max_students: int | None = None,
        properties: str | None = None,
    ):
        """Note: properties is json data"""
        self.title = title
        self.description = description
        self.start = start
        self.end = end
        self.max_students = max_students
        self.properties = properties

    def __repr__(self) -> str:
        return f"<SessionOccurence {self.id!r} (session id: {self.session_id!r})>"


class CancelledSession(Base):
    __tablename__ = "cancelled_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    start_date: Mapped[datetime | None]
    reason: Mapped[str | None] = mapped_column(String(256))

    def __init__(
        self,
        session: Session,
        start_date: datetime | None = None,
        reason: str | None = None,
    ):
        self.session_id = session.id
        self.start_date = start_date
        self.reason = reason

    def __repr__(self) -> str:
        return f"<CancelledSession {self.id!r} (session id: {self.session_id!r}, start_date: {self.start_date!r})>"


class AbsenceRequest(Base):
    __tablename__ = "absence_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    start_date: Mapped[datetime | None]
    reason: Mapped[str]
    status: Mapped[Request_Status] = mapped_column(default=Request_Status.PENDING)

    user: Mapped["User"] = relationship(back_populates="absence_requests")
    session: Mapped["Session"] = relationship(back_populates="absence_requests")

    def __init__(self, start_date: datetime, reason: str):
        self.start_date = start_date
        self.reason = reason

    def __repr__(self) -> str:
        return f"<AbsenceRequest {self.id!r} (session id: {self.session_id!r})>"


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[Question_Status] = mapped_column(default=Question_Status.OPEN)

    user: Mapped["User"] = relationship(back_populates="questions")
    group: Mapped["Group"] = relationship(back_populates="questions")

    def __init__(self, user, group, title: str, description: str):
        self.title = title
        self.description = description
        self.user = user
        self.group = group

    def __repr__(self) -> str:
        return f"<Question {self.id!r} (user id: {self.user_id!r})>"


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    title: Mapped[str]
    description: Mapped[str]

    def __init__(self, start_date: datetime, reason: str):
        self.start_date = start_date
        self.reason = reason

    def __repr__(self) -> str:
        return f"<Answer {self.id!r} (user id: {self.user_id!r})>"
