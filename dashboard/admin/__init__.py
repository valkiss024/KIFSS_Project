from sqlalchemy import event
from werkzeug.security import generate_password_hash

from dashboard import admin_site, db
from dashboard.admin.views import CustomAdminIndexView, CustomModelView, ModelView, CustomUserModelView
from dashboard.models import User, Organization, Sensor, AdminUser


def setup_admin():
    # noinspection SpellCheckingInspection
    admin_site.name = 'KIFSS Admin'
    admin_site.template_mode = 'bootstrap4'

    admin_site.add_view(ModelView(User, db.session))
    admin_site.add_view(ModelView(Organization, db.session))
    admin_site.add_view(ModelView(Sensor, db.session))
    admin_site.add_view(ModelView(AdminUser, db.session))
