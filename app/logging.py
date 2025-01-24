import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
import os
from sys import stdout
from flask.logging import default_handler


def setup_logging(app):
    """### Description:
    Add a RotatingFile handler and a Stream handler to the application and remove the default handler.

    ### List of config variables (app.config):
    `LOG_FOLDER`: Specify the folder in which to write the logs (default='logs').
    `LOG_LEVEL`: Set the RotatingFile handler log level (default=INFO), Stream handler is filtered to only DEBUG log levels.
    `LOG_MAX_BYTES` Set the logs max size in bytes (default=1_000_000, i.e. 1MB).
    `LOG_BACKUP` Set the logs max file numbers, e.g. starts at 1 and ends at `LOG_BACKUP`, and then
    removes the oldest log and starts over (default=10, i.e. total log size = 1MB*10 = 10MB).
    """
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] in (%(pathname)s:%(lineno)s): %(message)s"
    )

    conf = app.config

    log_folder = conf.get("LOG_FOLDER", "logs")
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, "timeed.log")

    log_level = conf.get("LOG_LEVEL", logging.INFO)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=conf.get("LOG_MAX_BYTES", 1_000_000),
        backupCount=conf.get("LOG_BACKUP", 10),
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(ProductionFilter())

    stream_handler = StreamHandler(stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(DebugFilter())

    if default_handler in app.logger.handlers:
        app.logger.removeHandler(default_handler)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)


class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG


class ProductionFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.DEBUG
