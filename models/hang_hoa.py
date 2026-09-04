from typing import Any, Dict, Optional, Tuple, Union


class HangHoa:
    def __init__(
        self,
        ma_hang: str = "",
        ten_hang: str = "",
        ma_danh_muc: str = "",
        don_gia: Union[float, int] = 0.0,
        so_luong_ton: int = 0,
        trang_thai: str = "Còn hàng",
        mo_ta: str = "",
        ten_danh_muc: str = ""
    ) -> None:
        self.ma_hang = str(ma_hang).strip() if ma_hang is not None else ""
        self.ten_hang = str(ten_hang).strip() if ten_hang is not None else ""
        self.ma_danh_muc = str(ma_danh_muc).strip() if ma_danh_muc is not None else ""
        self.don_gia = float(don_gia) if don_gia is not None else 0.0
        self.so_luong_ton = int(so_luong_ton) if so_luong_ton is not None else 0
        self.trang_thai = str(trang_thai).strip() if trang_thai is not None else "Còn hàng"
        self.mo_ta = str(mo_ta).strip() if mo_ta is not None else ""
        self.ten_danh_muc = str(ten_danh_muc).strip() if ten_danh_muc is not None else ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ma_hang": self.ma_hang,
            "ten_hang": self.ten_hang,
            "ma_danh_muc": self.ma_danh_muc,
            "ten_danh_muc": self.ten_danh_muc,
            "don_gia": self.don_gia,
            "so_luong_ton": self.so_luong_ton,
            "trang_thai": self.trang_thai,
            "mo_ta": self.mo_ta,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HangHoa":
        if not data:
            return cls()
        return cls(
            ma_hang=data.get("ma_hang", ""),
            ten_hang=data.get("ten_hang", ""),
            ma_danh_muc=data.get("ma_danh_muc", ""),
            don_gia=data.get("don_gia", 0.0),
            so_luong_ton=data.get("so_luong_ton", 0),
            trang_thai=data.get("trang_thai", "Còn hàng"),
            mo_ta=data.get("mo_ta", ""),
            ten_danh_muc=data.get("ten_danh_muc", ""),
        )

    @classmethod
    def from_row(cls, row: Any, columns: Optional[list] = None) -> "HangHoa":
        if row is None:
            return cls()
        try:
            if hasattr(row, "ma_hang"):
                return cls(
                    ma_hang=getattr(row, "ma_hang", ""),
                    ten_hang=getattr(row, "ten_hang", ""),
                    ma_danh_muc=getattr(row, "ma_danh_muc", ""),
                    don_gia=getattr(row, "don_gia", 0.0),
                    so_luong_ton=getattr(row, "so_luong_ton", 0),
                    trang_thai=getattr(row, "trang_thai", "Còn hàng"),
                    mo_ta=getattr(row, "mo_ta", "") or "",
                    ten_danh_muc=getattr(row, "ten_danh_muc", "") or "",
                )
        except Exception:
            pass

        if columns and isinstance(row, (tuple, list)):
            col_map = {name.lower(): idx for idx, name in enumerate(columns)}
            return cls(
                ma_hang=row[col_map["ma_hang"]] if "ma_hang" in col_map else "",
                ten_hang=row[col_map["ten_hang"]] if "ten_hang" in col_map else "",
                ma_danh_muc=row[col_map["ma_danh_muc"]] if "ma_danh_muc" in col_map else "",
                don_gia=row[col_map["don_gia"]] if "don_gia" in col_map else 0.0,
                so_luong_ton=row[col_map["so_luong_ton"]] if "so_luong_ton" in col_map else 0,
                trang_thai=row[col_map["trang_thai"]] if "trang_thai" in col_map else "Còn hàng",
                mo_ta=row[col_map["mo_ta"]] if "mo_ta" in col_map and row[col_map["mo_ta"]] is not None else "",
                ten_danh_muc=row[col_map["ten_danh_muc"]] if "ten_danh_muc" in col_map and row[col_map["ten_danh_muc"]] is not None else "",
            )

        # Trường hợp thứ tự mặc định của bảng HangHoa trong CSDL:
        # (ma_hang, ten_hang, ma_danh_muc, don_gia, so_luong_ton, trang_thai, mo_ta, [ten_danh_muc])
        if isinstance(row, (tuple, list)):
            return cls(
                ma_hang=row[0] if len(row) > 0 else "",
                ten_hang=row[1] if len(row) > 1 else "",
                ma_danh_muc=row[2] if len(row) > 2 else "",
                don_gia=row[3] if len(row) > 3 else 0.0,
                so_luong_ton=row[4] if len(row) > 4 else 0,
                trang_thai=row[5] if len(row) > 5 else "Còn hàng",
                mo_ta=row[6] if len(row) > 6 and row[6] is not None else "",
                ten_danh_muc=row[7] if len(row) > 7 and row[7] is not None else "",
            )

        return cls()

    def to_treeview_tuple(self) -> Tuple[str, str, str, str, int, str, str]:
        display_danh_muc = self.ten_danh_muc if self.ten_danh_muc else self.ma_danh_muc
        formatted_don_gia = f"{self.don_gia:,.0f}" if self.don_gia is not None else "0"
        return (
            self.ma_hang,
            self.ten_hang,
            display_danh_muc,
            formatted_don_gia,
            self.so_luong_ton,
            self.trang_thai,
            self.mo_ta,
        )

    def __repr__(self) -> str:
        return (
            f"HangHoa(ma_hang='{self.ma_hang}', ten_hang='{self.ten_hang}', "
            f"ma_danh_muc='{self.ma_danh_muc}', don_gia={self.don_gia}, "
            f"so_luong_ton={self.so_luong_ton}, trang_thai='{self.trang_thai}')"
        )
