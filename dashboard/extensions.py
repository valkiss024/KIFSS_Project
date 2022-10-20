from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Instantiate the DB object
login_manager = LoginManager()
admin_site = Admin()
