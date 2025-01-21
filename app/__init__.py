from flask import Flask, render_template

def create_app():
    app = Flask(__name__.split('.')[0])

    @app.route('/', methods=["GET"])
    def landing_page():
        return render_template('landing_page.html')

    return app