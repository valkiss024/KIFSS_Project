import os, json

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user, login_user
from dashboard import db, login_manager
from dashboard.forms import MainLoginForm, RegisterOrganizationForm, AddSensorForm, AddUserForm, ResetPasswordForm
from dashboard.models import Organization, User, Sensor
from dashboard._utils import json_to_sql, add_example_sensors, get_sensors, get_self_checks, get_triggers, send_notification

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
        print(login_user(user))
        print(current_user)

        return redirect(url_for('main.dashboard_'))

    return render_template('login.html', form=login_form)


@dashboard.route('/register', methods=['GET', 'POST'])
def register():
    """
    View function to handle the logic behind creating new organizations
    """
    register_form = RegisterOrganizationForm()
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

        recipient = os.environ.get('MAIL_USERNAME')
        subject = 'New Registration Request'
        body = f'A new organization - {new_organization.name} - has registered! Go to the Admin dashboard to approve it!'

        # send_notification([recipient], subject, body)

        flash('Account has been registered successfully, please wait for approval!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=register_form)


@dashboard.route('/dashboard')
@login_required
def dashboard_():
    print(current_user)
    add_example_sensors(current_user.get_organization_id())
    json_to_sql()
    data = get_sensors(current_user.get_organization_id())
    print(json.dumps(data))
    return render_template('dashboard.html', user=current_user, data=json.dumps(data))


@dashboard.route('/devices')
@login_required
def devices():

    selfchecks = get_self_checks(current_user.get_organization_id())
    d = {}
    for i in selfchecks["selfchecks"]:
        key = i["serial_number"]
        if key not in d.keys():
            d[key] = []
            
        d[key].append(i)

    # triggers = get_triggers(current_user.get_organization_id())
    # c = {}
    # for i in triggers["triggers"]:
    #     key = i["serial_number"]
    #     if key not in c.keys():
    #         c[key] = []
            
    #     c[key].append(i)

    return render_template('devices.html', selfchecks=json.dumps(d))


@dashboard.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html')


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


@dashboard.route('/adduser', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            contact_number=form.contact_number.data,
            organization_id=current_user.id
        )
        new_user.create_password_hash(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        recipient = new_user.email
        subject = "Account Created Successfully"
        body = f'Dear {new_user.last_name}, your automatically generated password for login: {form.password.data}!'

        # send_notification([recipient], subject, body)

        flash('New user added successfully! An email notification has been sent out!')
        return redirect(url_for('main.dashboard_'))

    return render_template('add_user.html', form=form)


@dashboard.route('/resetpassword', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm(current_user.__class__.__name__, current_user)
    if form.validate_on_submit():
        current_user.create_password_hash(form.new_password.data)

        db.session.merge(current_user)
        db.session.commit()

        logout_user()
        flash('Password updated successfully! Please log in again!')
        return redirect(url_for('main.login'))

    return render_template('reset_pass.html', form=form)
