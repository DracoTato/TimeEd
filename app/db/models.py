from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from enum import Enum
from datetime import date, datetime
from . import Base


class User_Type(Enum):
    _SUPER_ADMIN = 0  # Restricted type
    _ADMIN = 1  # Restricted type
    TEACHER = 2
    STUDENT = 3


class Gender(Enum):
    MALE = 0
    FEMALE = 1


class SessionFreq(Enum):
    DAILY = 0
    WEEKLY = 1
    MONTHLY = 2


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    role: Mapped[int] # User_Type.value
    full_name: Mapped[str]
    birthdate: Mapped[date]
    gender: Mapped[int] # Gender.value
    bio: Mapped[str | None]

    owned_groups: Mapped[list["Group"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    enrolled_groups: Mapped[list["Enroll"]] = relationship(back_populates="user")

    def __set_password__(self, value: str):
        """Store the password as a hash.
        Note: Use `create` instead of directly using this method!
        """
        self.password_hash = generate_password_hash(value)

    def check_password(self, value: str):
        """Check the given password against the stored hash."""
        return check_password_hash(self.password_hash, value)

    @classmethod
    def create(
        cls,
        email: str,
        password: str,
        role: User_Type,
        full_name: str,
        birthdate: date,
        gender: Gender,
        bio: str | None = None,
    ):
        """Return a new instance of `User`."""
        try:
            user = cls(
                email=email,
                role=role.value,
                full_name=full_name,
                birthdate=birthdate,
                gender=gender.value,
                bio=bio,
            )
            user.__set_password__(password)
            return user
        except Exception as e:
            raise e

    def __repr__(self) -> str:
        return f"<User {self.id!r} (email: {self.email!r}, role: {self.role!r})>"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(256))

    owner: Mapped["User"] = relationship(back_populates="owned_groups")
    enrolls: Mapped[list["Enroll"]] = relationship(back_populates="group")
    sessions: Mapped[list["Session"]] = relationship(back_populates="group")

    @classmethod
    def create(cls, owner: User, title: str, description: str):
        """Return a new instance of `Group`."""
        try:
            group = cls(title=title, description=description)
            group.owner = owner
            return group
        except Exception as e:
            raise e

    def __repr__(self) -> str:
        return f"<Group {self.id!r} (title: {self.title!r}, owner: {self.owner!r})>"


class Enroll(Base):
    __tablename__ = "enrolls"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    user: Mapped["User"] = relationship(back_populates="enrolled_groups")
    group: Mapped["Group"] = relationship(back_populates="enrolls")

    @classmethod
    def create(cls, user: User, group: Group):
        """Return a new instance of `Enroll`."""
        try:
            enroll = cls()
            enroll.user = user
            enroll.group = group
            return enroll
        except Exception as e:
            raise e

    def __repr__(self) -> str:
        return f"<Enroll {self.id!r} (user: {self.user!r}, group: {self.group!r})>"


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str | None] = mapped_column(String(256))
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    max_students: Mapped[int | None]
    frequency: Mapped[SessionFreq | None]
    repeat_until: Mapped[date | None]

    group: Mapped["Group"] = relationship(back_populates="sessions")

    @classmethod
    def create(
        cls,
        group: Group,
        title: str,
        description: str,
        start_date: datetime,
        end_date: datetime,
        max_students: int | None = None,
        freqeuncy: SessionFreq | None = None,
        repeat_until: date | None = None,
    ):
        """Return a new instance of `Session`."""
        try:
            session = cls(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                max_students=max_students,
                freqeuncy=freqeuncy,
                repeat_until=repeat_until,
            )
            session.group = group
        except Exception as e:
            raise e

    def __repr__(self) -> str:
        return f"<Session {self.id!r} (title: {self.title!r}, group: {self.group!r})>"


class CancelledSession(Base):
    __tablename__ = "cancelled_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    start_date: Mapped[datetime]
    reason: Mapped[str | None] = mapped_column(String(256))

    @classmethod
    def create(
        cls,
        session: Session,
        start_date: datetime | None = None,
        reason: str | None = None,
    ):
        """Return a new instance of `CancelledSession`."""
        try:
            return CancelledSession(
                session_id=session.id, start_date=start_date, reason=reason
            )
        except Exception as e:
            raise e

    def __repr__(self) -> str:
        return f"<CancelledSession {self.id!r} (session id: {self.session_id!r}, start_date: {self.start_date!r})>"
