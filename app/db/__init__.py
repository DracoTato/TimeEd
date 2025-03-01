from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime


class Base(DeclarativeBase):
    __abstract__ = True  # Don't create table

    # Global columns for all tables
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    deleted_at: Mapped[datetime | None]


db = SQLAlchemy(model_class=Base)