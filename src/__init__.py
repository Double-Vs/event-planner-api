import os
from flask import Flask
from flask_migrate import Migrate
from .models import db

from .api.hosts import bp as hosts_bp
from .api.guests import bp as guests_bp
from .api.vendors import bp as vendors_bp
from .api.events import bp as events_bp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres@localhost:5432/event_planner_db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)

    else:
        app.config.from_mapping(test_config)


    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(hosts_bp)
    app.register_blueprint(guests_bp)
    app.register_blueprint(vendors_bp)
    app.register_blueprint(events_bp)

    return app
