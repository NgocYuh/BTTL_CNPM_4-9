/* QuanLyGearCongNghe - database setup for SQL Server */

IF DB_ID(N'QuanLyGearCongNghe') IS NULL
BEGIN
	CREATE DATABASE QuanLyGearCongNghe;
END;
GO

USE QuanLyGearCongNghe;
GO

IF OBJECT_ID(N'dbo.DanhMuc', N'U') IS NULL
BEGIN
	CREATE TABLE dbo.DanhMuc
	(
		MaDanhMuc VARCHAR(20) NOT NULL,
		TenDanhMuc NVARCHAR(100) NOT NULL,
		MoTa NVARCHAR(300) NULL,
		TrangThai BIT NOT NULL CONSTRAINT DF_DanhMuc_TrangThai DEFAULT (1),
		CONSTRAINT PK_DanhMuc PRIMARY KEY (MaDanhMuc),
		CONSTRAINT UQ_DanhMuc_Ten UNIQUE (TenDanhMuc)
	);
END;
GO

IF OBJECT_ID(N'dbo.HangHoa', N'U') IS NULL
BEGIN
	CREATE TABLE dbo.HangHoa
	(
		MaHang VARCHAR(20) NOT NULL,
		TenHang NVARCHAR(150) NOT NULL,
		MaDanhMuc VARCHAR(20) NOT NULL,
		DonGia DECIMAL(18, 2) NOT NULL,
		SoLuongTon INT NOT NULL CONSTRAINT DF_HangHoa_SoLuongTon DEFAULT (0),
		TrangThai BIT NOT NULL CONSTRAINT DF_HangHoa_TrangThai DEFAULT (1),
		MoTa NVARCHAR(500) NULL,
		HinhAnh NVARCHAR(500) NULL,
		NgayTao DATETIME2(0) NOT NULL CONSTRAINT DF_HangHoa_NgayTao DEFAULT (SYSDATETIME()),
		CONSTRAINT PK_HangHoa PRIMARY KEY (MaHang),
		CONSTRAINT CK_HangHoa_DonGia CHECK (DonGia >= 0),
		CONSTRAINT CK_HangHoa_SoLuongTon CHECK (SoLuongTon >= 0),
		CONSTRAINT FK_HangHoa_DanhMuc FOREIGN KEY (MaDanhMuc)
			REFERENCES dbo.DanhMuc(MaDanhMuc)
	);
END;
GO

IF COL_LENGTH(N'dbo.HangHoa', N'HinhAnh') IS NULL
BEGIN
	ALTER TABLE dbo.HangHoa ADD HinhAnh NVARCHAR(500) NULL;
END;
GO

INSERT INTO dbo.DanhMuc (MaDanhMuc, TenDanhMuc, MoTa)
SELECT v.MaDanhMuc, v.TenDanhMuc, v.MoTa
FROM (VALUES
	('DM01', N'Chuột gaming', N'Chuột dành cho chơi game'),
	('DM02', N'Bàn phím cơ', N'Bàn phím cơ gaming'),
	('DM03', N'Tai nghe gaming', N'Tai nghe và headset gaming'),
	('DM04', N'Ghế gaming', N'Ghế chuyên dụng cho game thủ'),
	('DM05', N'Micro', N'Micro thu âm và livestream'),
	('DM06', N'Màn hình', N'Màn hình máy tính gaming')
) AS v(MaDanhMuc, TenDanhMuc, MoTa)
WHERE NOT EXISTS (SELECT 1 FROM dbo.DanhMuc d WHERE d.MaDanhMuc = v.MaDanhMuc);
GO

INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, MoTa, HinhAnh)
SELECT v.MaHang, v.TenHang, v.MaDanhMuc, v.DonGia, v.SoLuongTon, v.MoTa
	, v.HinhAnh
FROM (VALUES
	('HH001', N'Logitech G502 X', 'DM01', 1590000, 20, N'Chuột gaming có dây', N'images/products/chuot-logitech-g502-x.jpg'),
	('HH002', N'Razer DeathAdder V3', 'DM01', 2490000, 14, N'Chuột gaming công thái học', N'images/products/chuot-razer-deathadder-v3.jpg'),
	('HH003', N'Corsair Katar Pro', 'DM01', 790000, 25, N'Chuột gaming nhỏ gọn', N'images/products/chuot-corsair-katar-pro.jpg'),
	('HH004', N'HyperX Pulsefire Haste 2', 'DM01', 1790000, 18, N'Chuột gaming siêu nhẹ', N'images/products/chuot-hyperx-pulsefire-haste-2.jpg'),
	('HH005', N'SteelSeries Rival 5', 'DM01', 1490000, 11, N'Chuột gaming đa nút', N'images/products/chuot-steelseries-rival-5.jpg'),
	('HH006', N'ASUS ROG Gladius III', 'DM01', 2290000, 9, N'Chuột gaming không dây', N'images/products/chuot-asus-rog-gladius-iii.jpg'),
	('HH007', N'Fantech Helios XD5', 'DM01', 990000, 22, N'Chuột gaming wireless', N'images/products/chuot-fantech-helios-xd5.jpg'),
	('HH008', N'Glorious Model O', 'DM01', 1690000, 13, N'Chuột gaming honeycomb', N'images/products/chuot-glorious-model-o.jpg'),
	('HH009', N'Logitech G Pro X Superlight 2', 'DM01', 3590000, 7, N'Chuột gaming chuyên nghiệp', N'images/products/chuot-logitech-g-pro-x-superlight-2.jpg'),
	('HH010', N'Zowie EC2-CW', 'DM01', 3190000, 5, N'Chuột gaming eSports', N'images/products/chuot-zowie-ec2-cw.jpg'),
	('HH011', N'Keychron K2 V2', 'DM02', 1890000, 15, N'Bàn phím cơ không dây', N'images/products/ban-phim-keychron-k2-v2.jpg'),
	('HH012', N'Akko 5075B Plus', 'DM02', 2190000, 12, N'Bàn phím cơ bluetooth', N'images/products/ban-phim-akko-5075b-plus.jpg'),
	('HH013', N'Leopold FC750R', 'DM02', 2890000, 8, N'Bàn phím cơ cao cấp', N'images/products/ban-phim-leopold-fc750r.jpg'),
	('HH014', N'Razer BlackWidow V4', 'DM02', 3990000, 10, N'Bàn phím cơ gaming RGB', N'images/products/ban-phim-razer-blackwidow-v4.jpg'),
	('HH015', N'Logitech G Pro X TKL', 'DM02', 3290000, 9, N'Bàn phím gaming không dây', N'images/products/ban-phim-logitech-g-pro-x-tkl.jpg'),
	('HH016', N'FL-Esports MK870', 'DM02', 1590000, 16, N'Bàn phím cơ layout TKL', N'images/products/ban-phim-fl-esports-mk870.jpg'),
	('HH017', N'NuPhy Air75 V2', 'DM02', 2790000, 6, N'Bàn phím cơ low profile', N'images/products/ban-phim-nuphy-air75-v2.jpg'),
	('HH018', N'Wooting 60HE+', 'DM02', 4490000, 4, N'Bàn phím magnetic switch', N'images/products/ban-phim-wooting-60he.jpg'),
	('HH019', N'Varmilo VA87M', 'DM02', 2390000, 7, N'Bàn phím cơ switch tĩnh', N'images/products/ban-phim-varmilo-va87m.jpg'),
	('HH020', N'Corsair K70 RGB Pro', 'DM02', 3790000, 8, N'Bàn phím cơ full size', N'images/products/ban-phim-corsair-k70-rgb-pro.jpg'),
	('HH021', N'HyperX Cloud III', 'DM03', 2190000, 12, N'Tai nghe gaming', N'images/products/tai-nghe-hyperx-cloud-iii.jpg'),
	('HH022', N'Logitech G Pro X 2', 'DM03', 4290000, 8, N'Tai nghe gaming không dây', N'images/products/tai-nghe-logitech-g-pro-x2.jpg'),
	('HH023', N'Razer BlackShark V2 Pro', 'DM03', 3590000, 10, N'Headset gaming wireless', N'images/products/tai-nghe-razer-blackshark-v2-pro.jpg'),
	('HH024', N'SteelSeries Arctis Nova 7', 'DM03', 3990000, 9, N'Tai nghe đa nền tảng', N'images/products/tai-nghe-steelseries-arctis-nova-7.jpg'),
	('HH025', N'Corsair HS80 RGB', 'DM03', 2690000, 13, N'Tai nghe gaming có mic', N'images/products/tai-nghe-corsair-hs80-rgb.jpg'),
	('HH026', N'ASUS ROG Cetra II', 'DM03', 1990000, 15, N'Tai nghe in-ear gaming', N'images/products/tai-nghe-asus-rog-cetra-ii.jpg'),
	('HH027', N'Fantech Sonata MH90', 'DM03', 690000, 20, N'Headset gaming giá tốt', N'images/products/tai-nghe-fantech-sonata-mh90.jpg'),
	('HH028', N'EPOS H6PRO', 'DM03', 2490000, 6, N'Tai nghe gaming audiophile', N'images/products/tai-nghe-epos-h6pro.jpg'),
	('HH029', N'Beyerdynamic MMX 300', 'DM03', 5990000, 3, N'Headset gaming cao cấp', N'images/products/tai-nghe-beyerdynamic-mmx-300.jpg'),
	('HH030', N'JBL Quantum 910', 'DM03', 4990000, 5, N'Tai nghe gaming chống ồn', N'images/products/tai-nghe-jbl-quantum-910.jpg'),
	('HH031', N'DXRacer Formula', 'DM04', 6490000, 8, N'Ghế gaming công thái học', N'images/products/ghe-dxracer-formula.jpg'),
	('HH032', N'AndaSeat Kaiser 3', 'DM04', 8990000, 5, N'Ghế gaming khung thép', N'images/products/ghe-andaseat-kaiser-3.jpg'),
	('HH033', N'AKRacing Core Series', 'DM04', 7290000, 6, N'Ghế gaming tựa lưng cao', N'images/products/ghe-akracing-core-series.jpg'),
	('HH034', N'Corsair TC100 Relaxed', 'DM04', 5990000, 7, N'Ghế gaming đệm rộng', N'images/products/ghe-corsair-tc100-relaxed.jpg'),
	('HH035', N'Secretlab TITAN Evo', 'DM04', 11990000, 4, N'Ghế gaming cao cấp', N'images/products/ghe-secretlab-titan-evo.jpg'),
	('HH036', N'Warrior WGC305', 'DM04', 3290000, 12, N'Ghế gaming phổ thông', N'images/products/ghe-warrior-wgc305.jpg'),
	('HH037', N'Cougar Armor One', 'DM04', 4290000, 9, N'Ghế gaming có gác chân', N'images/products/ghe-cougar-armor-one.jpg'),
	('HH038', N'HyperX Stealth', 'DM04', 6990000, 5, N'Ghế gaming đệm foam', N'images/products/ghe-hyperx-stealth.jpg'),
	('HH039', N'GT Racing GT099', 'DM04', 2890000, 14, N'Ghế gaming lưng cao', N'images/products/ghe-gt-racing-gt099.jpg'),
	('HH040', N'Autofull M6', 'DM04', 5590000, 6, N'Ghế gaming massage', N'images/products/ghe-autofull-m6.jpg'),
	('HH041', N'FIFINE AM8', 'DM05', 1690000, 10, N'Micro USB/XLR', N'images/products/micro-fifine-am8.jpg'),
	('HH042', N'Razer Seiren V3 Mini', 'DM05', 1390000, 12, N'Micro USB nhỏ gọn', N'images/products/micro-razer-seiren-v3-mini.jpg'),
	('HH043', N'Elgato Wave:3', 'DM05', 3490000, 8, N'Micro condenser livestream', N'images/products/micro-elgato-wave-3.jpg'),
	('HH044', N'HyperX QuadCast 2', 'DM05', 3990000, 7, N'Micro USB RGB', N'images/products/micro-hyperx-quadcast-2.jpg'),
	('HH045', N'Audio-Technica AT2020', 'DM05', 2890000, 6, N'Micro thu âm studio', N'images/products/micro-audio-technica-at2020.jpg'),
	('HH046', N'Maono PD200X', 'DM05', 1890000, 11, N'Micro dynamic USB/XLR', N'images/products/micro-maono-pd200x.jpg'),
	('HH047', N'Blue Yeti X', 'DM05', 3290000, 5, N'Micro podcast chuyên nghiệp', N'images/products/micro-blue-yeti-x.jpg'),
	('HH048', N'FIFINE K688', 'DM05', 1590000, 13, N'Micro dynamic USB', N'images/products/micro-fifine-k688.jpg'),
	('HH049', N'Shure MV7', 'DM05', 6990000, 3, N'Micro podcast USB/XLR', N'images/products/micro-shure-mv7.jpg'),
	('HH050', N'BOYA BY-PM700', 'DM05', 1790000, 9, N'Micro condenser đa hướng', N'images/products/micro-boya-by-pm700.jpg'),
	('HH051', N'LG UltraGear 27GN800', 'DM06', 7290000, 6, N'Màn hình gaming 27 inch', N'images/products/man-hinh-lg-ultragear-27gn800.jpg'),
	('HH052', N'ASUS TUF VG27AQ', 'DM06', 6990000, 8, N'Màn hình 2K 165Hz', N'images/products/man-hinh-asus-tuf-vg27aq.jpg'),
	('HH053', N'Samsung Odyssey G5', 'DM06', 6490000, 7, N'Màn hình gaming cong', N'images/products/man-hinh-samsung-odyssey-g5.jpg'),
	('HH054', N'Dell G2724D', 'DM06', 6790000, 5, N'Màn hình gaming 2K', N'images/products/man-hinh-dell-g2724d.jpg'),
	('HH055', N'Gigabyte M27Q', 'DM06', 7990000, 6, N'Màn hình gaming KVM', N'images/products/man-hinh-gigabyte-m27q.jpg'),
	('HH056', N'ViewSonic XG2431', 'DM06', 5990000, 9, N'Màn hình gaming 240Hz', N'images/products/man-hinh-viewsonic-xg2431.jpg'),
	('HH057', N'AOC 24G2SP', 'DM06', 4290000, 15, N'Màn hình gaming 24 inch', N'images/products/man-hinh-aoc-24g2sp.jpg'),
	('HH058', N'BenQ Zowie XL2546K', 'DM06', 8990000, 4, N'Màn hình eSports 240Hz', N'images/products/man-hinh-benq-xl2546k.jpg'),
	('HH059', N'MSI G274QPF-QD', 'DM06', 7490000, 7, N'Màn hình gaming quantum dot', N'images/products/man-hinh-msi-g274qpf-qd.jpg'),
	('HH060', N'Cooler Master GM27-CFX', 'DM06', 6290000, 8, N'Màn hình gaming cong 165Hz', N'images/products/man-hinh-coolermaster-gm27-cfx.jpg')
) AS v(MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, MoTa, HinhAnh)
WHERE NOT EXISTS (SELECT 1 FROM dbo.HangHoa h WHERE h.MaHang = v.MaHang);
GO

UPDATE h
SET HinhAnh = v.HinhAnh
FROM dbo.HangHoa h
INNER JOIN (VALUES
	('HH001', N'images/products/chuot-logitech-g502-x.jpg'),
	('HH002', N'images/products/ban-phim-keychron-k2-v2.jpg'),
	('HH003', N'images/products/tai-nghe-hyperx-cloud-iii.jpg'),
	('HH004', N'images/products/ghe-dxracer-formula.jpg'),
	('HH005', N'images/products/micro-fifine-am8.jpg'),
	('HH006', N'images/products/man-hinh-lg-ultragear-27gn800.jpg')
) AS v(MaHang, HinhAnh) ON h.MaHang = v.MaHang
WHERE h.HinhAnh IS NULL;
GO

CREATE OR ALTER PROCEDURE dbo.sp_DanhMuc_GetAll
AS
BEGIN
	SET NOCOUNT ON;
	SELECT MaDanhMuc, TenDanhMuc, MoTa, TrangThai FROM dbo.DanhMuc
	WHERE TrangThai = 1 ORDER BY TenDanhMuc;
END;
GO

CREATE OR ALTER PROCEDURE dbo.sp_HangHoa_GetAll
AS
BEGIN
	SET NOCOUNT ON;
	SELECT h.MaHang, h.TenHang, h.MaDanhMuc, d.TenDanhMuc, h.DonGia,
		   h.SoLuongTon, h.TrangThai, h.MoTa, h.HinhAnh, h.NgayTao
	FROM dbo.HangHoa h INNER JOIN dbo.DanhMuc d ON d.MaDanhMuc = h.MaDanhMuc
	ORDER BY h.MaHang;
END;
GO

CREATE OR ALTER PROCEDURE dbo.sp_HangHoa_Insert
	@MaHang VARCHAR(20), @TenHang NVARCHAR(150), @MaDanhMuc VARCHAR(20),
	@DonGia DECIMAL(18, 2), @SoLuongTon INT, @TrangThai BIT = 1,
	@MoTa NVARCHAR(500) = NULL, @HinhAnh NVARCHAR(500) = NULL
AS
BEGIN
	SET NOCOUNT ON;
	INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, TrangThai, MoTa, HinhAnh)
	VALUES (@MaHang, @TenHang, @MaDanhMuc, @DonGia, @SoLuongTon, @TrangThai, @MoTa, @HinhAnh);
END;
GO

CREATE OR ALTER PROCEDURE dbo.sp_HangHoa_Update
	@MaHang VARCHAR(20), @TenHang NVARCHAR(150), @MaDanhMuc VARCHAR(20),
	@DonGia DECIMAL(18, 2), @SoLuongTon INT, @TrangThai BIT = 1,
	@MoTa NVARCHAR(500) = NULL, @HinhAnh NVARCHAR(500) = NULL
AS
BEGIN
	SET NOCOUNT ON;
	UPDATE dbo.HangHoa SET TenHang = @TenHang, MaDanhMuc = @MaDanhMuc,
		DonGia = @DonGia, SoLuongTon = @SoLuongTon, TrangThai = @TrangThai,
		MoTa = @MoTa, HinhAnh = @HinhAnh
	WHERE MaHang = @MaHang;
	IF @@ROWCOUNT = 0 THROW 50001, N'Khong tim thay hang hoa.', 1;
END;
GO

CREATE OR ALTER PROCEDURE dbo.sp_HangHoa_Delete @MaHang VARCHAR(20)
AS
BEGIN
	SET NOCOUNT ON;
	DELETE FROM dbo.HangHoa WHERE MaHang = @MaHang;
	IF @@ROWCOUNT = 0 THROW 50001, N'Khong tim thay hang hoa.', 1;
END;
GO

CREATE OR ALTER PROCEDURE dbo.sp_HangHoa_SearchFilter
	@TuKhoa NVARCHAR(150) = NULL, @MaDanhMuc VARCHAR(20) = NULL,
	@TrangThai BIT = NULL, @GiaTu DECIMAL(18, 2) = NULL,
	@GiaDen DECIMAL(18, 2) = NULL
AS
BEGIN
	SET NOCOUNT ON;
	SELECT h.MaHang, h.TenHang, h.MaDanhMuc, d.TenDanhMuc, h.DonGia,
		   h.SoLuongTon, h.TrangThai, h.MoTa, h.HinhAnh, h.NgayTao
	FROM dbo.HangHoa h INNER JOIN dbo.DanhMuc d ON d.MaDanhMuc = h.MaDanhMuc
	WHERE (@TuKhoa IS NULL OR h.MaHang LIKE N'%' + @TuKhoa + N'%' OR h.TenHang LIKE N'%' + @TuKhoa + N'%' OR d.TenDanhMuc LIKE N'%' + @TuKhoa + N'%')
	  AND (@MaDanhMuc IS NULL OR h.MaDanhMuc = @MaDanhMuc)
	  AND (@TrangThai IS NULL OR h.TrangThai = @TrangThai)
	  AND (@GiaTu IS NULL OR h.DonGia >= @GiaTu)
	  AND (@GiaDen IS NULL OR h.DonGia <= @GiaDen)
	ORDER BY h.MaHang;
END;
GO

CREATE OR ALTER PROCEDURE dbo.sp_HangHoa_Statistics
AS
BEGIN
	SET NOCOUNT ON;
	SELECT COUNT(*) AS TongSoLoaiHang, COALESCE(SUM(SoLuongTon), 0) AS TongSoLuongTon,
		   COALESCE(SUM(DonGia * SoLuongTon), 0) AS TongGiaTriTonKho
	FROM dbo.HangHoa;
	SELECT d.MaDanhMuc, d.TenDanhMuc, COUNT(h.MaHang) AS SoLoaiHang,
		   COALESCE(SUM(h.SoLuongTon), 0) AS SoLuongTon,
		   COALESCE(SUM(h.DonGia * h.SoLuongTon), 0) AS GiaTriTonKho
	FROM dbo.DanhMuc d LEFT JOIN dbo.HangHoa h ON h.MaDanhMuc = d.MaDanhMuc
	GROUP BY d.MaDanhMuc, d.TenDanhMuc ORDER BY d.MaDanhMuc;
END;
GO
