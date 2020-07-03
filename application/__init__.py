from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
oauth = OAuth()


def create_app():  # Initialise app
    """Construct the core application. """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    oauth.init_app(app)
    db.init_app(app)
    with app.app_context():
        from . import routes  # import routes
        db.create_all()  # Create sql tables for our data models
        CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
        oauth.register(
            name='google',
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        return app
