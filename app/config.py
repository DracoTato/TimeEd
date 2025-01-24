from os import getenv


class Config:
    SQLALCHEMY_DATABASE_URI = getenv("DATA_URI", "sqlite:///dev.db")
    SECRET_KEY = getenv("SECRET_KEY", "development")
