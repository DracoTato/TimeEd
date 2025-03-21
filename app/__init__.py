from flask import Flask, redirect, url_for
from typing import Any
from os import getenv
from .config import config_dict
from .logging import setup_logging
from .routes import register_blueprints
from .db import db
from .db.commands import register_commands


def create_app(config: dict[str, Any] = {}):
    app = Flask(
        __name__.split(".")[0],
        static_folder="web/assets",
        template_folder="web/templates",
    )

    config_env = config.get("ENV", None)
    env = config_env if config_env else getenv("FLASK_ENV", "production")

    conf = config_dict[env]

    app.config.from_object(conf)
    app.config.update(config)  # Highest priority

    setup_logging(app)

    db.init_app(app)  # Register db w/ flask instance

    register_blueprints(app)
    register_commands(app)

    @app.route("/")
    def index():
        return redirect(url_for("auth.register"))

    return app
