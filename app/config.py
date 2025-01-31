from os import getenv, environ


class Config:
    SQLALCHEMY_DATABASE_URI = getenv("DATA_URI", "sqlite:///dev.db")
    SECRET_KEY = getenv("SECRET_KEY", "development")

    def __init__(self, prefixes: list[str] = ["LOG_"]):
        """Add env variables starting with `prefixes` as attributes.

        Note: Please add an underscore after to prevent catching compound words, e.g. LOGGER_SMTH
        Default: ["LOG_"]
        """
        matching_vars = {
            key: value
            for key, value in environ.items()
            if any(key.startswith(prefix) for prefix in prefixes)
        }  # Check if key starts with any of the prefixes

        for key, value in matching_vars.items():
            if not hasattr(self, key):
                setattr(self, key, value)
