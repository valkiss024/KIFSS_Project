from flask import redirect, url_for, flash
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from wtforms import PasswordField
from wtforms.validators import InputRequired

from dashboard.forms import AdminLoginForm
from dashboard.models import AdminUser


class CustomAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not isinstance(current_user, AdminUser):
            flash('Please log in with an Admin account to access administrative functionalities!')
            return redirect(url_for('.admin_login'))
        return super(CustomAdminIndexView, self).index()

    @expose('/login/', methods=['GET', 'POST'])
    def admin_login(self):
        form = AdminLoginForm()
        if form.validate_on_submit():
            admin_user = form.get_user()
            login_user(admin_user)

            return super(CustomAdminIndexView, self).index()

        return self.render('admin/admin_login.html', form=form)

    @expose('/logout/')
    def admin_logout(self):
        logout_user()
        return redirect(url_for('.admin_login'))


class CustomPasswordField(PasswordField):

    def populate_obj(self, obj, name):
        setattr(obj, name, generate_password_hash(self.data))


class CustomModelView(ModelView):
    pass
    #def is_accessible(self):
    #    return isinstance(current_user, AdminUser)


class CustomUserModelView(CustomModelView):
    form_extra_fields = {
        'password': CustomPasswordField('Password', validators=[InputRequired()])
    }

    #def is_accessible(self):
    #    return isinstance(current_user, AdminUser)
