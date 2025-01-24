from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from enum import Enum
from datetime import datetime
from typing import Optional, List
from app.db import Base


class User_Types(Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    ADMIN = "admin"


class Gender(Enum):
    MALE = 0
    FEMALE = 1


class SessionFreq(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class User(Base):
    """"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    role: Mapped[User_Types]
    full_name: Mapped[Optional[str]]
    birthdate: Mapped[Optional[datetime]]
    gender: Mapped[Optional[Gender]]
    bio: Mapped[Optional[str]]

    owned_groups: Mapped[List["Group"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    enrolled_groups: Mapped[List["Enroll"]] = relationship(back_populates="user")

    def set_password(self, value: str):
        """Store the password as a hash."""
        self.password_hash = generate_password_hash(value)

    password = property(fset=set_password) # Enables User.password = "..."

    def check_password(self, value: str):
        """Check the given password against the stored hash."""
        return check_password_hash(self.password_hash, value)

    def __repr__(self) -> str:
        return f"<User(id: {self.id!r}, email: {self.email!r}, owned groups: {self.owned_groups!r}, enrolled groups: {self.enrolled_groups!r})>"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(256))

    owner: Mapped["User"] = relationship(back_populates="owned_groups")
    enrolls: Mapped[List["Enroll"]] = relationship(back_populates="group")
    sessions: Mapped[List["Session"]] = relationship(back_populates="group")

    def __repr__(self):
        return f"<Group(id: {self.id!r}, owner id: {self.owner.id!r}, owner email: {self.owner.email!r}, title: {self.title!r}, enrolled_students: {self.enrolls!r}, sessions: {self.sessions!r})>"


class Enroll(Base):
    __tablename__ = "enrolls"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    user: Mapped["User"] = relationship(back_populates="enrolled_groups")
    group: Mapped["Group"] = relationship(back_populates="enrolls")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[Optional[str]] = mapped_column(String(256))
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    max_students: Mapped[Optional[int]]
    frequency: Mapped[Optional[SessionFreq]]
    repeat_until: Mapped[Optional[datetime]]
    deleted_at: Mapped[Optional[datetime]]

    group: Mapped["Group"] = relationship(back_populates="sessions")


class CancelledSession(Base):
    __tablename__ = "cancelled_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    start_date: Mapped[datetime]
    reason: Mapped[Optional[str]] = mapped_column(String(256))
