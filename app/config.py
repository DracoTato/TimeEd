import os
from secrets import token_hex
from datetime import timedelta


class Config:
    """Base Config"""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATA_URI", "sqlite:///timeed.db")
    SECRET_KEY = os.getenv("SECRET_KEY", token_hex(32))
    SQLALCHEMY_TRACK_MODIFICATION = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)

    DEBUG = False
    TESTING = False

    def __init__(self, prefixes: list[str] = ["LOG_"]):
        """Add env variables starting with `prefixes` as attributes.

        Note: Please add an underscore after to prevent catching compound words, e.g. LOGGER_SMTH
        Default: ["LOG_"]
        """
        matching_vars = {
            key: value
            for key, value in os.environ.items()
            if any(key.startswith(prefix) for prefix in prefixes)
        }  # Check if key starts with any of the prefixes

        for key, value in matching_vars.items():
            if not hasattr(self, key):
                setattr(self, key, value)


class DevelopmentConfig(Config):
    """Development Config"""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATA_URI", "sqlite:///dev.db")
    DEBUG = True


class ProductionConfig(Config):
    """Production Config"""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATA_URI", "sqlite:///production.db")
    DEBUG = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "strict"


class TestConfig(Config):
    """Test Config"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    WTF_CSRF_ENABLED = False


config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestConfig,
}
