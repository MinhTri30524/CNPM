import enum
from enum import Enum as RoleEnum

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from app import db, app


# Enum cho loại điểm
class LoaiDiemEnum(enum.Enum):
	KIEM_TRA_15_PHUT = 1
	GIUA_KY = 2
	CUOI_KY = 3


class UserRole(RoleEnum):
	ADMIN = 1
	TEACH = 2
	EMLOYES = 3


# Lớp Quản trị thừa kế từ User
class User(db.Model, UserMixin):
	__tablename__ = 'user'
	ma_nhan_vien = Column(Integer, primary_key=True, autoincrement=True)
	ho_ten = Column(String(100), nullable=False)
	username = Column(String(100), nullable=False, unique=True)
	password = Column(String(100), nullable=False)
	avatar = Column(String(100),
					default="https://chuphinhthe.com/upload/product/8239-duong-4751.jpg")
	user_role = Column(Enum(UserRole), default=UserRole.EMLOYES)

	# trả về id duy nhất để đăng nhập vào tài khoản
	def get_id(self):
		return str(self.ma_nhan_vien)


# Lớp Quản trị kế thừa từ User


class QuanTri(User):
	__tablename__ = 'quan_tri'
	ma_nhan_vien = Column(Integer, ForeignKey('user.ma_nhan_vien'), primary_key=True)


# Thêm các thuộc tính/method riêng cho QuanTri nếu cần


# Lớp Nhân viên kế thừa từ User
class NhanVien(User):
	__tablename__ = 'nhan_vien'
	ma_nhan_vien = Column(Integer, ForeignKey('user.ma_nhan_vien'), primary_key=True)


# Thêm các thuộc tính/method riêng cho NhanVien nếu cần


# Lớp Học sinh không kế thừa từ User
class HocSinh(db.Model):
	__tablename__ = 'hoc_sinh'
	ma_hoc_sinh = Column(Integer, primary_key=True, autoincrement=True)
	ho_ten = Column(String(100), nullable=False)
	ngay_sinh = Column(DateTime, nullable=False)
	gioi_tinh = Column(String(10), nullable=False)
	std = Column(Integer, nullable=False)
	dia_chi = Column(String(100), nullable=False)
	mail = Column(String(100), nullable=False)
	lop_hoc_id = Column(Integer, ForeignKey('lop_hoc.ma_lop'))  # Thêm cột khóa ngoại
	hocs = relationship('Hoc', backref='hoc_sinh', lazy=True)  # Quan hệ với Hoc
	lop_hoc = relationship("LopHoc", back_populates="hoc_sinhs")  # Quan hệ với LopHoc

	def __str__(self):
		return self.ma_hoc_sinh

	@staticmethod
	def getStudents_no_Class():
		# ham tra ve cac hoc sinh da dang ky nhap hoc ma chua co lop hoc
		students_no_class = db.session.query(HocSinh).filter(HocSinh.lop_hoc_id == None).all()
		result = [
			{
				"ma_hoc_sinh": student.ma_hoc_sinh,
				"ho_ten": student.ho_ten,
				"ngay_sinh": student.ngay_sinh.strftime("%Y-%m-%d") if student.ngay_sinh else None,
				"gioi_tinh": student.gioi_tinh,
				"dia_chi": student.dia_chi,
				"mail": student.mail,
			}
			for student in students_no_class
		]
		return result

	@staticmethod
	def get_students_in_class(lop_id):
		students_in_class = db.session.query(HocSinh).filter(HocSinh.lop_hoc_id == lop_id).all()
		result = [
			{
				"ma_hoc_sinh": student.ma_hoc_sinh,
				"ho_ten": student.ho_ten,
				"ngay_sinh": student.ngay_sinh.strftime("%Y-%m-%d") if student.ngay_sinh else None,
				"gioi_tinh": student.gioi_tinh,
				"dia_chi": student.dia_chi,
				"mail": student.mail,
			}
			for student in students_in_class
		]
		return result

	@staticmethod
	def get_students_by_year(semester_name, year):
		students = db.session.query(HocSinh).join(Hoc, HocSinh.ma_hoc_sinh == Hoc.hoc_sinh_id).join(
			Diem, Diem.hoc_id == Hoc.ma_hoc).join(HocKy, Diem.hoc_ky_id == HocKy.id).filter(
			HocKy.ten == semester_name, HocKy.nam_hoc == year).all()

		result = [
			{
				"ma_hoc_sinh": student.ma_hoc_sinh,
				"ho_ten": student.ho_ten,
				"ngay_sinh": student.ngay_sinh.strftime("%Y-%m-%d") if student.ngay_sinh else None,
				"gioi_tinh": student.gioi_tinh,
				"dia_chi": student.dia_chi,
				"mail": student.mail,
			}
			for student in students
		]
		return result


# Lớp Giảng viên kế thừa từ User
class GiangVien(User):
	__tablename__ = 'giang_vien'
	ma_nhan_vien = Column(Integer, ForeignKey('user.ma_nhan_vien'), primary_key=True)
	# Thiết lập 1-1 với LopHoc
	lop_hoc = relationship("LopHoc", back_populates="giang_vien", uselist=False)

	def to_dict(self):
		# Trả về thông tin kết hợp giữa GiangVien và User
		user_info = User.query.filter_by(ma_nhan_vien=self.ma_nhan_vien).first()
		return {
			"ma_nhan_vien": self.ma_nhan_vien,
			"ho_ten": user_info.ho_ten,
			"username": user_info.username,
			"avatar": user_info.avatar,
			"user_role": user_info.user_role.name,  # Nếu UserRole là Enum
		}


# Lớp Lớp học
class LopHoc(db.Model):
	__tablename__ = 'lop_hoc'
	ma_lop = Column(Integer, primary_key=True)
	so_luong = Column(Integer, nullable=False)
	ten = Column(String(100), nullable=False)
	khoi_id = Column(Integer, ForeignKey('khoi.id'))
	hoc_sinhs = relationship('HocSinh', back_populates='lop_hoc',
							 lazy=True)  # Thay backref thành back_populates
	hocs = relationship('Hoc', backref='lop_hoc', lazy=True)

	# Thiết lập mối quan hệ 1-1 với GiangVien
	giang_vien_id = Column(Integer, ForeignKey('giang_vien.ma_nhan_vien'),
						   unique=True)
	giang_vien = relationship("GiangVien", back_populates="lop_hoc", uselist=False, lazy=True)

	def to_dict(self):
		return {
			'id': self.ma_lop,
			'ten_lop': self.ten,
		}

	@staticmethod
	def get_all_class():
		classes = db.session.query(LopHoc).all()
		result = [
			{
				"ma_lop": _class.ma_lop,
				"ten_lop": _class.ten,
				# Các cột khác nếu có...
			}
			for _class in classes
		]
		return result


# Lớp Khối
class Khoi(db.Model):
	__tablename__ = 'khoi'
	id = Column(Integer, primary_key=True)
	ten = Column(String(100), nullable=False)
	lops = relationship('LopHoc', backref='khoi', lazy=True)


# Lớp Học
class Hoc(db.Model):
	__tablename__ = 'hoc'
	ma_hoc = Column(Integer, primary_key=True, autoincrement=True)
	lop_hoc_id = Column(Integer, ForeignKey('lop_hoc.ma_lop'))
	hoc_sinh_id = Column(Integer, ForeignKey('hoc_sinh.ma_hoc_sinh'))
	mon_hoc_id = Column(Integer, ForeignKey('mon_hoc.ma_mon'))
	diems = relationship('Diem', backref='hoc', lazy=True)


# Lớp Môn học
class MonHoc(db.Model):
	__tablename__ = 'mon_hoc'
	ma_mon = Column(Integer, primary_key=True)
	ten = Column(String(100), nullable=False)
	so_tiet = Column(Integer, nullable=False)
	hocs = relationship('Hoc', backref='mon_hoc', lazy=True)

	def __str__(self):
		return self.ten


# Lớp Điểm
class Diem(db.Model):
	__tablename__ = 'diem'
	id = Column(Integer, primary_key=True, autoincrement=True)
	loai_diem = Column(Enum(LoaiDiemEnum), nullable=False)
	diem = Column(Float, nullable=False)
	hoc_ky_id = Column(Integer, ForeignKey('hoc_ky.id'))
	hoc_id = Column(Integer, ForeignKey('hoc.ma_hoc'))


# Lớp Học kỳ
class HocKy(db.Model):
	__tablename__ = 'hoc_ky'
	id = Column(Integer, primary_key=True)
	ten = Column(String(100), nullable=False)
	nam_hoc = Column(String(20), nullable=False)
	diems = relationship('Diem', backref='hoc_ky', lazy=True)

	def __str__(self):
		return self.ten


if __name__ == '__main__':
	with app.app_context():
		db.create_all()
