import os

SECRET_KEY = 'my secret'  # Reading in the SECRET_KEY environmental variable

# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/kifss'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Admin site configuration
FLASK_ADMIN_SWATCH = 'cerulean'

# Flask-Mail configuration
MAIL_SERVER = 'smtp.office365.com'
MAIL_PORT = 587
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USE_TLS = True
MAIL_USE_SSL = False
