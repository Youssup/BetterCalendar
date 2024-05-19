from flask import Flask
from flask_cors import CORS

from .config import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])

    CORS(app)

    with app.app_context():
        from .routes import mainRoutes, authenticationRoutes
        app.register_blueprint(mainRoutes.mainBP)
        app.register_blueprint(authenticationRoutes.authBP)

    return app
