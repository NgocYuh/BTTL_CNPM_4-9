"""
Repository: HangHoaRepository (Kho lưu trữ dữ liệu Hàng hóa & Thống kê)
Phụ trách: 
    - Thành viên 3 (TV3): Quản lý danh mục hàng hóa / CRUD
    - Thành viên 5 (TV5): Thống kê tổng số lượng & tồn kho
Dự án: QuanLyHangHoa (Cửa hàng kinh doanh Gear Công Nghệ)
Đồng bộ: Tương tác với SQL Server qua config.database và Stored Procedure của TV2
"""

import logging
from typing import Any, Dict, List, Optional

from config.database import get_connection
from models.hang_hoa import HangHoa

logger = logging.getLogger(__name__)


def _get_db_connection():
    """Hàm trợ giúp lấy kết nối CSDL từ config.database hoặc kết nối trực tiếp (hỗ trợ code TV5)."""
    try:
        conn = get_connection()
        if conn is not None:
            return conn
    except Exception:
        pass

    # Fallback kết nối trực tiếp nếu config.database chưa hoàn thiện hoặc dùng driver khác
    try:
        import pyodbc
        server = "localhost"
        database = "QuanLyGearCongNghe"
        drivers = [
            "ODBC Driver 18 for SQL Server",
            "ODBC Driver 17 for SQL Server",
            "SQL Server Native Client 11.0",
            "SQL Server",
        ]
        available_drivers = pyodbc.drivers()
        selected_driver = "SQL Server"
        for d in drivers:
            if d in available_drivers:
                selected_driver = d
                break

        conn_str = f"DRIVER={{{selected_driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        if "ODBC Driver 18" in selected_driver:
            conn_str += "TrustServerCertificate=yes;"
        return pyodbc.connect(conn_str, timeout=5)
    except Exception as exc:
        raise RuntimeError("Không thể kết nối SQL Server.") from exc


class HangHoaRepository:
    """
    Tầng Data Access Layer (DAL) chịu trách nhiệm tương tác trực tiếp với SQL Server:
        - Sử dụng Stored Procedures do TV2 định nghĩa:
            + sp_HangHoa_GetAll
            + sp_HangHoa_Insert
            + sp_HangHoa_Update
            + sp_HangHoa_Delete
            + sp_DanhMuc_GetAll
            + sp_HangHoa_Statistics
        - Tuyệt đối dùng Parameterized Query / Stored Procedure để ngăn ngừa SQL Injection.
        - Tự động đóng mở kết nối (Context Manager).
        - Cơ chế Mock Data dự phòng trong RAM khi chưa kết nối được CSDL (hỗ trợ dev & test offline).
    """

    # Danh mục gear mặc định theo thiết kế của TV2
    DEFAULT_DANH_MUC = [
        {"ma_danh_muc": "DM01", "ten_danh_muc": "Chuột gaming", "mo_ta": "Chuột dành cho chơi game"},
        {"ma_danh_muc": "DM02", "ten_danh_muc": "Bàn phím cơ", "mo_ta": "Bàn phím cơ gaming"},
        {"ma_danh_muc": "DM03", "ten_danh_muc": "Tai nghe gaming", "mo_ta": "Tai nghe và headset gaming"},
        {"ma_danh_muc": "DM04", "ten_danh_muc": "Ghế gaming", "mo_ta": "Ghế chuyên dụng cho game thủ"},
        {"ma_danh_muc": "DM05", "ten_danh_muc": "Micro", "mo_ta": "Micro thu âm và livestream"},
        {"ma_danh_muc": "DM06", "ten_danh_muc": "Màn hình", "mo_ta": "Màn hình máy tính gaming"},
    ]

    def __init__(self, use_mock_fallback: bool = True) -> None:
        """
        Khởi tạo Repository.
        Args:
            use_mock_fallback: Cho phép dùng dữ liệu bộ nhớ tạm nếu kết nối SQL Server thất bại.
        """
        self.use_mock_fallback = use_mock_fallback
        self._in_memory_db: List[HangHoa] = []
        self._is_db_connected: Optional[bool] = None
        self._init_mock_data()

    def _init_mock_data(self) -> None:
        """Khởi tạo danh sách dữ liệu mẫu gear công nghệ giống seed data của TV2."""
        sample_items = [
            ("HH001", "Logitech G502 X", "DM01", "Chuột gaming", 1590000.0, 20, 1, "Chuột gaming có dây"),
            ("HH002", "Keychron K2 V2", "DM02", "Bàn phím cơ", 1890000.0, 15, 1, "Bàn phím cơ không dây"),
            ("HH003", "HyperX Cloud III", "DM03", "Tai nghe gaming", 2190000.0, 12, 1, "Tai nghe gaming"),
            ("HH004", "DXRacer Formula", "DM04", "Ghế gaming", 6490000.0, 8, 1, "Ghế gaming công thái học"),
            ("HH005", "FIFINE AM8", "DM05", "Micro", 1690000.0, 10, 1, "Micro USB/XLR"),
            ("HH006", "LG UltraGear 27GN800", "DM06", "Màn hình", 7290000.0, 6, 1, "Màn hình gaming 27 inch"),
        ]
        self._in_memory_db = [
            HangHoa(
                ma_hang=item[0],
                ten_hang=item[1],
                ma_danh_muc=item[2],
                ten_danh_muc=item[3],
                don_gia=item[4],
                so_luong_ton=item[5],
                trang_thai=item[6],
                mo_ta=item[7],
            )
            for item in sample_items
        ]

    def is_connected(self) -> bool:
        """Kiểm tra xem hiện tại có kết nối được với SQL Server hay không."""
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1;")
                    cursor.fetchone()
            self._is_db_connected = True
            return True
        except Exception:
            self._is_db_connected = False
            return False

    # =========================================================================
    # 1. READ: LẤY DANH SÁCH & CHI TIẾT (TV3)
    # =========================================================================

    def get_all(self) -> List[HangHoa]:
        """
        Lấy tất cả hàng hóa trong hệ thống.
        Thực thi Stored Procedure: dbo.sp_HangHoa_GetAll
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    try:
                        cursor.execute("EXEC dbo.sp_HangHoa_GetAll;")
                    except Exception:
                        sql = """
                            SELECT h.MaHang, h.TenHang, h.MaDanhMuc, d.TenDanhMuc,
                                   h.DonGia, h.SoLuongTon, h.TrangThai, h.MoTa, h.NgayTao
                            FROM dbo.HangHoa h
                            INNER JOIN dbo.DanhMuc d ON d.MaDanhMuc = h.MaDanhMuc
                            ORDER BY h.MaHang;
                        """
                        cursor.execute(sql)

                    rows = cursor.fetchall()
                    result = [HangHoa.from_row(row) for row in rows]
                    self._is_db_connected = True
                    return result
        except Exception as error:
            logger.warning("Không thể kết nối SQL Server: %s", error)
            self._is_db_connected = False
            if self.use_mock_fallback:
                return list(self._in_memory_db)
            raise

    def get_by_id(self, ma_hang: str) -> Optional[HangHoa]:
        """Lấy thông tin chi tiết một mặt hàng theo mã hàng."""
        ma_hang = str(ma_hang).strip()
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = """
                        SELECT h.MaHang, h.TenHang, h.MaDanhMuc, d.TenDanhMuc,
                               h.DonGia, h.SoLuongTon, h.TrangThai, h.MoTa, h.NgayTao
                        FROM dbo.HangHoa h
                        INNER JOIN dbo.DanhMuc d ON d.MaDanhMuc = h.MaDanhMuc
                        WHERE h.MaHang = ?;
                    """
                    cursor.execute(sql, (ma_hang,))
                    row = cursor.fetchone()
                    if row:
                        return HangHoa.from_row(row)
                    return None
        except Exception as error:
            logger.warning("Không thể kết nối SQL Server: %s", error)
            if self.use_mock_fallback:
                for item in self._in_memory_db:
                    if item.ma_hang.upper() == ma_hang.upper():
                        return item
                return None
            raise

    def check_exists(self, ma_hang: str) -> bool:
        """Kiểm tra mã hàng đã tồn tại trong CSDL hay chưa."""
        ma_hang = str(ma_hang).strip()
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT 1 FROM dbo.HangHoa WHERE MaHang = ?;"
                    cursor.execute(sql, (ma_hang,))
                    row = cursor.fetchone()
                    return row is not None
        except Exception as error:
            logger.warning("Không thể kết nối SQL Server: %s", error)
            if self.use_mock_fallback:
                return any(item.ma_hang.upper() == ma_hang.upper() for item in self._in_memory_db)
            raise

    # =========================================================================
    # 2. CREATE: THÊM MỚI HÀNG HÓA (TV3)
    # =========================================================================

    def insert(self, hang_hoa: HangHoa) -> bool:
        """
        Thêm một mặt hàng mới vào cơ sở dữ liệu.
        Thực thi Stored Procedure: dbo.sp_HangHoa_Insert
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    params = (
                        hang_hoa.ma_hang,
                        hang_hoa.ten_hang,
                        hang_hoa.ma_danh_muc,
                        hang_hoa.don_gia,
                        hang_hoa.so_luong_ton,
                        hang_hoa.trang_thai_bit,
                        hang_hoa.mo_ta,
                    )
                    try:
                        cursor.execute("EXEC dbo.sp_HangHoa_Insert ?, ?, ?, ?, ?, ?, ?;", params)
                    except Exception:
                        sql = """
                            INSERT INTO dbo.HangHoa (MaHang, TenHang, MaDanhMuc, DonGia, SoLuongTon, TrangThai, MoTa)
                            VALUES (?, ?, ?, ?, ?, ?, ?);
                        """
                        cursor.execute(sql, params)

                    conn.commit()
                    return True
        except Exception as error:
            logger.warning("Không thể thêm vào SQL Server: %s", error)
            if self.use_mock_fallback:
                if any(x.ma_hang.upper() == hang_hoa.ma_hang.upper() for x in self._in_memory_db):
                    raise ValueError(f"Mã hàng hóa '{hang_hoa.ma_hang}' đã tồn tại.")
                if not hang_hoa.ten_danh_muc:
                    dm = next((d for d in self.DEFAULT_DANH_MUC if d["ma_danh_muc"] == hang_hoa.ma_danh_muc), None)
                    if dm:
                        hang_hoa.ten_danh_muc = dm["ten_danh_muc"]
                self._in_memory_db.append(hang_hoa)
                return True
            raise

    # =========================================================================
    # 3. UPDATE: SỬA HÀNG HÓA (TV3)
    # =========================================================================

    def update(self, hang_hoa: HangHoa) -> bool:
        """
        Cập nhật thông tin hàng hóa.
        Thực thi Stored Procedure: dbo.sp_HangHoa_Update
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    params = (
                        hang_hoa.ma_hang,
                        hang_hoa.ten_hang,
                        hang_hoa.ma_danh_muc,
                        hang_hoa.don_gia,
                        hang_hoa.so_luong_ton,
                        hang_hoa.trang_thai_bit,
                        hang_hoa.mo_ta,
                    )
                    try:
                        cursor.execute("EXEC dbo.sp_HangHoa_Update ?, ?, ?, ?, ?, ?, ?;", params)
                    except Exception:
                        sql = """
                            UPDATE dbo.HangHoa
                            SET TenHang = ?, MaDanhMuc = ?, DonGia = ?, SoLuongTon = ?, TrangThai = ?, MoTa = ?
                            WHERE MaHang = ?;
                        """
                        update_params = (
                            hang_hoa.ten_hang,
                            hang_hoa.ma_danh_muc,
                            hang_hoa.don_gia,
                            hang_hoa.so_luong_ton,
                            hang_hoa.trang_thai_bit,
                            hang_hoa.mo_ta,
                            hang_hoa.ma_hang,
                        )
                        cursor.execute(sql, update_params)

                    conn.commit()
                    return True
        except Exception as error:
            logger.warning("Không thể cập nhật vào SQL Server: %s", error)
            if self.use_mock_fallback:
                for idx, item in enumerate(self._in_memory_db):
                    if item.ma_hang.upper() == hang_hoa.ma_hang.upper():
                        if not hang_hoa.ten_danh_muc:
                            dm = next((d for d in self.DEFAULT_DANH_MUC if d["ma_danh_muc"] == hang_hoa.ma_danh_muc), None)
                            if dm:
                                hang_hoa.ten_danh_muc = dm["ten_danh_muc"]
                        self._in_memory_db[idx] = hang_hoa
                        return True
                raise ValueError(f"Không tìm thấy hàng hóa với mã '{hang_hoa.ma_hang}'.")
            raise

    # =========================================================================
    # 4. DELETE: XÓA HÀNG HÓA (TV3)
    # =========================================================================

    def delete(self, ma_hang: str) -> bool:
        """
        Xóa hàng hóa theo mã hàng.
        Thực thi Stored Procedure: dbo.sp_HangHoa_Delete
        """
        ma_hang = str(ma_hang).strip()
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    try:
                        cursor.execute("EXEC dbo.sp_HangHoa_Delete ?;", (ma_hang,))
                    except Exception:
                        cursor.execute("DELETE FROM dbo.HangHoa WHERE MaHang = ?;", (ma_hang,))

                    conn.commit()
                    return True
        except Exception as error:
            logger.warning("Không thể xóa khỏi SQL Server: %s", error)
            if self.use_mock_fallback:
                initial_len = len(self._in_memory_db)
                self._in_memory_db = [x for x in self._in_memory_db if x.ma_hang.upper() != ma_hang.upper()]
                if len(self._in_memory_db) < initial_len:
                    return True
                raise ValueError(f"Không tìm thấy hàng hóa với mã '{ma_hang}'.")
            raise

    # =========================================================================
    # 5. TIỆN ÍCH: LẤY DANH MỤC (HỖ TRỢ VIEW COMBOBOX)
    # =========================================================================

    def get_all_danh_muc(self) -> List[Dict[str, str]]:
        """
        Lấy danh sách các danh mục hàng hóa đang hoạt động để đổ vào Combobox.
        Thực thi Stored Procedure: dbo.sp_DanhMuc_GetAll
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    try:
                        cursor.execute("EXEC dbo.sp_DanhMuc_GetAll;")
                    except Exception:
                        cursor.execute("SELECT MaDanhMuc, TenDanhMuc FROM dbo.DanhMuc WHERE TrangThai = 1 ORDER BY TenDanhMuc;")

                    rows = cursor.fetchall()
                    result = []
                    for row in rows:
                        ma_dm = getattr(row, "MaDanhMuc", row[0])
                        ten_dm = getattr(row, "TenDanhMuc", row[1])
                        result.append({"ma_danh_muc": str(ma_dm), "ten_danh_muc": str(ten_dm)})
                    return result
        except Exception as error:
            logger.warning("Không thể tải danh mục từ SQL Server: %s", error)
            return list(self.DEFAULT_DANH_MUC)

    # =========================================================================
    # 6. CÁC PHƯƠNG THỨC THỐNG KÊ (THÀNH VIÊN 5)
    # =========================================================================

    def get_total_product_types(self) -> int:
        """Lấy tổng số loại hàng (tổng số bản ghi hàng hóa trong HangHoa)."""
        try:
            conn = _get_db_connection()
            try:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT COUNT(*) AS TongSoLoaiHang FROM dbo.HangHoa;")
                    row = cursor.fetchone()
                except Exception:
                    cursor.execute("{CALL sp_ThongKe_TongSoLoaiHang}")
                    row = cursor.fetchone()

                if row and row[0] is not None:
                    return int(row[0])
                return 0
            finally:
                conn.close()
        except Exception as error:
            logger.warning("Không thể truy vấn CSDL cho thống kê số loại hàng: %s", error)
            if self.use_mock_fallback:
                return len(self._in_memory_db)
            return 0

    def get_total_quantity(self) -> int:
        """Lấy tổng số lượng hàng tồn kho."""
        try:
            conn = _get_db_connection()
            try:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT COALESCE(SUM(SoLuongTon), 0) AS TongSoLuong FROM dbo.HangHoa;")
                    row = cursor.fetchone()
                except Exception:
                    cursor.execute("SELECT COALESCE(SUM(SoLuong), 0) AS TongSoLuong FROM dbo.HangHoa;")
                    row = cursor.fetchone()

                if row and row[0] is not None:
                    return int(row[0])
                return 0
            finally:
                conn.close()
        except Exception as error:
            logger.warning("Không thể truy vấn CSDL cho thống kê tổng số lượng: %s", error)
            if self.use_mock_fallback:
                return sum(x.so_luong_ton for x in self._in_memory_db)
            return 0

    def get_total_inventory_value(self) -> float:
        """Lấy tổng giá trị tồn kho = SUM(DonGia * SoLuongTon)."""
        try:
            conn = _get_db_connection()
            try:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT COALESCE(SUM(DonGia * SoLuongTon), 0) AS TongGiaTriTonKho FROM dbo.HangHoa;")
                    row = cursor.fetchone()
                except Exception:
                    cursor.execute("SELECT COALESCE(SUM(DonGia * SoLuong), 0) AS TongGiaTriTonKho FROM dbo.HangHoa;")
                    row = cursor.fetchone()

                if row and row[0] is not None:
                    return float(row[0])
                return 0.0
            finally:
                conn.close()
        except Exception as error:
            logger.warning("Không thể truy vấn CSDL cho thống kê tổng giá trị: %s", error)
            if self.use_mock_fallback:
                return sum(x.don_gia * x.so_luong_ton for x in self._in_memory_db)
            return 0.0

    def get_statistics_by_category(self) -> List[Dict[str, Any]]:
        """
        Lấy thống kê theo từng danh mục:
        Mã danh mục, Tên danh mục, Số loại hàng, Tổng số lượng, Tổng giá trị.
        """
        try:
            conn = _get_db_connection()
            try:
                cursor = conn.cursor()
                sql = """
                    SELECT
                        dm.MaDanhMuc,
                        dm.TenDanhMuc,
                        COUNT(hh.MaHang) AS SoLoaiHang,
                        COALESCE(SUM(hh.SoLuongTon), 0) AS TongSoLuong,
                        COALESCE(SUM(hh.DonGia * hh.SoLuongTon), 0) AS TongGiaTri
                    FROM dbo.DanhMuc dm
                    LEFT JOIN dbo.HangHoa hh ON dm.MaDanhMuc = hh.MaDanhMuc
                    GROUP BY dm.MaDanhMuc, dm.TenDanhMuc
                    ORDER BY dm.MaDanhMuc;
                """
                cursor.execute(sql)
                rows = cursor.fetchall()

                result = []
                for row in rows:
                    result.append({
                        "MaDanhMuc": row[0] if row[0] is not None else "",
                        "TenDanhMuc": row[1] if row[1] is not None else "",
                        "SoLoaiHang": int(row[2]) if row[2] is not None else 0,
                        "TongSoLuong": int(row[3]) if row[3] is not None else 0,
                        "TongGiaTri": float(row[4]) if row[4] is not None else 0.0,
                    })
                return result
            finally:
                conn.close()
        except Exception as error:
            logger.warning("Không thể truy vấn CSDL cho thống kê theo danh mục: %s", error)
            if self.use_mock_fallback:
                result = []
                for dm in self.DEFAULT_DANH_MUC:
                    items = [x for x in self._in_memory_db if x.ma_danh_muc == dm["ma_danh_muc"]]
                    result.append({
                        "MaDanhMuc": dm["ma_danh_muc"],
                        "TenDanhMuc": dm["ten_danh_muc"],
                        "SoLoaiHang": len(items),
                        "TongSoLuong": sum(x.so_luong_ton for x in items),
                        "TongGiaTri": sum(x.don_gia * x.so_luong_ton for x in items),
                    })
                return result
            return []
