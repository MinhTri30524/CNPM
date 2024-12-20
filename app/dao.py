from app.models import User, HocSinh,GiangVien, LopHoc
from app import app, db
import hashlib
import cloudinary.uploader
from flask import jsonify

#lấy user đó ra
def auth_user(username, password, role=None):
	password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

	u = User.query.filter(User.username.__eq__(username.strip()),
						  User.password.__eq__(password))
	print("uuuuuuuuuuuuuuuu===>",u)
	if role:
		u = u.filter(User.user_role.__eq__(role))
		print("role=====>",role)

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
#thêm một học sinh mới
def add_student(name, birthDate,phone, sex, address, email ):
	print(name)
	add = HocSinh(ho_ten = name, ngay_sinh = birthDate, gioi_tinh=sex, std=phone, dia_chi=address, mail=email)
	db.session.add(add)
	db.session.commit()

#tạo một lớp học mới
def aad_class_Student(malop, so_luong, ten, giang_vien):
	pass

#Lấy tất cả giảng viên ra
def get_teacher():
    # Lấy tất cả giảng viên từ bảng GiangVien
    gv = GiangVien.query.all()
    # Chuyển mỗi giảng viên thành từ điển bằng phương thức to_dict()
    teachers = [teacher.to_dict() for teacher in gv]
    return teachers

#lấy tất cả học sinh đã đã đang ký nhập học chưa có id mã lóp
def get_students_no_Class():
	students = HocSinh.getStudents_no_Class()
	return students

#tra ve hoc sinh theo id lop ho da co san
def get_stdents_in_class(class_id):
	students_in_class = HocSinh.get_students_in_class(class_id)
	return students_in_class

#lay tat ca cac lop hoc da duoc tao ra
def get_class():
	class_id = LopHoc.get_all_class()
	return class_id

def get_user_by_id(ma_nhan_vien):
	return User.query.get(ma_nhan_vien)
