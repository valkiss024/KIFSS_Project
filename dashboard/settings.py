import os

SECRET_KEY = os.environ.get('SECRET_KEY')  # Reading in the SECRET_KEY environmental variable

SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASK_ADMIN_SWATCH = 'cerulean'
