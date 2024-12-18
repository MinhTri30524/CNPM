import enum
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app import db, app


class User(db.Model, UserMixin):
	id = Column(Integer, primary_key=True)
	username = Column(String(100), unique=True)
	password = Column(String(100))
	fullname = Column(String(100))
	avatar = Column(String(255))


class LoaiDiemEnum(enum.Enum):
    KIEM_TRA_MIENG = 'Kiểm tra miệng'
    KIEM_TRA_15_PHUT = 'Kiểm tra 15 phút'
    GIUA_KY = 'Giữa kỳ'
    CUOI_KY = 'Cuối kỳ'


class QuanTri(User):
	pass


class NhanVien(User):
	pass


class HocSinh(db.Model):
	id = Column(db.Integer, primary_key=True)
	ten = Column(db.String(100))
	hocs = relationship('Hoc', backref='hoc_sinh', lazy=True)  # Quan hệ với Hoc
	bang_diems = relationship('BangDiem', backref='hoc_sinh', lazy=True)  # Quan hệ với Bang

	def __str__(self):
		return self.ten


class LopHoc(db.Model):
	id = Column(db.Integer, primary_key=True)
	ten = Column(db.String(100))
	hoc_sinhs = relationship('HocSinh', backref='lop_hoc', lazy=True)  # Quan hệ với HocSinh
	hocs = relationship('Hoc', backref='lop_hoc', lazy=True)  # Quan hệ với Hoc
	khoi_id = Column(db.Integer, db.ForeignKey('khoi.id'))

	def __str__(self):
		return self.ten


class Khoi(db.Model):
	id = Column(db.Integer, primary_key=True)
	ten = Column(db.String(100))
	lops = relationship('LopHoc', backref='khoi', lazy=True)  # Quan hệ với LopHoc
# Thêm các field và method tương ứng


class Hoc(db.Model):
	lop_hoc_id = Column(db.Integer, db.ForeignKey('lop_hoc.id'), primary_key=True)
	hoc_sinh_id = Column(db.Integer, db.ForeignKey('hoc_sinh.id'), primary_key=True)


class MonHoc(db.Model):
	id = Column(db.Integer, primary_key=True)
	ten = Column(db.String(100))
# Thêm các field và method tương ứng

	def __str__(self):
		return self.ten


class BangDiem(db.Model):
	id = Column(db.Integer, primary_key=True)
	hoc_ky_id = Column(db.Integer, db.ForeignKey('hoc_ky.id'))
	mon_hoc_id = Column(db.Integer, db.ForeignKey('mon_hoc.id'))
	hoc_sinh_id = Column(db.Integer, db.ForeignKey('hoc_sinh.id'))
	diems = relationship('Diem', backref='bang_diem', lazy=True)  # Quan hệ với Diem


class Diem(db.Model):
	id = Column(db.Integer, primary_key=True)
	diem = Column(db.Float, nullable=False)
	bangdiem_id = Column(db.Integer, db.ForeignKey('bang_diem.id'))
	loai_diem = Column(Enum(LoaiDiemEnum), nullable=False)


class HocKy(db.Model):
	id = Column(db.Integer, primary_key=True)
	ten = Column(db.String(100))
	bang_diems = relationship('BangDiem', backref='hoc_ky', lazy=True)  # Quan hệ với BangDiem

	def __str__(self):
		return self.ten


class GiangVien(db.Model):
	id = Column(db.Integer, primary_key=True)

	def __str__(self):
		return self.ten


if __name__ == '__main__':
	with app.app_context():
		db.create_all()
