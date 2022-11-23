import os

SECRET_KEY = os.environ.get('SECRET_KEY')  # Reading in the SECRET_KEY environmental variable

<<<<<<< HEAD
# Database configuration
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/kifss'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
=======
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/kifss'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
>>>>>>> 301637f452394d518dcc9fd665e4d68f2103a73d
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Admin site configuration
FLASK_ADMIN_SWATCH = 'cerulean'

# Flask-Mail configuration
MAIL_SERVER = 'smtp.office365.com'
MAIL_PORT = 465
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USE_TLS = False
MAIL_USE_SSL = True
