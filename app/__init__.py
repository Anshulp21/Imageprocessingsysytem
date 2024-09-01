import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_folders():
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    if not os.path.exists(Config.PROCESSED_FOLDER):
        os.makedirs(Config.PROCESSED_FOLDER)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    create_folders()

    from .routes.api import api_bp
    from .routes.webhook import webhook_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(webhook_bp, url_prefix='/webhook')

    return app
