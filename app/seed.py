from app import db, app
from app.models import HocKy, Diem, LoaiDiemEnum, Hoc, Khoi, LopHoc, MonHoc, HocSinh, GiangVien, \
	UserRole

if __name__ == '__main__':
	with app.app_context():
		# Thêm dữ liệu cho bảng Khoi
		khoi_1 = Khoi(ten="Khối 10")
		khoi_2 = Khoi(ten="Khối 11")
		khoi_3 = Khoi(ten="Khối 12")
		db.session.add_all([khoi_1, khoi_2, khoi_3])

		# Thêm dữ liệu cho bảng LopHoc
		lop_1 = LopHoc(so_luong=30, ten="10A1", khoi_id=1)
		lop_2 = LopHoc(so_luong=35, ten="11B1", khoi_id=2)
		lop_3 = LopHoc(so_luong=28, ten="12C1", khoi_id=3)
		db.session.add_all([lop_1, lop_2, lop_3])

		# Thêm dữ liệu cho bảng MonHoc
		mon_toan = MonHoc(ten="Toán", so_tiet=45)
		mon_ly = MonHoc(ten="Vật Lý", so_tiet=40)
		mon_hoa = MonHoc(ten="Hóa Học", so_tiet=35)
		db.session.add_all([mon_toan, mon_ly, mon_hoa])

		# Thêm dữ liệu vào bảng HocSinh
		hs_1 = HocSinh(
			ho_ten="Nguyễn Văn A",
			ngay_sinh="2008-09-01",
			gioi_tinh="Nam",
			dia_chi="Hà Nội",
			mail="vana@gmail.com",
			lop_hoc_id=1
		)
		hs_2 = HocSinh(
			ho_ten="Trần Thị B",
			ngay_sinh="2009-05-10",
			gioi_tinh="Nữ",
			dia_chi="Hải Phòng",
			mail="thib@gmail.com",
			lop_hoc_id=2
		)
		db.session.add_all([hs_1, hs_2])

		# Thêm dữ liệu GiangVien
		gv_1 = GiangVien(
			ho_ten="Lê Thị C",
			username="letc",
			password="password123",
			user_role=UserRole.TEACH
		)
		db.session.add(gv_1)

		# Thêm dữ liệu HocKy
		hoc_ky_1 = HocKy(ten="Học kỳ 1", nam_hoc="2023-2024")
		hoc_ky_2 = HocKy(ten="Học kỳ 2", nam_hoc="2023-2024")
		db.session.add_all([hoc_ky_1, hoc_ky_2])

		# Thêm dữ liệu cho bảng Hoc
		hoc_1 = Hoc(lop_hoc_id=1, hoc_sinh_id=1, mon_hoc_id=1)
		hoc_2 = Hoc(lop_hoc_id=2, hoc_sinh_id=2, mon_hoc_id=2)
		hoc_3 = Hoc(lop_hoc_id=3, hoc_sinh_id=1, mon_hoc_id=3)
		db.session.add_all([hoc_1, hoc_2, hoc_3])

		# Thêm dữ liệu Diem
		diem_1 = Diem(loai_diem=LoaiDiemEnum.KIEM_TRA_15_PHUT, diem=8.5, hoc_ky_id=1, hoc_id=1)
		diem_2 = Diem(loai_diem=LoaiDiemEnum.CUOI_KY, diem=9.0, hoc_ky_id=1, hoc_id=1)
		db.session.add_all([diem_1, diem_2])

	db.session.commit()
