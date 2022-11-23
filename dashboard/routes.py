from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user, login_user

from dashboard import db
from dashboard.forms import MainLoginForm, OrganizationRegisterForm, AddSensorForm
from dashboard.models import Organization, Sensor

dashboard = Blueprint('main', __name__, template_folder='templates')  # Instantiate the Blueprint object


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
        login_user(user)

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

        flash('Account has been registered successfully, please wait for approval!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register_org.html', form=register_form)


@dashboard.route('/dashboard')
@login_required
def dashboard_():
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
            organization_id=current_user.get_user_organisation(),
            address=sensor_form.address.data,
            city=sensor_form.city.data,
            region=sensor_form.region.data
        )

        db.session.add(new_sensor)
        db.session.commit()

        flash('Sensor has been added successfully!', 'success')
        return redirect(url_for('main.dashboard_'))

    return render_template('account.html', form=sensor_form)