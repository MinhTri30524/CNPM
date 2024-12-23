from flask import redirect
from flask_admin import Admin, AdminIndexView
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user

from app import db, app
from app.dao import course_report, get_class, get_classes_info
from app.models import HocSinh, UserRole, LopHoc


class MyAdminIndexView(AdminIndexView):
	@expose("/")
	def index(self):
		course = 'Toán'
		year = '2023-2024'
		semester = 'Học kỳ 1'
		stats = course_report(course, year, semester)

		return self.render(
			'admin/index.html',
			stats=stats,
			course=course,
			year=year,
			semester=semester
		)


admin = Admin(app, name='Administration', template_mode='bootstrap4', index_view=MyAdminIndexView())


class AuthenticatedView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class MyView(BaseView):
	def is_accessible(self):
		return current_user.is_authenticated


# class ClassView(MyView):
# 	@expose("/")
# 	def index(self):
# 		classes = get_classes_info()
# 		return self.render('admin/class.html', classes=classes)


class ClassView(AuthenticatedView):
	can_export = True
	column_searchable_list = ['ma_lop', 'ten']
	column_filters = ['ma_lop', 'ten']
	can_view_details = True
	column_list = ['ma_lop', 'ten', 'so_luong']


class CourseOutlineView(AuthenticatedView):
	can_export = True
	column_searchable_list = ['ma_lop', 'ten']
	column_filters = ['ma_lop', 'ten']
	can_view_details = True
	column_list = ['ma_lop', 'ten', 'so_luong']


class LogoutView(MyView):
	@expose("/")
	def index(self):
		logout_user()
		return redirect('/admin')


class StatsView(MyView):
	@expose("/")
	def index(self):
		return self.render('admin/stats.html')


admin.add_view(ClassView(name='Danh sách lớp', model=LopHoc, session=db.session))
admin.add_view(LogoutView(name='Đăng xuất'))
