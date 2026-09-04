# Phan cong nhiem vu project QuanLyHangHoa

## 1. Thong tin chung

- Ten project: QuanLyHangHoa
- Chu de: Chuong trinh quan ly hang hoa cho cua hang kinh doanh gear cong nghe
- Cong nghe du kien su dung:
  - Python 3
  - Tkinter / ttk
  - SQL Server
  - pyodbc
  - Stored Procedure
- Mat hang quan ly:
  - Chuot gaming
  - Ban phim co
  - Tai nghe gaming
  - Ghe gaming
  - Micro
  - Man hinh

## 2. Cau truc project du kien

```text
QuanLyHangHoa/
|
├── main.py
|
├── config/
|   └── database.py
|
├── models/
|   └── hang_hoa.py
|
├── repositories/
|   └── hang_hoa_repository.py
|
├── services/
|   └── hang_hoa_service.py
|
├── views/
|   ├── main_window.py
|   ├── hang_hoa_view.py
|   └── thong_ke_view.py
|
├── utils/
|   ├── validators.py
|   └── helpers.py
|
├── sql/
|   └── database.sql
|
├── docs/
|   └── phan_cong_nhiem_vu.md
|
└── requirements.txt
```

## 3. Phan cong chi tiet

### THANH VIEN 1 - Truong nhom / Tich hop chuong trinh

Phu trach:

- main.py
- views/main_window.py
- utils/helpers.py
- Tao giao dien chinh
- Tich hop toan bo module
- Kiem tra chuong trinh cuoi cung
- Chuan bi demo

Noi dung thuyet trinh:

- Gioi thieu tong quan project
- Trinh bay kien truc chuong trinh
- Trinh bay luong chay tu main.py den giao dien chinh
- Demo menu chinh va qua trinh tich hop cac chuc nang

### THANH VIEN 2 - Co so du lieu SQL Server

Phu trach:

- config/database.py
- sql/database.sql
- Thiet ke database QuanLyGearCongNghe
- Tao bang DanhMuc
- Tao bang HangHoa
- Tao khoa chinh, khoa ngoai, CHECK, UNIQUE
- Tao Stored Procedure
- Them du lieu mau gear cong nghe

Noi dung thuyet trinh:

- Trinh bay thiet ke database QuanLyGearCongNghe
- Giai thich quan he giua bang DanhMuc va HangHoa
- Trinh bay cac rang buoc du lieu
- Trinh bay Stored Procedure dung cho CRUD, tim kiem, loc va thong ke

### THANH VIEN 3 - Quan ly danh muc hang hoa / CRUD

Phu trach:

- models/hang_hoa.py
- repositories/hang_hoa_repository.py
- services/hang_hoa_service.py
- views/hang_hoa_view.py
- Hien thi danh sach hang hoa
- Them hang hoa
- Sua hang hoa
- Xoa hang hoa
- Lam moi du lieu

Noi dung thuyet trinh:

- Trinh bay model HangHoa
- Trinh bay cach Repository goi database
- Trinh bay cach Service xu ly nghiep vu
- Demo cac chuc nang hien thi, them, sua, xoa va lam moi du lieu

### THANH VIEN 4 - Tim kiem, loc va kiem tra du lieu

Phu trach:

- utils/validators.py
- Mot phan repositories/hang_hoa_repository.py
- Mot phan services/hang_hoa_service.py
- Mot phan views/hang_hoa_view.py
- Tim kiem theo ma hang, ten hang, danh muc
- Loc theo danh muc, trang thai, khoang gia
- Kiem tra du lieu dau vao
- Hien thi thong bao loi tieng Viet

Noi dung thuyet trinh:

- Trinh bay cac ham kiem tra du lieu dau vao
- Giai thich cach tranh du lieu sai khi them hoac sua hang hoa
- Demo chuc nang tim kiem
- Demo chuc nang loc theo danh muc, trang thai va khoang gia

### THANH VIEN 5 - Thong ke tong so luong

Phu trach:

- views/thong_ke_view.py
- Mot phan repositories/hang_hoa_repository.py
- Hien thi tong so loai hang
- Hien thi tong so luong ton kho
- Hien thi tong gia tri ton kho
- Thong ke theo danh muc
- Co the them bieu do neu phu hop

Noi dung thuyet trinh:

- Trinh bay giao dien thong ke
- Giai thich cac chi so thong ke chinh
- Trinh bay truy van COUNT, SUM, GROUP BY
- Demo bang thong ke theo danh muc

## 4. Bang tong hop phan cong

| Thanh vien | Vai tro | File phu trach | Chuc nang phu trach | Noi dung thuyet trinh |
|---|---|---|---|---|
| Thanh vien 1 | Truong nhom / Tich hop chuong trinh | main.py, views/main_window.py, utils/helpers.py | Giao dien chinh, menu, tich hop module, kiem thu cuoi, chuan bi demo | Tong quan project, kien truc chuong trinh, luong chay chinh, demo menu |
| Thanh vien 2 | Co so du lieu SQL Server | config/database.py, sql/database.sql | Thiet ke database, bang DanhMuc, bang HangHoa, khoa, rang buoc, Stored Procedure, du lieu mau | Database QuanLyGearCongNghe, quan he bang, rang buoc, Stored Procedure |
| Thanh vien 3 | Quan ly danh muc hang hoa / CRUD | models/hang_hoa.py, repositories/hang_hoa_repository.py, services/hang_hoa_service.py, views/hang_hoa_view.py | Hien thi danh sach, them, sua, xoa, lam moi du lieu | Model, Repository, Service, demo CRUD |
| Thanh vien 4 | Tim kiem, loc va kiem tra du lieu | utils/validators.py, mot phan repositories/hang_hoa_repository.py, mot phan services/hang_hoa_service.py, mot phan views/hang_hoa_view.py | Tim kiem, loc, validation, thong bao loi tieng Viet | Kiem tra du lieu, tim kiem, loc, xu ly loi |
| Thanh vien 5 | Thong ke tong so luong | views/thong_ke_view.py, mot phan repositories/hang_hoa_repository.py | Tong so loai hang, tong so luong ton kho, tong gia tri ton kho, thong ke theo danh muc | Giao dien thong ke, COUNT, SUM, GROUP BY, demo thong ke |

## 5. Thu tu lam viec nhom

1. Thanh vien 2 lam database truoc.
2. Thanh vien 1 tao khung project va giao dien chinh.
3. Thanh vien 3 lam CRUD hang hoa.
4. Thanh vien 4 bo sung tim kiem, loc, validation.
5. Thanh vien 5 lam thong ke.
6. Thanh vien 1 tich hop va kiem thu toan bo.

## 6. Cau truc chuc nang cuoi cung

```text
DANH MUC
|
├── DANH MUC HANG HOA
|   ├── Hien thi danh sach
|   ├── Them hang hoa
|   ├── Sua hang hoa
|   ├── Xoa hang hoa
|   ├── Tim kiem
|   └── Loc
|
└── THONG KE TONG SO LUONG
    ├── Tong so loai hang hoa
    ├── Tong so luong ton kho
    ├── Tong gia tri ton kho
    └── Thong ke theo danh muc
```

## 7. Checklist kiem thu du kien

- Chay duoc chuong trinh bang lenh python main.py.
- Ket noi duoc SQL Server thong qua pyodbc.
- Khong lap lai connection string o nhieu file.
- Hien thi duoc danh sach hang hoa tren ttk.Treeview.
- Them hang hoa thanh cong voi du lieu hop le.
- Khong them duoc hang hoa khi ma hang trong.
- Khong them duoc hang hoa khi ten hang trong.
- Khong them duoc hang hoa khi danh muc trong.
- Khong them duoc hang hoa khi don gia nho hon 0.
- Khong them duoc hang hoa khi so luong nho hon 0.
- Sua thong tin hang hoa thanh cong.
- Xoa hang hoa thanh cong.
- Tim kiem duoc theo ma hang, ten hang, danh muc.
- Loc duoc theo danh muc.
- Loc duoc theo trang thai.
- Loc duoc theo khoang gia.
- Lam moi du lieu thanh cong.
- Hien thi dung tong so loai hang hoa.
- Hien thi dung tong so luong ton kho.
- Hien thi dung tong gia tri hang ton kho.
- Hien thi dung thong ke theo danh muc.
- Co messagebox thong bao loi hoac thanh cong bang tieng Viet.
- Khong viet SQL noi chuoi gay SQL Injection.
- Repository uu tien goi Stored Procedure.
- Tach ro GUI, Service, Repository, Database.

## 8. Ghi chu chat luong code khi trien khai

- Code phai chay duoc.
- Khong de TODO.
- Khong de pass trong function chinh.
- Khong viet pseudo-code.
- Co xu ly loi.
- Co messagebox thong bao loi/thanh cong bang tieng Viet.
- Khong viet SQL noi chuoi gay SQL Injection.
- Dung parameterized query hoac Stored Procedure.
- Tach ro GUI, Service, Repository, Database.
