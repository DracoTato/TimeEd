from .auth import auth_bp

# list of blueprints to be registered in app/__init__.py
BLUEPRINTS = [auth_bp]

def register_blueprints(app):
    """Register blueprints with a flask instance"""
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)
