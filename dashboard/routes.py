import os

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user, login_user
from flask_mail import Message
from dashboard import db, login_manager, mail
from dashboard.forms import MainLoginForm, OrganizationRegisterForm, AddSensorForm
from dashboard.models import Organization, User, Sensor

import dashboard.inserts as ins

dashboard = Blueprint('main', __name__, template_folder='templates')  # Instantiate the Blueprint object


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.user_loader
def load_organization(organization_id):
    return Organization.query.get(int(organization_id))



# Define routes for the Dashboard


@dashboard.route('/', methods=['GET', 'POST'])
@dashboard.route('/login', methods=['GET', 'POST'])
def login():
    """
    View function to handle the logic behind logging users / organizations in, defaults to both '/' and '/login'
    endpoints
    """
    login_form = MainLoginForm()
    if login_form.validate_on_submit():
        user = login_form.get_user()
        print(login_user(user, remember=True))
        print(current_user)

        return redirect(url_for('main.dashboard_'))

    return render_template('login.html', form=login_form)


@dashboard.route('/register', methods=['GET', 'POST'])
def register():
    """
    View function to handle the logic behind creating new organizations
    """
    register_form = OrganizationRegisterForm()
    if register_form.validate_on_submit():
        new_organization = Organization(
            name=register_form.name.data,
            email=register_form.email.data,
            country=register_form.country.data,
            postcode=register_form.postcode.data
        )

        new_organization.create_password_hash(register_form.password.data)

        db.session.add(new_organization)
        db.session.commit()

        # print(os.environ.get('MAIL_USERNAME'))

        msg = Message(
            'New Registration Request!',
            sender=os.environ.get('MAIL_USERNAME'),
            recipients=[os.environ.get('MAIL_USERNAME')]
        )
        msg.body = f'A new organization - {new_organization.name} - has registered! Go to the Admin dashboard to approve it!'
        # mail.send(msg)

        flash('Account has been registered successfully, please wait for approval!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=register_form)


@dashboard.route('/dashboard')
@login_required
def dashboard_():
    # print(current_user
    ins.add_example_sensors(current_user.get_organization())
    ins.json_to_sql()
    return render_template('dashboard.html', user=current_user)


@dashboard.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.login'))


@dashboard.route('/addsensor', methods=['GET', 'POST'])
@login_required
def addsensor():
    """
    View function to handle the logic behind creating new sensors
    """
    sensor_form = AddSensorForm()

    # TODO: Find library for address to coords conversion
    # get latitude
    # get longitude

    if sensor_form.validate_on_submit():
        new_sensor = Sensor(
            serial_number=sensor_form.serial_number.data,
            organization_id=current_user.get_user_organization(),
            address=sensor_form.address.data,
            city=sensor_form.city.data,
            region=sensor_form.region.data
        )

        db.session.add(new_sensor)
        db.session.commit()

        flash('Sensor has been added successfully!', 'success')
        return redirect(url_for('main.dashboard_'))

    return render_template('account.html', form=sensor_form)