"""
Module: repositories.hang_hoa_repository
Phụ trách: Thành viên 3, 4 (CRUD, tìm kiếm, lọc) & Thành viên 5 (Thống kê)
"""

from typing import List, Dict, Any, Optional


def _get_db_connection():
    """Hàm trợ giúp lấy kết nối CSDL từ config.database hoặc kết nối trực tiếp."""
    try:
        from config.database import get_connection
        conn = get_connection()
        if conn is not None:
            return conn
    except Exception:
        pass

    # Fallback kết nối trực tiếp nếu config.database chưa được Thành viên 2 hoàn thiện
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


class HangHoaRepository:
    """Repository quản lý dữ liệu hàng hóa và thống kê."""

    def __init__(self):
        pass

    # =========================================================================
    # CÁC PHƯƠNG THỨC THỐNG KÊ - MODULE THÀNH VIÊN 5
    # =========================================================================

    def get_total_product_types(self) -> int:
        """Lấy tổng số loại hàng (tổng số bản ghi hàng hóa trong HangHoa)."""
        conn = _get_db_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute("{CALL sp_ThongKe_TongSoLoaiHang}")
                row = cursor.fetchone()
            except Exception:
                cursor.execute("SELECT COUNT(*) AS TongSoLoaiHang FROM HangHoa;")
                row = cursor.fetchone()

            if row and row[0] is not None:
                return int(row[0])
            return 0
        finally:
            conn.close()

    def get_total_quantity(self) -> int:
        """Lấy tổng số lượng hàng tồn kho."""
        conn = _get_db_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute("{CALL sp_ThongKe_TongSoLuong}")
                row = cursor.fetchone()
            except Exception:
                cursor.execute("SELECT COALESCE(SUM(SoLuong), 0) AS TongSoLuong FROM HangHoa;")
                row = cursor.fetchone()

            if row and row[0] is not None:
                return int(row[0])
            return 0
        finally:
            conn.close()

    def get_total_inventory_value(self) -> float:
        """Lấy tổng giá trị tồn kho = SUM(DonGia * SoLuong)."""
        conn = _get_db_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute("{CALL sp_ThongKe_TongGiaTriTonKho}")
                row = cursor.fetchone()
            except Exception:
                cursor.execute("SELECT COALESCE(SUM(DonGia * SoLuong), 0) AS TongGiaTriTonKho FROM HangHoa;")
                row = cursor.fetchone()

            if row and row[0] is not None:
                return float(row[0])
            return 0.0
        finally:
            conn.close()

    def get_statistics_by_category(self) -> List[Dict[str, Any]]:
        """
        Lấy thống kê theo từng danh mục:
        Mã danh mục, Tên danh mục, Số loại hàng, Tổng số lượng, Tổng giá trị.
        Dùng LEFT JOIN để giữ lại danh mục chưa có sản phẩm.
        """
        conn = _get_db_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute("{CALL sp_ThongKe_TheoDanhMuc}")
                rows = cursor.fetchall()
            except Exception:
                sql = """
                    SELECT
                        dm.MaDanhMuc,
                        dm.TenDanhMuc,
                        COUNT(hh.MaHang) AS SoLoaiHang,
                        COALESCE(SUM(hh.SoLuong), 0) AS TongSoLuong,
                        COALESCE(SUM(hh.DonGia * hh.SoLuong), 0) AS TongGiaTri
                    FROM DanhMuc dm
                    LEFT JOIN HangHoa hh
                        ON dm.MaDanhMuc = hh.MaDanhMuc
                    GROUP BY
                        dm.MaDanhMuc,
                        dm.TenDanhMuc
                    ORDER BY
                        dm.TenDanhMuc;
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
