from flask import Flask

from .extensions import db, login_manager, admin_site, mail
from .models import User, Organization, Sensor
from .routes import dashboard
from .admin import setup_admin, CustomAdminIndexView
import dashboard.inserts as ins


def create_app(config_file='./settings.py'):
    app = Flask(__name__)  # Instantiate a Flask object

    app.config.from_pyfile(config_file)  # Apply configuration to the application

    db.init_app(app)
    with app.app_context():
        # db.drop_all()
        db.create_all()
        db.session.commit()
        # ins.json_to_sql()

    mail.init_app(app)

    app.register_blueprint(dashboard)  # Register the Blueprint to access routes

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'error'

    admin_site.init_app(app, index_view=CustomAdminIndexView())
    setup_admin()

    return app
