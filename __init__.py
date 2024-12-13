from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    secrets_key = secrets.token_hex(16)

    app.config['SECRET_KEY'] = secrets
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://localhost:3360/touristattraction'

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app