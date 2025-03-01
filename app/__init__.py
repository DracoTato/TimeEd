from flask import Flask, render_template
from typing import Any
from .config import Config
from .logging import setup_logging
from .routes import blueprints
from .db import db
from .db.commands import register_commands  


def create_app(config: dict[str, Any] = {}):
    app = Flask(
        __name__.split(".")[0],
        static_folder="web/assets",
        template_folder="web/templates",
    )

    if config:
        app.config.from_mapping(config)  # Highest priority
    else:
        conf = Config()  # Init the object first
        app.config.from_object(conf)  # Load from file
    setup_logging(app)

    db.init_app(app)  # Register db w/ flask instance

    # Register blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
