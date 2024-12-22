import math
from flask import render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user
from app import app, login
from app import dao, utils
from app.dao import course_report
from app.models import UserRole


# from app.models import UserRole


# Trang chủ
@app.route("/")
def index():
	return render_template('index.html')


# Load trang login
@app.route("/login", methods=['get', 'post'])
def login_process():
	if request.method.__eq__('POST'):
		username = request.form.get('username')
		password = request.form.get('password')
		u = dao.auth_user(username=username, password=password)
		if u:
			login_user(u)
			return redirect('/')
	return render_template('login.html')

# Sử lý đăng xuất
@app.route("/logout")
def logout_process():
	logout_user()
	return redirect('/login')

# load trang đăng ký
@app.route('/register', methods=['get', 'post'])
def register_process():
	err_msg = ''
	if request.method.__eq__('POST'):
		password = request.form.get('password')
		confirm = request.form.get('confirm')
		if password.__eq__(confirm):
			data = request.form.copy()
			del data['confirm']
			avatar = request.files.get('avatar')
			dao.add_user(avatar=avatar, **data)
			return redirect('/login')
		else:
			err_msg = 'Mật khẩu không khớp!'
	return render_template('register.html', err_msg=err_msg)


#lay cac giang vien ra
@app.route("/api/get_teacher", methods=["POST"])
def get_teacher():
	teacher = dao.get_teacher()
	return jsonify({"message": "teach_successfully", "data": teacher})


#lay tra ca hoc sinh chua co lop ra ra
@app.route("/api/get_students_no_class", methods=["POST"])
def get_students_no_class():
	studens_no_class = dao.get_students_no_Class()
	return jsonify({"message":"successfully","data":studens_no_class})

#lay hoc sinh ra theo lop
@app.route("/api/get_students_in_class", methods=["POST"])
def get_students_in_class():
	data =request.get_json()
	student_in_class = dao.get_stdents_in_class(data["malop"])
	return jsonify({"message":"successfully","data":student_in_class})


#api tra ta ca lop hoc da duoc tao ra
@app.route("/api/get_class", methods=["POST"])
def get_class():
	class_id = dao.get_class()
	return jsonify({"message":"successfully","data":class_id})


#them 1 hoặc danh sách hoc sinh vao database
@app.route("/api/add_Student", methods=['POST'])
def add_student():
    # Lấy dữ liệu từ request
	data = request.get_json()
	# print("data===>",data)
	if "data" in data and data["data"] is not None:
		data = data["data"]
		for student__ in data:
			dao.add_student(student__["name"],student__["brithday"],student__["phone"],student__["sex"],student__["address"],student__["mail"])
		return jsonify({"message": "Student added successfully", "data": data}), 201
	
	return jsonify({"error": "No data provided"}), 400
	

@app.route("/api/add_class", methods=['POST'])
def add_class():
    # Lấy dữ liệu từ request
	data = request.get_json()
	# print("data===>",data)
	if "data" in data and data["data"] is not None:
		
		data = data["data"]
		for class__ in data:
			print(class__["teach_id"])
			dao.add_class_Student(class__["malop"],class__["member"],class__["name"],class__["block_id"],class__["teach_id"])
		return jsonify({"message": "Student added successfully", "data": data}), 201
	
	return jsonify({"error": "No data provided"}), 400

@app.route("/api/add_hoc", methods=['POST'])
def add_hoc():
    # Lấy dữ liệu từ request
	data = request.get_json()
	# print("data===>",data)
	if "data" in data and data["data"] is not None:
		data = data["data"]
		for hoc__ in data:
			dao.add_hoc(hoc__["class_id"],hoc__["student_id"])
		return jsonify({"message": "add_hoc added successfully", "data": data}), 201
	
	return jsonify({"error": "No data provided"}), 400

# load trang admin
# @app.route("/login-admin", methods=['post'])
# def login_admin_process():
# 	username = request.form.get('username')
# 	password = request.form.get('password')
#
# 	u = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)
# 	if u:
# 		login_user(u)
#
# 	return redirect('/admin')






# Load Trang Tiếp Nhận Học Sinh
@app.route('/Student_admission')
def Student_admission():
	return render_template('Student_admission.html')


# Load Trang lập danh sách lớp
@app.route('/Make_class_list')
def Make_class_list():
	return render_template('Make_class_list.html')


# load trang nhập điểm
@app.route('/Enter_score')
def Enter_score():
	return render_template('Enter_score.html')


# Load trang xuất điểm
@app.route('/Starting_point')
def Starting_point():
	return render_template('Starting_point.html')


# Load trang thống kê báo cáo
@app.route('/Reporting_statistics')
def Reporting_statistics():
	return render_template('Reporting_statistics.html')


# Load trang thay đổi quy định
@app.route('/Change_rules')
def Change_rules():
	return render_template('Change_rules.html')


# Xử lý user từ cơ sở dữ liệu
@login.user_loader
def load_user(user_id):
	return dao.get_user_by_id(user_id)


@app.route("/login-admin", methods=['post'])
def login_admin_process():
	username = request.form.get('username')
	password = request.form.get('password')

	u = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)
	if u:
		login_user(u)

	return redirect('/admin')


@app.route('/api/course-report')
def api_course_report():
    course = request.args.get('course', 'Toán')  # Môn học
    year = request.args.get('year', '2023-2024')  # Năm học
    semester = request.args.get('semester', 'Học kỳ 1')  # Học kỳ

    data = course_report(course, year, semester)
    return jsonify(data)


if __name__ == '__main__':
	with app.app_context():
		from app import admin
		app.run(debug=True)
