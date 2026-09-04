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
		NgayTao DATETIME2(0) NOT NULL CONSTRAINT DF_HangHoa_NgayTao DEFAULT (SYSDATETIME()),
		CONSTRAINT PK_HangHoa PRIMARY KEY (MaHang),
		CONSTRAINT CK_HangHoa_DonGia CHECK (DonGia >= 0),
		CONSTRAINT CK_HangHoa_SoLuongTon CHECK (SoLuongTon >= 0),
		CONSTRAINT FK_HangHoa_DanhMuc FOREIGN KEY (MaDanhMuc)
			REFERENCES dbo.DanhMuc(MaDanhMuc)
	);
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

INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, MoTa)
SELECT v.MaHang, v.TenHang, v.MaDanhMuc, v.DonGia, v.SoLuongTon, v.MoTa
FROM (VALUES
	('HH001', N'Logitech G502 X', 'DM01', 1590000, 20, N'Chuột gaming có dây'),
	('HH002', N'Keychron K2 V2', 'DM02', 1890000, 15, N'Bàn phím cơ không dây'),
	('HH003', N'HyperX Cloud III', 'DM03', 2190000, 12, N'Tai nghe gaming'),
	('HH004', N'DXRacer Formula', 'DM04', 6490000, 8, N'Ghế gaming công thái học'),
	('HH005', N'FIFINE AM8', 'DM05', 1690000, 10, N'Micro USB/XLR'),
	('HH006', N'LG UltraGear 27GN800', 'DM06', 7290000, 6, N'Màn hình gaming 27 inch')
) AS v(MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, MoTa)
WHERE NOT EXISTS (SELECT 1 FROM dbo.HangHoa h WHERE h.MaHang = v.MaHang);
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
		   h.SoLuongTon, h.TrangThai, h.MoTa, h.NgayTao
	FROM dbo.HangHoa h INNER JOIN dbo.DanhMuc d ON d.MaDanhMuc = h.MaDanhMuc
	ORDER BY h.MaHang;
END;
GO

CREATE OR ALTER PROCEDURE dbo.sp_HangHoa_Insert
	@MaHang VARCHAR(20), @TenHang NVARCHAR(150), @MaDanhMuc VARCHAR(20),
	@DonGia DECIMAL(18, 2), @SoLuongTon INT, @TrangThai BIT = 1,
	@MoTa NVARCHAR(500) = NULL
AS
BEGIN
	SET NOCOUNT ON;
	INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, TrangThai, MoTa)
	VALUES (@MaHang, @TenHang, @MaDanhMuc, @DonGia, @SoLuongTon, @TrangThai, @MoTa);
END;
GO

CREATE OR ALTER PROCEDURE dbo.sp_HangHoa_Update
	@MaHang VARCHAR(20), @TenHang NVARCHAR(150), @MaDanhMuc VARCHAR(20),
	@DonGia DECIMAL(18, 2), @SoLuongTon INT, @TrangThai BIT = 1,
	@MoTa NVARCHAR(500) = NULL
AS
BEGIN
	SET NOCOUNT ON;
	UPDATE dbo.HangHoa SET TenHang = @TenHang, MaDanhMuc = @MaDanhMuc,
		DonGia = @DonGia, SoLuongTon = @SoLuongTon, TrangThai = @TrangThai, MoTa = @MoTa
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
		   h.SoLuongTon, h.TrangThai, h.MoTa, h.NgayTao
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
