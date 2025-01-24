from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Any
from .config import Config
from .models import Base
from .logging import setup_logging

db = SQLAlchemy(model_class=Base)


def create_app(config: Dict[Any, Any] = {}):
    app = Flask(__name__.split(".")[0])

    if config:
        app.config.from_mapping(config)  # Highest priority
    else:
        conf = Config()  # Init the object first
        app.config.from_object(conf)  # Load from file
    setup_logging(app)

    try:
        db.init_app(app)  # Load the DB
        with app.app_context():
            db.create_all()  # Create the DB tables
    except Exception as e:
        app.logger.error(e)

    @app.route("/", methods=["GET"])
    def landing_page():  # type: ignore (Pylance)
        app.logger.info("Landing Page accessed.")
        return render_template("landing_page.html")

    return app
