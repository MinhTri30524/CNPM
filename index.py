import math
from flask import render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user
from app import app, login
from app import dao, utils
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
			print("data======>",data)
			dao.add_student(student__["ma_hoc_sinh"],student__["ho_ten"],student__["ngay_sinh"],student__["std"],student__["gioi_tinh"],student__["dia_chi"],student__["mail"])
		return jsonify({"message": "Student added successfully", "data": data}), 201
	
	return jsonify({"error": "No data provided"}), 400

@app.route("/api/remote_Student", methods=['POST'])
def remote_student():
    # Lấy dữ liệu từ request
	data = request.get_json()
	# print("data===>",data)
	if "data" in data and data["data"] is not None:
		data = data["data"]
		for student__ in data:
			print("data======>",data)
			dao.remote_students(student__["ma_sinh_vien"])
		return jsonify({"message": "Student added successfully", "data": data}), 201
	
	return jsonify({"error": "No data provided"}), 400



@app.route("/api/add_class", methods=['POST'])
def add_class():
    # Lấy dữ liệu từ request
	data = request.get_json()
	print("data===>",data)
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
	print("data===>",data)
	if "data" in data and data["data"] is not None:
		data = data["data"]
		for hoc__ in data:
			dao.add_hoc(hoc__["class_id"],hoc__["student_id"])
		return jsonify({"message": "add_hoc added successfully", "data": data}), 201
	
	return jsonify({"error": "No data provided"}), 400	


@app.route('/api/get_student_scores', methods=['POST'])
def get_student_scores():
    data = request.json
    class_input = data.get('class')
    student_name = data.get('name', "").strip()
    academic_year = data.get('year')

    # Giả sử có một hàm get_scores_from_db lấy dữ liệu từ database
    scores = get_scores_from_db(class_input, academic_year, student_name)

    if not scores:
        return jsonify({"success": False, "message": "Không tìm thấy học sinh nào."})

    # Tính điểm trung bình
    for student in scores:
        student['averageHK1'] = calculate_average(student['scoresHK1'])
        student['averageHK2'] = calculate_average(student['scoresHK2'])

    return jsonify({"success": True, "scores": scores})

def calculate_average(scores):
    total_points = 0
    total_weights = 0

    for score_type, weight in [('15p', 1), ('45p', 2), ('final', 3)]:
        for score in scores.get(score_type, []):
            total_points += score * weight
            total_weights += weight

    return round(total_points / total_weights, 2) if total_weights > 0 else 0

def get_scores_from_db(class_input, academic_year, student_name):
    # Ví dụ dữ liệu giả lập
    students = [
        {
            "name": "Nguyễn Văn A",
            "class": "10A",
			"academic_year": "2022-2023",
            "scoresHK1": {
                "15p": [8, 7, 9],
                "45p": [8, 9],
                "final": [9],
            },
            "scoresHK2": {
                "15p": [7, 6],
                "45p": [7, 8],
                "final": [8],
            }
        }
    ]

    filtered_students = [
        s for s in students
        if s['class'] == class_input and
        (not student_name or student_name.lower() in s['name'].lower())
    ]

    return filtered_students

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
	students = dao.get_students_no_Class()
	return render_template('Student_admission.html', student = students)


# Load Trang lập danh sách lớp
@app.route('/Make_class_list')
def Make_class_list():
	students = dao.get_students_no_Class()
	class_id = dao.get_class()
	return render_template("Make_class_list.html", students=students, classes=class_id)



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
    return redirect('/admin')


if __name__ == '__main__':
	with app.app_context():
		from app import admin
		app.run(debug=True)
