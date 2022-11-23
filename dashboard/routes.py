from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user, login_user

from dashboard import db, login_manager
from dashboard.forms import MainLoginForm, OrganizationRegisterForm
from dashboard.models import Organization, User

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

    return render_template('login_copy.html', form=login_form)


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

    return render_template('register_copy.html', form=register_form)


@dashboard.route('/dashboard')
@login_required
def dashboard_():
    # print(current_user)
    return render_template('dashboard.html', user=current_user)


@dashboard.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.login'))
