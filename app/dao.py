import hashlib

import cloudinary.uploader

from app import db, app
from app.models import User, HocSinh, GiangVien, LopHoc, Diem, Hoc, HocKy, MonHoc, Khoi


# lấy user đó ra
def auth_user(username, password, role=None):
	password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
	u = User.query.filter(User.username.__eq__(username.strip()),
						  User.password.__eq__(password))
	if role:
		u = u.filter(User.user_role.__eq__(role))
		print("role=====>", role)
	return u.first()


# Thêm người dùng mới
def add_user(id, name, username, password, avatar):
	password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
	role = "EMLOYES"
	if id.startswith('20'):
		role = "ADMIN"
	elif id.startswith('19'):
		role = "TEACH"
	elif id.startswith("18"):
		role = "EMLOYES"
	u = User(ma_nhan_vien=id, ho_ten=name, username=username, password=password,
			 avatar='https://chuphinhthe.com/upload/product/8239-duong-4751.jpg', user_role=role)
	if avatar:
		res = cloudinary.uploader.upload(avatar)
		u.avatar = res.get('secure_url')
	db.session.add(u)
	db.session.commit()


# thêm một học sinh mới
def add_student(ma_hoc_sinh,ho_ten, ngay_sinh, std, gioi_tinh, dia_chi, mail):
	# Kiểm tra xem học sinh đã tồn tại trong cơ sở dữ liệu chưa
    existing_student = HocSinh.query.filter_by(ma_hoc_sinh=ma_hoc_sinh).first()
    if existing_student:
        # Nếu học sinh đã tồn tại, cập nhật những trường thay đổi
        existing_student.ho_ten = ho_ten
        existing_student.ngay_sinh = ngay_sinh
        existing_student.std = std
        existing_student.gioi_tinh = gioi_tinh
        existing_student.dia_chi = dia_chi
        existing_student.mail = mail
        db.session.commit()  # Lưu lại thay đổi vào cơ sở dữ liệu
        return "Thông tin học sinh đã được cập nhật."
    else:
        # Nếu học sinh chưa tồn tại, thêm mới học sinh
        add = HocSinh(ma_hoc_sinh=ma_hoc_sinh, ho_ten=ho_ten, ngay_sinh=ngay_sinh,
                      gioi_tinh=gioi_tinh, std=std, dia_chi=dia_chi, mail=mail)
        db.session.add(add)
        db.session.commit()  # Lưu học sinh mới vào cơ sở dữ liệu
        return "Học sinh đã được thêm mới."



# tạo một lớp học mới
def add_class_student(malop, so_luong, ten, khoi_id, giang_vien_id):
    existing_class = LopHoc.query.filter_by(ma_lop=malop).first()

    if existing_class:
        # Nếu ma_lop đã tồn tại, cập nhật nội dung
        existing_class.so_luong = so_luong
        existing_class.ten = ten
        existing_class.khoi_id = khoi_id
        existing_class.giang_vien_id = giang_vien_id
        print(f"Đã cập nhật lớp học với mã lớp: {malop}")
    else:

        new_class = LopHoc(ma_lop=malop, so_luong=so_luong, ten=ten, khoi_id=khoi_id, giang_vien_id=giang_vien_id)
        db.session.add(new_class)
        print(f"Đã thêm lớp học mới với mã lớp: {malop}")

    db.session.commit()


# Lấy tất cả giảng viên ra
def get_teacher():
	tech = User.query.filter(User.user_role == "TEACH").all()
	result = [
			{
				"ho_ten": tech__.ho_ten,
				"ma_nhan_vien": tech__.ma_nhan_vien,
				# Các cột khác nếu có...
			}
			for tech__ in tech
		]
	return result


# add hoc thanh lap lop tu nhan vien tao
def add_hoc(class_id, student_id):
	add = Hoc(lop_hoc_id=class_id, hoc_sinh_id=student_id)
	db.session.add(add)
	db.session.commit()


# lấy tất cả học sinh đã đã đang ký nhập học chưa có id mã lóp
def get_students_no_Class():
	students = HocSinh.getStudents_no_Class()
	return students

def remote_students(ma_hoc_sinh):
	student = HocSinh.query.filter_by(ma_hoc_sinh=ma_hoc_sinh).first()
	if student:
		db.session.delete(student)
		db.session.commit()

def get_khoi():
	khoi__ = Khoi.query.all()
	return khoi__



# tra ve hoc sinh theo id lop ho da co san
def get_stdents_in_class(class_id):
	students_in_class = HocSinh.get_students_in_class(class_id)
	return students_in_class

def remote_class(ma_lop):
	class__ =  LopHoc.query.filter_by(ma_lop=ma_lop).first()
	if class__:
		db.session.delete(class__)
		db.session.commit()

# lay tat ca cac lop hoc da duoc tao ra
def get_class():
	class_id = LopHoc.query.all()
	result = [
			{
				"ma_lop": _class.ma_lop,
				"so_luong":_class.so_luong,
				"ten": _class.ten,
				"khoi_id": _class.khoi_id,
				"giang_vien_id":_class.giang_vien_id
			}
			for _class in class_id
		]
	return result

#api lấy và lưu dữ liệu cho phần nhập điểm



def get_user_by_id(ma_nhan_vien):
	return User.query.get(ma_nhan_vien)


def get_students_by_year(semester_name, year):
	students = HocSinh.get_students_in_class(semester_name, year)
	return students


# Hàm lấy điểm của học sinh theo tên lớp, tên học kỳ, năm học và tên môn học
def get_student_scores(class_name, semester_name, year, subject_name):
	scores = db.session.query(
		HocSinh.ma_hoc_sinh,
		HocSinh.ho_ten,
		Diem.diem,
		Diem.loai_diem
	).join(Hoc, Hoc.hoc_sinh_id == HocSinh.ma_hoc_sinh).join(
		LopHoc, Hoc.lop_hoc_id == LopHoc.ma_lop).join(
		Diem, Diem.hoc_id == Hoc.ma_hoc).join(
		HocKy, Diem.hoc_ky_id == HocKy.id).join(
		MonHoc, Hoc.mon_hoc_id == MonHoc.ma_mon).filter(
		LopHoc.ten == class_name,
		HocKy.ten == semester_name,
		HocKy.nam_hoc == year,
		MonHoc.ten == subject_name
	).all()

	result = {}
	for score in scores:
		if score.ma_hoc_sinh not in result:
			result[score.ma_hoc_sinh] = {
				"ma_hoc_sinh": score.ma_hoc_sinh,
				"ho_ten": score.ho_ten,
				"diems": []
			}
		result[score.ma_hoc_sinh]["diems"].append({
			"diem": score.diem,
			"loai_diem": score.loai_diem.name
		})

	return list(result.values())


# Hàm lấy điểm trung bình của học sinh theo năm học
def get_average_score_by_year(year):
	average_scores = db.session.query(
		HocSinh.ma_hoc_sinh,
		HocSinh.ho_ten,
		HocKy.ten,
		db.func.avg(Diem.diem).label('average_score')
	).join(Hoc, Hoc.hoc_sinh_id == HocSinh.ma_hoc_sinh).join(
		LopHoc, Hoc.lop_hoc_id == LopHoc.ma_lop).join(
		Diem, Diem.hoc_id == Hoc.ma_hoc).join(
		HocKy, Diem.hoc_ky_id == HocKy.id).filter(
		HocKy.nam_hoc == year
	).group_by(
		HocSinh.ma_hoc_sinh,
		HocSinh.ho_ten,
		HocKy.ten
	).all()

	result = {}
	for score in average_scores:
		if score.ma_hoc_sinh not in result:
			result[score.ma_hoc_sinh] = {
				"ma_hoc_sinh": score.ma_hoc_sinh,
				"ho_ten": score.ho_ten,
				"average_scores": {}
			}
		result[score.ma_hoc_sinh]["average_scores"][score.ten_hoc_ky] = score.average_score

	return list(result.values())


# Hàm báo cáo tổng kết môn học
def course_report(course, year, semester):
	# Trả về Lớp, sĩ số, số lượng đạt, tỷ lệ đạt
	statis = db.session.query(
		LopHoc.ten,
		db.func.count(HocSinh.ma_hoc_sinh).label('si_so'),
		db.func.sum(db.case(
			(Diem.diem >= 5, 1),
			else_=0
		)).label('so_luong_dat'),
		db.func.avg(db.case(
			(Diem.diem >= 5, 1),
			else_=0
		)).label('ty_le_dat')
	).join(Hoc, Hoc.lop_hoc_id == LopHoc.ma_lop).join(
		HocSinh, Hoc.hoc_sinh_id == HocSinh.ma_hoc_sinh  # Thêm liên kết giữa HocSinh và Hoc
	).join(
		Diem, Diem.hoc_id == Hoc.ma_hoc
	).join(
		HocKy, Diem.hoc_ky_id == HocKy.id
	).join(
		MonHoc, Hoc.mon_hoc_id == MonHoc.ma_mon
	).filter(
		MonHoc.ten == course,
		HocKy.ten == semester,
		HocKy.nam_hoc == year
	).group_by(
		LopHoc.ten
	).all()

	return [
		{
			"lop": statis[0],
			"si_so": statis[1],
			"so_luong_dat": int(statis[2]),
			"ty_le_dat": float(statis[3])
		}
		for statis in statis
	]


# Chạy thử các hàm
if __name__ == '__main__':
	with app.app_context():
		res = get_student_scores("10A1", "Học kỳ 1", "2023-2024", "Toán")
		print(res)
