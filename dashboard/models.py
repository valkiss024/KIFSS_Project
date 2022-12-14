from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


# Define models --> tables in the DB

class User(db.Model, UserMixin):
    """
    The User model, defines a User object in the Database
    """

    # noinspection SpellCheckingInspection
    __tablename__ = 'user'

    # Define User table columns:
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)
    password = db.Column(db.String(120), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id', ondelete='CASCADE'), nullable=False)

    organization = relationship('Organization', backref='users')

    def __init__(self, first_name, last_name, email, contact_number, organization_id):
        """Class constructor"""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact_number = contact_number
        self.organization_id = organization_id

    def __repr__(self):
        """Object representation for debugging and read queries"""
        return f'User({self.first_name}, {self.last_name}, {self.email}, {self.contact_number})'

    def create_password_hash(self, password):
        """Method to encrypt password provided by the user"""
        self.password = generate_password_hash(password=password)

    def validate_password_hash(self, password):
        """Method to decrypt stored password hash and compare it against password provided"""
        return check_password_hash(pwhash=self.password, password=password)

    def get_organization_id(self):
        return self.organization_id


class Organization(db.Model, UserMixin):
    """
    The Organization model, defines an Organization object in the Database
    """

    # noinspection SpellCheckingInspection
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    country = db.Column(db.String(40), nullable=False)
    postcode = db.Column(db.String(9), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, name, email, country, postcode):
        """Class constructor"""
        self.name = name
        self.email = email
        self.country = country
        self.postcode = postcode
        # For all newly created Organizations the 'is_approved' flag defaults to False until further approval by Alex
        self.is_approved = False

    def __repr__(self):
        """Object representation for debugging and read queries"""
        return f'Organization({self.name}, {self.email}, {self.country}, {self.postcode}, {self.is_approved})'

    def create_password_hash(self, password):
        """Method to encrypt password provided by the user"""
        self.password = generate_password_hash(password=password)

    def validate_password_hash(self, password):
        """Method to decrypt stored password hash and compare it against password provided"""
        return check_password_hash(pwhash=self.password, password=password)

    def get_organization_id(self):
        return self.id


class Sensor(db.Model):
    """
    The Sensor model, defines a Sensor object in the Database
    """

    # noinspection SpellCheckingInspection
    __tablename__ = 'sensor'

    serial_number = db.Column(db.String(10), primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    # TODO: Implement what happens to the Sensor if either of the Foreign Keys get deleted
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)

    organization = relationship('Organization', backref='sensors')

    def __init__(self, serial_number, name, organization_id, address, city, region, latitude, longitude):
        """Class constructor"""
        self.serial_number = serial_number
        self.name = name
        self.organization_id = organization_id
        self.address = address
        self.city = city
        self.region = region
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        """Object representation for debugging and read queries"""
        return f'Device({self.serial_number}, {self.name}, {self.organization.name}, {self.address}, {self.city}, {self.region}, {self.latitude}, {self.longitude})'


class SelfCheck(db.Model):
    """
    The SelfCheck model, defines a SelfCheck object in the Database
    """

    # noinspection SpellCheckingInspection
    __tablename__ = 'selfcheck'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(10), db.ForeignKey('sensor.serial_number'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    assessed = db.Column(db.Boolean, nullable=False)

    sensor = relationship('Sensor', backref='selfchecks')

    def __init__(self, serial_number, status, date, assessed):
        """Class constructor"""
        self.serial_number = serial_number
        self.status = status
        self.date = date
        self.assessed = assessed

    def __repr__(self):
        """Object representation for debugging and read queries"""
        return f'SelfCheck({self.sensor.serial_number}, {self.status}, {self.date}, {self.assessed})'


class Trigger(db.Model):
    """
    The Trigger model, defines a Trigger object in the Database
    """

    # noinspection SpellCheckingInspection
    __tablename__ = 'trigger'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(10), db.ForeignKey('sensor.serial_number'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    assessed = db.Column(db.Boolean, nullable=False)

    sensor = relationship('Sensor', backref='triggers')

    def __init__(self, serial_number, status, date, assessed):
        """Class constructor"""
        self.serial_number = serial_number
        self.status = status
        self.date = date
        self.assessed = assessed

    def __repr__(self):
        """Object representation for debugging and read queries"""
        return f'Trigger({self.sensor.serial_number}, {self.status}, {self.date}. {self.assessed})'


class AdminUser(db.Model, UserMixin):
    """
    The AdminUser model, defines a User in the Database who is an Admin to the site
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, email, password):
        """Class constructor"""
        self.email = email
        self.create_password_hash(password=password)
        self.is_admin = True

    def create_password_hash(self, password):
        """Method to encrypt password provided by the user"""
        self.password = generate_password_hash(password=password)

    def validate_password_hash(self, password):
        """Method to decrypt stored password hash and compare it against password provided"""
        return check_password_hash(pwhash=self.password, password=password)
