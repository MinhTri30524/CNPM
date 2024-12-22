from app import db, app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask_admin import BaseView, expose
from flask import redirect
from app.models import HocSinh, NhanVien, UserRole

admin = Admin(app, name='Administration', template_mode='bootstrap4')


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class CategoryView(AuthenticatedView):
    can_export = True
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name']
    can_view_details = True
    column_list = ['name', 'products']


class StudentView(AuthenticatedView):
    can_export = True
    column_searchable_list = ['ma_hoc_sinh', 'ma_hoc_sinh']
    column_filters = ['ma_hoc_sinh', 'ho_ten']
    can_view_details = True
    column_list = ['ma_hoc_sinh', 'ho_ten', 'ngay_sinh', 'std']


class MyView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(MyView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(MyView):
    @expose("/")
    def index(self):

        return self.render('admin/stats.html')


admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
admin.add_view(StudentView(HocSinh, db.session))
