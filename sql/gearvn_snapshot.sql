/* GearVN snapshot collected 2026-09-04. Prices and availability are not realtime. */
USE QuanLyGearCongNghe;
GO
IF COL_LENGTH(N'dbo.HangHoa', N'NguonDuLieu') IS NULL ALTER TABLE dbo.HangHoa ADD NguonDuLieu NVARCHAR(500) NULL;
GO

/* Verified GearVN snapshot examples collected on 2026-09-04. */
IF NOT EXISTS (SELECT 1 FROM dbo.HangHoa WHERE MaHang = 'GVN0601')
	INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, TrangThai, MoTa, HinhAnh, NguonDuLieu)
	VALUES ('GVN0601', N'Màn hình LG 27U730B-B 27 inch IPS 4K HDR10 USBC chuyên đồ họa', 'DM06', 8790000, 10, 1,
		N'Snapshot GearVN: IPS 4K, 60 Hz, 5 ms, USB-C 65 W.',
		N'https://cdn.hstatic.net/products/200000722513/man-hinh-lg-27u730b-b-27-ips-4k-hdr10-usbc-chuyen-do-hoa-1_f299a33162ec40c6accf565c98818d28.jpg',
		N'https://gearvn.com/products/man-hinh-lg-27u730b-b-27-ips-4k-hdr10-usbc-chuyen-do-hoa');

IF NOT EXISTS (SELECT 1 FROM dbo.HangHoa WHERE MaHang = 'GVN0602')
	INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, TrangThai, MoTa, HinhAnh, NguonDuLieu)
	VALUES ('GVN0602', N'Màn hình LG 27U711B-B 27 inch IPS 4K HDR10', 'DM06', 5690000, 10, 1,
		N'Snapshot GearVN: IPS 4K, 60 Hz, 5 ms, DCI-P3 90%.',
		N'https://cdn.hstatic.net/products/200000722513/man-hinh-lg-27u711b-b-27-ips-4k-hdr10-1_d6f635458b6a493ebdc56a7a9516dbdc.jpg',
		N'https://gearvn.com/products/man-hinh-lg-27u711b-b-27-ips-4k-hdr10');

IF NOT EXISTS (SELECT 1 FROM dbo.HangHoa WHERE MaHang = 'GVN0603')
	INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, TrangThai, MoTa, HinhAnh, NguonDuLieu)
	VALUES ('GVN0603', N'Màn hình VSP G2410QS 24 inch IPS 2K 100Hz USBC', 'DM06', 3190000, 10, 1,
		N'Snapshot GearVN: IPS 2K, 100 Hz, USB-C PD 65 W.',
		N'https://cdn.hstatic.net/products/200000722513/man-hinh-vsp-g2410qs-24-ips-2k-100hz-usbc-1_0a92c7fc0b6844c8891daa5cfd8f2fe8.jpg',
		N'https://gearvn.com/products/man-hinh-vsp-g2410qs-24-ips-2k-100hz-usbc');

IF NOT EXISTS (SELECT 1 FROM dbo.HangHoa WHERE MaHang = 'GVN0604')
	INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, TrangThai, MoTa, HinhAnh, NguonDuLieu)
	VALUES ('GVN0604', N'Màn hình ASUS TUF GAMING VG27AQME5F 27 inch Fast IPS 2K 255Hz', 'DM06', 5190000, 10, 1,
		N'Snapshot GearVN: Fast IPS 2K, 255 Hz, phản hồi 0.3 ms.',
		N'https://cdn.hstatic.net/products/200000722513/man-hinh-asus-tuf-gaming-vg27aqme5f-27-fast-ips-2k-255hz-chuyen-game-1_7d1f5073a43c41278c9a276dd217ab20.jpg',
		N'https://gearvn.com/products/man-hinh-asus-tuf-gaming-vg27aqme5f-27-fast-ips-2k-255hz-chuyen-game');

IF NOT EXISTS (SELECT 1 FROM dbo.HangHoa WHERE MaHang = 'GVN0605')
	INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, TrangThai, MoTa, HinhAnh, NguonDuLieu)
	VALUES ('GVN0605', N'Màn hình BenQ Zowie XL2586X+ 25 inch 600Hz DyAc 2', 'DM06', 29990000, 10, 1,
		N'Snapshot GearVN: Fast TN Full HD, 600 Hz, DyAc 2.',
		N'https://cdn.hstatic.net/products/200000722513/man-hinh-benq-zowie-xl2586x-25-600hz-dyac-2-chuyen-game-1_0844b15233d349ca8e56cc4a13934efb.jpg',
		N'https://gearvn.com/products/man-hinh-benq-zowie-xl2586x-25-600hz-dyac-2-chuyen-game');

UPDATE dbo.HangHoa
SET TenHang = N'Màn hình LG 27U730B-B 27 inch IPS 4K HDR10 USBC chuyên đồ họa',
	DonGia = 8790000,
	HinhAnh = N'images/products/man-hinh-lg-ultragear-27gn800.jpg',
	NguonDuLieu = N'https://gearvn.com/products/man-hinh-lg-27u730b-b-27-ips-4k-hdr10-usbc-chuyen-do-hoa'
WHERE MaHang = 'HH051';

UPDATE dbo.HangHoa
SET TenHang = N'Màn hình LG 27U711B-B 27 inch IPS 4K HDR10',
	DonGia = 5690000,
	HinhAnh = N'images/products/man-hinh-asus-tuf-vg27aq.jpg',
	NguonDuLieu = N'https://gearvn.com/products/man-hinh-lg-27u711b-b-27-ips-4k-hdr10'
WHERE MaHang = 'HH052';

UPDATE dbo.HangHoa
SET TenHang = N'Màn hình VSP G2410QS 24 inch IPS 2K 100Hz USBC',
	DonGia = 3190000,
	HinhAnh = N'images/products/man-hinh-samsung-odyssey-g5.jpg',
	NguonDuLieu = N'https://gearvn.com/products/man-hinh-vsp-g2410qs-24-ips-2k-100hz-usbc'
WHERE MaHang = 'HH053';

UPDATE dbo.HangHoa
SET TenHang = N'Màn hình ASUS TUF GAMING VG27AQME5F 27 inch Fast IPS 2K 255Hz',
	DonGia = 5190000,
	HinhAnh = N'images/products/man-hinh-dell-g2724d.jpg',
	NguonDuLieu = N'https://gearvn.com/products/man-hinh-asus-tuf-gaming-vg27aqme5f-27-fast-ips-2k-255hz-chuyen-game'
WHERE MaHang = 'HH054';

UPDATE dbo.HangHoa
SET TenHang = N'Màn hình BenQ Zowie XL2586X+ 25 inch 600Hz DyAc 2',
	DonGia = 29990000,
	HinhAnh = N'images/products/man-hinh-gigabyte-m27q.jpg',
	NguonDuLieu = N'https://gearvn.com/products/man-hinh-benq-zowie-xl2586x-25-600hz-dyac-2-chuyen-game'
WHERE MaHang = 'HH055';
GO

