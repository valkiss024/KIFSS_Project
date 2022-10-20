from sqlalchemy import event
from werkzeug.security import generate_password_hash

from dashboard import admin_site, db
from dashboard.admin.views import CustomAdminIndexView, CustomModelView
from dashboard.models import User, Organization, Sensor, AdminUser


def setup_admin():
    # noinspection SpellCheckingInspection
    admin_site.name = 'KIFSS Admin'
    admin_site.template_mode = 'bootstrap4'

    admin_site.add_view(CustomModelView(User, db.session))
    admin_site.add_view(CustomModelView(Organization, db.session))
    admin_site.add_view(CustomModelView(Sensor, db.session))
    admin_site.add_view(CustomModelView(AdminUser, db.session))

    @event.listens_for(User.password, 'set', retval=True)
    def hash_user_password(target, value, oldvalue, initiator):
        if value != oldvalue:
            return generate_password_hash(value)
        return value

    @event.listens_for(Organization.password, 'set', retval=True)
    def hash_user_password(target, value, oldvalue, initiator):
        if value != oldvalue:
            return generate_password_hash(value)
        return value

    @event.listens_for(AdminUser.password, 'set', retval=True)
    def hash_user_password(target, value, oldvalue, initiator):
        if value != oldvalue:
            return generate_password_hash(value)
        return value
