def validate_ma_hang(ma_hang):
    """
    Kiểm tra mã hàng.
    """
    if ma_hang is None or not ma_hang.strip():
        return False, "Mã hàng không được để trống."

    ma_hang = ma_hang.strip()

    if len(ma_hang) > 20:
        return False, "Mã hàng không được vượt quá 20 ký tự."

    return True, ""


def validate_ten_hang(ten_hang):
    """
    Kiểm tra tên hàng.
    """
    if ten_hang is None or not ten_hang.strip():
        return False, "Tên hàng không được để trống."

    ten_hang = ten_hang.strip()

    if len(ten_hang) > 100:
        return False, "Tên hàng không được vượt quá 100 ký tự."

    return True, ""


def validate_danh_muc(ma_danh_muc):
    """
    Kiểm tra danh mục.
    """
    if ma_danh_muc is None or not str(ma_danh_muc).strip():
        return False, "Danh mục không được để trống."

    return True, ""


def validate_don_gia(don_gia):
    """
    Kiểm tra đơn giá.
    """
    if don_gia is None or str(don_gia).strip() == "":
        return False, "Đơn giá không được để trống."

    try:
        gia = float(don_gia)
    except (ValueError, TypeError):
        return False, "Đơn giá phải là số."

    if gia < 0:
        return False, "Đơn giá không được nhỏ hơn 0."

    return True, ""


def validate_so_luong(so_luong):
    """
    Kiểm tra số lượng.
    """
    if so_luong is None or str(so_luong).strip() == "":
        return False, "Số lượng không được để trống."

    try:
        so_luong_int = int(so_luong)
    except (ValueError, TypeError):
        return False, "Số lượng phải là số nguyên."

    if so_luong_int < 0:
        return False, "Số lượng không được nhỏ hơn 0."

    return True, ""


def validate_khoang_gia(gia_min, gia_max):
    """
    Kiểm tra khoảng giá khi lọc.
    """
    min_value = None
    max_value = None

    if gia_min is not None and str(gia_min).strip() != "":
        try:
            min_value = float(gia_min)
        except (ValueError, TypeError):
            return False, "Giá tối thiểu phải là số."

        if min_value < 0:
            return False, "Giá tối thiểu không được nhỏ hơn 0."

    if gia_max is not None and str(gia_max).strip() != "":
        try:
            max_value = float(gia_max)
        except (ValueError, TypeError):
            return False, "Giá tối đa phải là số."

        if max_value < 0:
            return False, "Giá tối đa không được nhỏ hơn 0."

    if min_value is not None and max_value is not None:
        if min_value > max_value:
            return False, "Giá tối thiểu không được lớn hơn giá tối đa."

    return True, ""


def validate_hang_hoa(ma_hang, ten_hang, ma_danh_muc, don_gia, so_luong):
    """
    Kiểm tra toàn bộ dữ liệu hàng hóa.
    Trả về:
        (True, "")
    hoặc:
        (False, "Nội dung lỗi")
    """

    validators = [
        validate_ma_hang(ma_hang),
        validate_ten_hang(ten_hang),
        validate_danh_muc(ma_danh_muc),
        validate_don_gia(don_gia),
        validate_so_luong(so_luong)
    ]

    for is_valid, message in validators:
        if not is_valid:
            return False, message

    return True, ""