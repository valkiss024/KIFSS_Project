from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, TelField, BooleanField
from wtforms.validators import InputRequired, Email, Length, ValidationError, StopValidation

from dashboard.models import Organization, User, AdminUser, Sensor
from dashboard._utils import generate_password


# Registration Forms:

class RegisterForm(FlaskForm):
    """
    The Base Registration Form - defines basic form fields and validation methods use across different registration
    forms on the site
    """

    email = EmailField(label='Email Address:', validators=[InputRequired(), Email(), Length(max=120)])
    password = PasswordField(label='Password:', validators=[InputRequired(), Length(min=8, max=40)])
    confirm_password = PasswordField(label='Confirm Password:', validators=[InputRequired(), Length(min=8, max=40)])
    submit = SubmitField(label='Register', render_kw={'style': 'text-center'})

    def validate_confirm_password(self, confirm_password):
        """Method for validating password match"""
        if confirm_password.data != self.password.data:
            raise ValidationError('Passwords must match!')


class RegisterOrganizationForm(RegisterForm):
    """
    The Organization Registration form - derived from the Registration Form, used to get the data required to
    create a new Organization object in the Database
    """

    name = StringField(label='Organisation Name:', validators=[InputRequired(), Length(min=2, max=50)])
    country = StringField(label='Country:', validators=[InputRequired(), Length(max=40)])
    postcode = StringField(label='Postcode:', validators=[InputRequired(), Length(max=9)])

    def validate_email(self, email):
        """Method to validate whether an Organization with the email already exists"""
        if Organization.query.filter_by(email=email.data).first():
            raise ValidationError('An Organization with this email already exists!')

    def validate_name(self, name):
        """Method to validate whether an Organization with the name already exists"""
        if Organization.query.filter_by(name=name.data).first():
            raise ValidationError('An Organization with this name already exists!')


class AddUserForm(FlaskForm):
    """
    The User Registration form - derived from the Registration Form, used to get the data required to create a new
    User object in the Database
    """

    email = EmailField(label='Email Address:', validators=[InputRequired(), Email(), Length(max=120)])
    first_name = StringField(label='First Name:', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField(label='Last Name:', validators=[InputRequired(), Length(min=2, max=50)])
    contact_number = TelField(label='Contact Number:', validators=[Length(max=13)])
    password = StringField(label='Password:', default=generate_password(8),
                           render_kw={'disabled': ""})
    submit = SubmitField(label='Add User', render_kw={'style': 'text-center'})

    def validate_email(self, email):
        """Method to validate whether a User with the email already exists"""
        # TODO: This would only allow a user to be part of only one Organization
        # Do a query on the endpoint for Organization specific search to check for only current Organization
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('A User with this email already exists')


class AddSensorForm(FlaskForm):
    """
    The Add Sensor form -  derived from the Registration Form, used to get the data to create a new Sensor object in the
    Database
    """

    serial_number = StringField(label='Serial Number:', validators=[InputRequired(), Length(min=2, max=10)])
    name = StringField(label='Name:', validators=[InputRequired(), Length(min=2, max=50)])
    address = StringField(label='Address Line 1:', validators=[InputRequired(), Length(max=70)])
    city = StringField(label='City:', validators=[InputRequired(), Length(max=30)])
    region = StringField(label='Region:', validators=[InputRequired(), Length(max=30)])
    submit = SubmitField(label='Add Sensor', render_kw={'style': 'text-center'})

    def validate_serial_number(self, serial_number):
        """Method to validate whether a Sensor with the serial number already exists"""
        if Sensor.query.filter_by(serial_number=serial_number.data).first():
            raise ValidationError('A Sensor with this serial number already exists')


# Login Forms:

class BaseLoginForm(FlaskForm):
    """
    The Base Login Form - defines basic form fields and validation methods use across different login forms on the site
    """

    email = EmailField(validators=[InputRequired(), Email(), Length(max=120)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=40)])
    submit = SubmitField('Login')

    def _validate_password(self, password, user):
        """Method to match the password provided against the password hash stored in the Database"""
        if not user.validate_password_hash(password=password):
            raise ValidationError('Incorrect password!')


class MainLoginForm(BaseLoginForm):
    """
    The Main Login Form - derived from the Base Login Form, used on the '/' and '/login' routes to validate and log in
    users or organizations
    """

    is_organization = BooleanField(label='I am an organization')

    def validate_email(self, email):
        """Main validation method - checks if the user exists, call the password validator then in case if the user is
        an organization then checks whether they have been approved"""

        user = self.get_user()
        if not user:
            raise StopValidation(f'No profile associated with {email.data} was found!')
        self._validate_password(password=self.password.data, user=user)
        if hasattr(user, 'is_approved'):
            if not user.is_approved:
                raise ValidationError(f'Registration request has not been approved yet!')

    def get_user(self):
        if not self.is_organization.data:
            return User.query.filter_by(email=self.email.data).first()
        return Organization.query.filter_by(email=self.email.data).first()


class AdminLoginForm(BaseLoginForm):
    """
    The Admin Login Form - derived from the Base Login Form and used on the Flask Admin site to log users in with
    Admin privileges
    """

    def validate_email(self, email):
        admin_user = self.get_user()
        if not admin_user:
            raise StopValidation(f'No admin profile associated with {email.data} was found!')

    def get_user(self):
        return AdminUser.query.filter_by(email=self.email.data).first()


# Reset password form
class ResetPasswordForm(FlaskForm):
    """
    The Reset Password Form - derived from the Flask Form and used to get data to update a User's password
    """

    old_password = PasswordField(validators=[InputRequired(), Length(min=8, max=40)])
    new_password = PasswordField(validators=[InputRequired(), Length(min=8, max=40)])
    new_password_confirm = PasswordField(validators=[InputRequired(), Length(min=8, max=40)])
    submit = SubmitField(label='Reset', render_kw={'style': 'text-center'})

    def __init__(self, user_class, user):
        super().__init__()
        self.__user_class = user_class
        self.__user = user

    def validate_new_password(self, new_password):
        if new_password.data == self.old_password.data:
            raise ValidationError('New password must differ from old password!')

    def validate_new_password_confirm(self, new_password_confirm):
        """Method for validating password match"""
        if new_password_confirm.data != self.new_password.data:
            raise ValidationError('New passwords must match!')

    def validate_old_password(self, old_password):
        user = self._get_user()
        if not user.validate_password_hash(old_password.data):
            raise ValidationError('Incorrect old password')

    def _get_user(self):
        if self.__user_class == 'Organization':
            return Organization.query.filter_by(id=self.__user.id).first()
        else:
            return User.query.filter_by(id=self.__user.id).first()

