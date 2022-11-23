import os

SECRET_KEY = 'secret'  # Reading in the SECRET_KEY environmental variable

# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/kifss'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASK_ADMIN_SWATCH = 'cerulean'