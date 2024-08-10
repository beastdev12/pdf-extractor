from flask import Flask
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()