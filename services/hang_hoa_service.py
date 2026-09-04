"""
Service: HangHoaService (Tầng xử lý nghiệp vụ Hàng hóa)
Phụ trách chính: Thành viên 3 (TV3) - Quản lý danh mục hàng hóa / CRUD
Đồng hành: Thành viên 4 (TV4) - Tìm kiếm, lọc và validation nâng cao
Dự án: QuanLyHangHoa (Cửa hàng kinh doanh Gear Công Nghệ)
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from models.hang_hoa import HangHoa
from repositories.hang_hoa_repository import HangHoaRepository

logger = logging.getLogger(__name__)


class HangHoaService:
    """
    Tầng Business Logic Layer (BLL) xử lý các nghiệp vụ quản lý hàng hóa:
        - Kiểm tra tính hợp lệ dữ liệu (Mã không rỗng, Tên không rỗng, Đơn giá >= 0, Số lượng >= 0).
        - Kiểm tra trùng lặp khóa chính trước khi thêm mới.
        - Điều hướng các thao tác Thêm, Sửa, Xóa, Đọc danh sách xuống tầng Repository.
        - Chuẩn hóa kết quả trả về cho View dưới dạng: (thanh_cong: bool, thong_bao: str, du_lieu: Any).
    """

    def __init__(self, repository: Optional[HangHoaRepository] = None) -> None:
        """Khởi tạo Service với Repository tương ứng (hỗ trợ Dependency Injection)."""
        self.repository = repository if repository is not None else HangHoaRepository()

    # =========================================================================
    # 1. READ: LẤY DANH SÁCH & CHI TIẾT
    # =========================================================================

    def lay_danh_sach_hang_hoa(self) -> Tuple[bool, str, List[HangHoa]]:
        """
        Lấy danh sách tất cả hàng hóa hiện có trong hệ thống.
        Returns:
            (True, "Thành công", danh_sach_hang_hoa) hoặc (False, "Thông báo lỗi", [])
        """
        try:
            danh_sach = self.repository.get_all()
            return True, f"Tải thành công {len(danh_sach)} mặt hàng.", danh_sach
        except Exception as error:
            logger.error("Lỗi khi lấy danh sách hàng hóa: %s", error)
            return False, f"Không thể tải danh sách hàng hóa: {str(error)}", []

    def lay_chi_tiet_hang_hoa(self, ma_hang: str) -> Tuple[bool, str, Optional[HangHoa]]:
        """
        Lấy thông tin chi tiết một mặt hàng theo mã hàng.
        """
        if not ma_hang or not ma_hang.strip():
            return False, "Mã hàng hóa không được để trống.", None

        ma_hang = ma_hang.strip()
        try:
            hang_hoa = self.repository.get_by_id(ma_hang)
            if hang_hoa:
                return True, "Tìm thấy thông tin hàng hóa.", hang_hoa
            return False, f"Không tìm thấy hàng hóa có mã '{ma_hang}'.", None
        except Exception as error:
            logger.error("Lỗi khi tìm hàng hóa '%s': %s", ma_hang, error)
            return False, f"Lỗi truy vấn hàng hóa: {str(error)}", None

    def lay_danh_sach_danh_muc(self) -> List[Dict[str, str]]:
        """Lấy danh sách danh mục để nạp vào Combobox của giao diện."""
        try:
            return self.repository.get_all_danh_muc()
        except Exception as error:
            logger.error("Lỗi khi lấy danh mục: %s", error)
            return self.repository.DEFAULT_DANH_MUC

    # =========================================================================
    # 2. VALIDATION NGHIỆP VỤ (ĐỒNG BỘ VỚI TV4 - utils.validators)
    # =========================================================================

    def kiem_tra_du_lieu_hang_hoa(self, hang_hoa: HangHoa, is_update: bool = False) -> Tuple[bool, str]:
        """
        Kiểm tra tính hợp lệ của dữ liệu hàng hóa trước khi lưu vào CSDL.
        Sử dụng trực tiếp các hàm validation từ utils.validators của TV4.
        """
        try:
            from utils.validators import validate_hang_hoa
            hop_le, msg = validate_hang_hoa(
                ma_hang=hang_hoa.ma_hang,
                ten_hang=hang_hoa.ten_hang,
                ma_danh_muc=hang_hoa.ma_danh_muc,
                don_gia=hang_hoa.don_gia,
                so_luong=hang_hoa.so_luong_ton,
            )
            if not hop_le:
                return False, msg
        except ImportError:
            # Fallback kiểm tra nội bộ nếu utils.validators chưa có sẵn
            if not hang_hoa.ma_hang or not hang_hoa.ma_hang.strip():
                return False, "Mã hàng hóa không được để trống."
            if len(hang_hoa.ma_hang.strip()) > 20:
                return False, "Mã hàng hóa không được vượt quá 20 ký tự."
            if not hang_hoa.ten_hang or not hang_hoa.ten_hang.strip():
                return False, "Tên hàng hóa không được để trống."
            if len(hang_hoa.ten_hang.strip()) > 150:
                return False, "Tên hàng hóa không được vượt quá 150 ký tự."
            if not hang_hoa.ma_danh_muc or not hang_hoa.ma_danh_muc.strip():
                return False, "Vui lòng chọn danh mục cho hàng hóa."
            if hang_hoa.don_gia < 0:
                return False, "Đơn giá không được nhỏ hơn 0."
            if hang_hoa.so_luong_ton < 0:
                return False, "Số lượng tồn không được nhỏ hơn 0."

        return True, "Dữ liệu hợp lệ."

    # =========================================================================
    # 3. CREATE: THÊM MỚI HÀNG HÓA
    # =========================================================================

    def them_hang_hoa(self, hang_hoa: HangHoa) -> Tuple[bool, str]:
        """
        Thêm một mặt hàng mới vào hệ thống.
        - Kiểm tra định dạng dữ liệu đầu vào.
        - Kiểm tra trùng mã hàng.
        - Gọi Repository để lưu vào CSDL.
        """
        # 1. Kiểm tra validation
        hop_le, thong_bao_loi = self.kiem_tra_du_lieu_hang_hoa(hang_hoa, is_update=False)
        if not hop_le:
            return False, thong_bao_loi

        # 2. Kiểm tra trùng mã hàng
        try:
            if self.repository.check_exists(hang_hoa.ma_hang):
                return False, f"Mã hàng '{hang_hoa.ma_hang}' đã tồn tại trong hệ thống. Vui lòng chọn mã khác."
        except Exception as error:
            logger.warning("Không thể kiểm tra tồn tại mã hàng: %s", error)

        # 3. Ghi vào CSDL
        try:
            thanh_cong = self.repository.insert(hang_hoa)
            if thanh_cong:
                return True, f"Thêm mới hàng hóa '{hang_hoa.ten_hang}' thành công."
            return False, "Thêm hàng hóa không thành công. Vui lòng thử lại."
        except Exception as error:
            logger.error("Lỗi khi thêm hàng hóa: %s", error)
            return False, f"Lỗi khi thêm hàng hóa: {str(error)}"

    # =========================================================================
    # 4. UPDATE: SỬA HÀNG HÓA
    # =========================================================================

    def cap_nhat_hang_hoa(self, hang_hoa: HangHoa) -> Tuple[bool, str]:
        """
        Cập nhật thông tin mặt hàng đã tồn tại.
        - Kiểm tra định dạng dữ liệu đầu vào.
        - Kiểm tra mã hàng có tồn tại không.
        - Gọi Repository để cập nhật vào CSDL.
        """
        # 1. Kiểm tra validation
        hop_le, thong_bao_loi = self.kiem_tra_du_lieu_hang_hoa(hang_hoa, is_update=True)
        if not hop_le:
            return False, thong_bao_loi

        # 2. Kiểm tra mã hàng có tồn tại không
        try:
            if not self.repository.check_exists(hang_hoa.ma_hang):
                return False, f"Không tìm thấy hàng hóa có mã '{hang_hoa.ma_hang}' để cập nhật."
        except Exception as error:
            logger.warning("Không thể kiểm tra tồn tại mã hàng: %s", error)

        # 3. Ghi cập nhật vào CSDL
        try:
            thanh_cong = self.repository.update(hang_hoa)
            if thanh_cong:
                return True, f"Cập nhật hàng hóa '{hang_hoa.ma_hang}' thành công."
            return False, "Cập nhật hàng hóa không thành công."
        except Exception as error:
            logger.error("Lỗi khi cập nhật hàng hóa: %s", error)
            return False, f"Lỗi khi cập nhật hàng hóa: {str(error)}"

    # =========================================================================
    # 5. DELETE: XÓA HÀNG HÓA
    # =========================================================================

    def xoa_hang_hoa(self, ma_hang: str) -> Tuple[bool, str]:
        """
        Xóa một mặt hàng theo mã hàng.
        - Kiểm tra mã hàng không rỗng.
        - Kiểm tra tồn tại trước khi xóa.
        - Gọi Repository để xóa khỏi CSDL.
        """
        if not ma_hang or not ma_hang.strip():
            return False, "Vui lòng chọn hàng hóa cần xóa."

        ma_hang = ma_hang.strip()

        # Kiểm tra tồn tại
        try:
            if not self.repository.check_exists(ma_hang):
                return False, f"Không tìm thấy hàng hóa có mã '{ma_hang}' để xóa."
        except Exception as error:
            logger.warning("Không thể kiểm tra tồn tại mã hàng: %s", error)

        # Thực thi xóa
        try:
            thanh_cong = self.repository.delete(ma_hang)
            if thanh_cong:
                return True, f"Đã xóa hàng hóa '{ma_hang}' thành công."
            return False, f"Không thể xóa hàng hóa '{ma_hang}'."
        except Exception as error:
            logger.error("Lỗi khi xóa hàng hóa: %s", error)
            return False, f"Lỗi khi xóa hàng hóa: {str(error)}"
