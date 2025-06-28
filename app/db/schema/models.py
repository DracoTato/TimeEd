from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime

from . import enums
from .. import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    role: Mapped[enums.User_Type]
    status: Mapped[enums.Account_Status] = mapped_column(
        default=enums.Account_Status.UNVERIFIED
    )
    display_name: Mapped[str]
    birthdate: Mapped[date]
    gender: Mapped[enums.Gender]
    bio: Mapped[str | None]

    owned_groups: Mapped[list["Group"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    owned_sessions: Mapped[list["Session"]] = relationship(
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
        role: enums.User_Type,
        username: str,
        display_name: str,
        birthdate: date,
        gender: enums.Gender,
        bio: str | None = None,
    ):
        self.email = email
        self.role = role
        self.username = username
        self.display_name = display_name
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
    description: Mapped[str] = mapped_column(String(64))

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
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(64))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    rule: Mapped[str | None]
    max_students: Mapped[int | None]

    owner: Mapped["User"] = relationship(back_populates="owned_sessions")
    group: Mapped["Group"] = relationship(back_populates="sessions")
    absence_requests: Mapped[list["AbsenceRequest"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        owner: User,
        group: Group,
        title: str,
        description: str,
        start: datetime,
        end: datetime,
        rule: str | None = None,
        max_students: int | None = None,
    ):
        self.title = title
        self.description = description
        self.start_time = start
        self.end_time = end
        self.rule = rule
        self.max_students = max_students

        self.owner = owner
        self.group = group

    def __repr__(self) -> str:
        return f"<Session {self.id!r} (title: {self.title!r}, group_id: {self.group_id!r})>"


class AbsenceRequest(Base):
    __tablename__ = "absence_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    start_date: Mapped[datetime | None]
    reason: Mapped[str]
    status: Mapped[enums.Request_Status] = mapped_column(
        default=enums.Request_Status.PENDING
    )

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
    status: Mapped[enums.Question_Status] = mapped_column(
        default=enums.Question_Status.OPEN
    )

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
