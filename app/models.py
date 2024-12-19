import enum
from enum import Enum as RoleEnum
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db, app

# Enum cho loại điểm
class LoaiDiemEnum(enum.Enum):
    KIEM_TRA_MIENG = 'Kiểm tra miệng'
    KIEM_TRA_15_PHUT = 'Kiểm tra 15 phút'
    GIUA_KY = 'Giữa kỳ'
    CUOI_KY = 'Cuối kỳ'

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
    avatar = Column(String(100), default="https://chuphinhthe.com/upload/product/8239-duong-4751.jpg")
    user_role = Column(Enum(UserRole), default=UserRole.EMLOYES)
    #trả về id duy nhất để đăng nhập vào tài khoản
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
    ngay_sinh =  Column(DateTime, nullable=False)
    gioi_tinh = Column(String(10), nullable=False)
    std =  Column(Integer, nullable=False)
    dia_chi = Column(String(100), nullable=False)
    mail = Column(String(100), nullable=False)
    lop_hoc_id = Column(Integer, ForeignKey('lop_hoc.ma_lop'))  # Thêm cột khóa ngoại
    hocs = relationship('Hoc', backref='hoc_sinh', lazy=True)  # Quan hệ với Hoc
    lop_hoc = relationship("LopHoc", back_populates="hoc_sinhs")  # Quan hệ với LopHoc

    def __str__(self):
        return self.ma_hoc_sinh

# Lớp Giảng viên kế thừa từ User
class GiangVien(User):
    __tablename__ = 'giang_vien'
    ma_nhan_vien = Column(Integer, ForeignKey('user.ma_nhan_vien'), primary_key=True)
    lop_hoc = relationship('LopHoc', back_populates='giang_vien', uselist=False)  # Quan hệ 1-1

# Lớp Lớp học
class LopHoc(db.Model):
    __tablename__ = 'lop_hoc'
    ma_lop = Column(Integer, primary_key=True)
    ten = Column(String(100), nullable=False)
    giang_vien_id = Column(Integer, ForeignKey('giang_vien.ma_nhan_vien'), unique=True)  # Quan hệ 1-1
    khoi_id = Column(Integer, ForeignKey('khoi.id'))
    hoc_sinhs = relationship('HocSinh', back_populates='lop_hoc', lazy=True)  # Thay backref thành back_populates
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
    hoc_sinh_id = Column(Integer, ForeignKey('hoc_sinh.ma_hoc_sinh'))
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
    hoc_sinh_id = Column(Integer, ForeignKey('hoc_sinh.ma_hoc_sinh'))

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
