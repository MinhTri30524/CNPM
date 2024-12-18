# import enum
# from flask_login import UserMixin
# from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
# from sqlalchemy.orm import relationship
#
# from app import db, app
#
#
# class User(db.Model, UserMixin):
# 	__tablename__ = 'user'
# 	ma_nhan_vien = Column(Integer, primary_key=True, autoincrement=True)
# 	ho_ten = Column(String(100), nullable=False)
# 	ten_lot = Column(String(100), nullable=False)
# 	ngay_sinh = Column(String(100), nullable=False)
# 	dia_chi = Column(String(100), nullable=False, unique=True)
# 	email = Column(String(100), nullable=False, unique=True)
# 	so_dien_thoai = Column(String(100), nullable=False, unique=True)
#
#
# class LoaiDiemEnum(enum.Enum):
#     KIEM_TRA_MIENG = 'Kiểm tra miệng'
#     KIEM_TRA_15_PHUT = 'Kiểm tra 15 phút'
#     GIUA_KY = 'Giữa kỳ'
#     CUOI_KY = 'Cuối kỳ'
#
#
# class QuanTri(User):
#
# 	def __str__(self):
# 		return self.fullname
#
#
# class NhanVien(User):
#
# 	def __str__(self):
# 		return self.fullname
#
#
# class HocSinh(User):
# 	hocs = relationship('Hoc', backref='hoc_sinh', lazy=True)  # Quan hệ với Hoc
# 	bang_diems = relationship('BangDiem', backref='hoc_sinh', lazy=True)  # Quan hệ với Bang
#
# 	def __str__(self):
# 		return self.ten
#
#
# class LopHoc(db.Model):
# 	ma_lop = Column(db.Integer, primary_key=True)
# 	ten = Column(db.String(100))
#
# 	giang_vien_id = Column(db.Integer, db.ForeignKey('giang_vien.ma_nhan_vien'))
# 	khoi_id = Column(db.Integer, db.ForeignKey('khoi.id'))
#
# 	hoc_sinhs = relationship('HocSinh', backref='lop_hoc', lazy=True)  # Quan hệ với HocSinh
# 	hocs = relationship('Hoc', backref='lop_hoc', lazy=True)  # Quan hệ với Hoc
# 	giang_vien = relationship('GiangVien', back_populates='lop_hoc', uselist=False)  # Quan hệ 1-1
#
# 	def __str__(self):
# 		return self.ten
#
#
# class Khoi(db.Model):
# 	id = Column(db.Integer, primary_key=True)
# 	ten = Column(db.String(100))
# 	lops = relationship('LopHoc', backref='khoi', lazy=True)  # Quan hệ với LopHoc
# # Thêm các field và method tương ứng
#
#
# class Hoc(db.Model):
# 	ma_hoc = Column(db.Integer, primary_key=True, autoincrement=True)
# 	lop_hoc_id = Column(db.Integer, db.ForeignKey('lop_hoc.ma_lop'))
# 	hoc_sinh_id = Column(db.Integer, db.ForeignKey('hoc_sinh.ma_nhan_vien'))
# 	hoc_ky_id = Column(db.Integer, db.ForeignKey('hoc_ky.id'))
#
#
# class MonHoc(db.Model):
# 	ma_mon = Column(db.Integer, primary_key=True)
# 	ten = Column(db.String(100))
# 	so_tiet = Column(db.Integer)
# 	bang_diems = relationship('BangDiem', backref='mon_hoc', lazy=True)  # Quan hệ với BangDiem
#
# 	def __str__(self):
# 		return self.ten
#
#
# class Diem(db.Model):
# 	id = Column(db.Integer, primary_key=True)
# 	loai_diem = Column(Enum(LoaiDiemEnum))
# 	diem = Column(db.Float)
# 	hoc_ky_id = Column(db.Integer, db.ForeignKey('hoc_ky.id'))
# 	mon_hoc_id = Column(db.Integer, db.ForeignKey('mon_hoc.ma_mon'))
# 	hoc_sinh_id = Column(db.Integer, db.ForeignKey('hoc_sinh.ma_nhan_vien'))
#
#
# class HocKy(db.Model):
# 	id = Column(db.Integer, primary_key=True)
# 	ten = Column(db.String(100))
# 	nam_hoc = Column(DateTime)
#
# 	bang_diems = relationship('BangDiem', backref='hoc_ky', lazy=True)  # Quan hệ với BangDiem
# 	hocs = relationship('Hoc', backref='hoc_ky', lazy=True)  # Quan hệ với Hoc
#
# 	def __str__(self):
# 		return self.ten
#
#
# class GiangVien(User):
# 	__tablename__ = 'giang_vien'
# 	ma_nhan_vien = Column(Integer, ForeignKey('user.ma_nhan_vien'),
# 						  primary_key=True)  # Liên kết với User
# 	lop_hoc = relationship('LopHoc', back_populates='giang_vien', uselist=False)  # Quan hệ 1-1
#
# 	def __str__(self):
# 		return self.ten
#
#
# if __name__ == '__main__':
# 	with app.app_context():
# 		db.create_all()


import enum
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db, app


# Lớp cơ sở người dùng
# class User(db.Model, UserMixin):
#     __tablename__ = 'user'
#     ma_nhan_vien = Column(Integer, primary_key=True, autoincrement=True)
#     ho_ten = Column(String(100), nullable=False)
#     ten_lot = Column(String(100), nullable=False)
#     ngay_sinh = Column(String(100), nullable=False)
#     dia_chi = Column(String(100), nullable=False, unique=True)
#     email = Column(String(100), nullable=False, unique=True)
#     so_dien_thoai = Column(String(100), nullable=False, unique=True)


# Enum cho loại điểm
class LoaiDiemEnum(enum.Enum):
    KIEM_TRA_MIENG = 'Kiểm tra miệng'
    KIEM_TRA_15_PHUT = 'Kiểm tra 15 phút'
    GIUA_KY = 'Giữa kỳ'
    CUOI_KY = 'Cuối kỳ'


# Lớp Quản trị thừa kế từ User
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    ma_nhan_vien = Column(Integer, primary_key=True, autoincrement=True)
    ho_ten = Column(String(100), nullable=False)
    ten_lot = Column(String(100), nullable=False)
    ngay_sinh = Column(String(100), nullable=False)
    dia_chi = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    so_dien_thoai = Column(String(100), nullable=False, unique=True)

    # Định nghĩa __str__ để dễ đọc hơn
    def __str__(self):
        return self.ho_ten


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


# Lớp Học sinh kế thừa từ User
class HocSinh(User):
    __tablename__ = 'hoc_sinh'
    ma_nhan_vien = Column(Integer, ForeignKey('user.ma_nhan_vien'), primary_key=True)
    hocs = relationship('Hoc', backref='hoc_sinh', lazy=True)  # Quan hệ với Hoc
    # Thêm các thuộc tính/method riêng cho HocSinh nếu cần


# Lớp Giảng viên kế thừa từ User
class GiangVien(User):
    __tablename__ = 'giang_vien'
    ma_nhan_vien = Column(Integer, ForeignKey('user.ma_nhan_vien'), primary_key=True)
    lop_hoc = relationship('LopHoc', back_populates='giang_vien', uselist=False)  # Quan hệ 1-1
    # Thêm các thuộc tính/method riêng cho GiangVien nếu cần


# Lớp Lớp học
class LopHoc(db.Model):
    __tablename__ = 'lop_hoc'
    ma_lop = Column(Integer, primary_key=True)
    ten = Column(String(100), nullable=False)
    giang_vien_id = Column(Integer, ForeignKey('giang_vien.ma_nhan_vien'), unique=True)  # Quan hệ 1-1
    khoi_id = Column(Integer, ForeignKey('khoi.id'))

    hoc_sinhs = relationship('HocSinh', backref='lop_hoc', lazy=True)
    hocs = relationship('Hoc', backref='lop_hoc', lazy=True)
    giang_vien = relationship('GiangVien', back_populates='lop_hoc', uselist=False)

    def __str__(self):
        return self.ten


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
    hoc_sinh_id = Column(Integer, ForeignKey('hoc_sinh.ma_nhan_vien'))
    hoc_ky_id = Column(Integer, ForeignKey('hoc_ky.id'))


# Lớp Môn học
class MonHoc(db.Model):
    __tablename__ = 'mon_hoc'
    ma_mon = Column(Integer, primary_key=True)
    ten = Column(String(100), nullable=False)
    so_tiet = Column(Integer, nullable=False)
    bang_diems = relationship('Diem', backref='mon_hoc', lazy=True)

    def __str__(self):
        return self.ten


# Lớp Điểm
class Diem(db.Model):
    __tablename__ = 'diem'
    id = Column(Integer, primary_key=True)
    loai_diem = Column(Enum(LoaiDiemEnum), nullable=False)
    diem = Column(Float, nullable=False)
    hoc_ky_id = Column(Integer, ForeignKey('hoc_ky.id'))
    mon_hoc_id = Column(Integer, ForeignKey('mon_hoc.ma_mon'))
    hoc_sinh_id = Column(Integer, ForeignKey('hoc_sinh.ma_nhan_vien'))


# Lớp Học kỳ
class HocKy(db.Model):
    __tablename__ = 'hoc_ky'
    id = Column(Integer, primary_key=True)
    ten = Column(String(100), nullable=False)
    nam_hoc = Column(DateTime, nullable=False)
    hocs = relationship('Hoc', backref='hoc_ky', lazy=True)

    def __str__(self):
        return self.ten


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
