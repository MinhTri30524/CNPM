import hashlib

import cloudinary.uploader

from app import db, app
from app.models import User, HocSinh, GiangVien, LopHoc, Diem, Hoc, HocKy, MonHoc


# lấy user đó ra
def auth_user(username, password, role=None):
	password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

	u = User.query.filter(User.username.__eq__(username.strip()),
						  User.password.__eq__(password))
	print("uuuuuuuuuuuuuuuu===>", u)
	if role:
		u = u.filter(User.user_role.__eq__(role))
		print("role=====>", role)

	return u.first()


# Thêm người dùng mới
def add_user(id, name, username, password, avatar):
	password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
	u = User(ma_nhan_vien=id, ho_ten=name, username=username, password=password,
			 avatar='https://chuphinhthe.com/upload/product/8239-duong-4751.jpg')
	if avatar:
		res = cloudinary.uploader.upload(avatar)
		u.avatar = res.get('secure_url')

	db.session.add(u)
	db.session.commit()


# thêm một học sinh mới
def add_student(name, birthDate, phone, sex, address, email):
	print(name)
	add = HocSinh(ho_ten=name, ngay_sinh=birthDate, gioi_tinh=sex, std=phone, dia_chi=address,
				  mail=email)
	db.session.add(add)
	db.session.commit()


# tạo một lớp học mới
def aad_class_Student(malop, so_luong, ten, giang_vien):
	pass


# Lấy tất cả giảng viên ra
def get_teacher():
	# Lấy tất cả giảng viên từ bảng GiangVien
	gv = GiangVien.query.all()
	# Chuyển mỗi giảng viên thành từ điển bằng phương thức to_dict()
	teachers = [teacher.to_dict() for teacher in gv]
	return teachers


# lấy tất cả học sinh đã đã đang ký nhập học chưa có id mã lóp
def get_students_no_Class():
	students = HocSinh.getStudents_no_Class()
	return students


# tra ve hoc sinh theo id lop ho da co san
def get_stdents_in_class(class_id):
	students_in_class = HocSinh.get_students_in_class(class_id)
	return students_in_class


# lay tat ca cac lop hoc da duoc tao ra
def get_class():
	class_id = LopHoc.get_all_class()
	return class_id


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
			"ty_le_dat": float(statis[3]) * 100
		}
		for statis in statis
	]


# Chạy thử các hàm
if __name__ == '__main__':
	with app.app_context():
		res = get_student_scores("10A1", "Học kỳ 1", "2023-2024", "Toán")
		print(res)
