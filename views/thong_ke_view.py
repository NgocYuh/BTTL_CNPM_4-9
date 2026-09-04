"""
Module: views.thong_ke_view
Thành viên phụ trách: Thành viên 5 — Module Thống kê tổng số lượng
Giao diện thống kê hàng hóa, tổng số lượng tồn kho và phân loại theo danh mục.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Dict, Any

from repositories.hang_hoa_repository import HangHoaRepository


def _format_currency(value: Any) -> str:
    """Định dạng tiền tệ chuẩn tiếng Việt (ví dụ: 125,000,000 đ)."""
    if value is None:
        return "0 đ"
    try:
        num = float(value)
        return f"{int(round(num)):,} đ"
    except (ValueError, TypeError):
        return "0 đ"


def _format_quantity(value: Any) -> str:
    """Định dạng số lượng với dấu phân cách (ví dụ: 1,250)."""
    if value is None:
        return "0"
    try:
        num = float(value)
        return f"{int(round(num)):,}"
    except (ValueError, TypeError):
        return "0"


class ThongKeView(ttk.Frame):
    """
    Giao diện Thống kê tổng số lượng hàng hóa và giá trị tồn kho.
    Kế thừa ttk.Frame để Thành viên 1 dễ dàng tích hợp vào MainWindow.
    """

    def __init__(self, parent, repository: Optional[HangHoaRepository] = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.repository = repository or HangHoaRepository()

        # Biến StringVar hiển thị trên 3 thẻ tổng quan
        self.var_total_types = tk.StringVar(value="0")
        self.var_total_quantity = tk.StringVar(value="0")
        self.var_total_value = tk.StringVar(value="0 đ")

        self._configure_styles()
        self._build_ui()

        # Tự động tải dữ liệu khi mở màn hình
        self.load_statistics()

    def _configure_styles(self):
        """Cấu hình các style ttk cho giao diện."""
        style = ttk.Style(self)

        # Style tiêu đề
        style.configure(
            "ThongKeHeader.TLabel",
            font=("Segoe UI", 16, "bold"),
            foreground="#1E293B",
        )

        style.configure(
            "ThongKeSection.TLabel",
            font=("Segoe UI", 11, "bold"),
            foreground="#334155",
        )

        style.configure(
            "ThongKe.Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            foreground="#1E293B",
        )

        style.configure(
            "ThongKe.Treeview",
            font=("Segoe UI", 10),
            rowheight=26,
        )

    def _build_ui(self):
        """Xây dựng bố cục giao diện."""
        self.pack(fill="both", expand=True, padx=20, pady=15)

        # 1. TIÊU ĐỀ CHÍNH
        title_label = ttk.Label(
            self,
            text="THỐNG KÊ HÀNG HÓA",
            style="ThongKeHeader.TLabel",
            anchor="center",
        )
        title_label.pack(fill="x", pady=(0, 15))

        # 2. KHU VỰC 3 THẺ TỔNG QUAN
        cards_frame = ttk.Frame(self)
        cards_frame.pack(fill="x", pady=(0, 15))
        cards_frame.columnconfigure((0, 1, 2), weight=1, uniform="cards")

        # Thẻ 1: Tổng số loại
        card1 = tk.LabelFrame(
            cards_frame,
            text=" Tổng số loại ",
            font=("Segoe UI", 10, "bold"),
            fg="#1E40AF",
            bg="#EFF6FF",
            relief="groove",
            bd=2,
            padx=12,
            pady=10,
        )
        card1.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        lbl_val1 = tk.Label(
            card1,
            textvariable=self.var_total_types,
            font=("Segoe UI", 20, "bold"),
            fg="#1D4ED8",
            bg="#EFF6FF",
        )
        lbl_val1.pack(expand=True, pady=4)

        # Thẻ 2: Tổng số lượng
        card2 = tk.LabelFrame(
            cards_frame,
            text=" Tổng số lượng ",
            font=("Segoe UI", 10, "bold"),
            fg="#065F46",
            bg="#ECFDF5",
            relief="groove",
            bd=2,
            padx=12,
            pady=10,
        )
        card2.grid(row=0, column=1, sticky="nsew", padx=4)

        lbl_val2 = tk.Label(
            card2,
            textvariable=self.var_total_quantity,
            font=("Segoe UI", 20, "bold"),
            fg="#047857",
            bg="#ECFDF5",
        )
        lbl_val2.pack(expand=True, pady=4)

        # Thẻ 3: Tổng giá trị tồn kho
        card3 = tk.LabelFrame(
            cards_frame,
            text=" Tổng giá trị tồn kho ",
            font=("Segoe UI", 10, "bold"),
            fg="#92400E",
            bg="#FFFBEB",
            relief="groove",
            bd=2,
            padx=12,
            pady=10,
        )
        card3.grid(row=0, column=2, sticky="nsew", padx=(8, 0))

        lbl_val3 = tk.Label(
            card3,
            textvariable=self.var_total_value,
            font=("Segoe UI", 18, "bold"),
            fg="#B45309",
            bg="#FFFBEB",
        )
        lbl_val3.pack(expand=True, pady=4)

        # 3. NÚT LÀM MỚI
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(0, 15))

        btn_refresh = ttk.Button(
            btn_frame,
            text="🔄 Làm mới",
            command=self.load_statistics,
            cursor="hand2",
        )
        btn_refresh.pack(anchor="center", ipadx=10, ipady=3)

        # 4. KHU VỰC THỐNG KÊ THEO DANH MỤC
        lbl_section = ttk.Label(
            self,
            text="THỐNG KÊ THEO DANH MỤC",
            style="ThongKeSection.TLabel",
        )
        lbl_section.pack(anchor="w", pady=(5, 8))

        # Bảng dữ liệu Treeview
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        columns = ("TenDanhMuc", "SoLoaiHang", "TongSoLuong", "TongGiaTri")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="ThongKe.Treeview",
            selectmode="browse",
        )

        self.tree.heading("TenDanhMuc", text="Danh mục", anchor="w")
        self.tree.heading("SoLoaiHang", text="Số loại hàng", anchor="e")
        self.tree.heading("TongSoLuong", text="Tổng số lượng", anchor="e")
        self.tree.heading("TongGiaTri", text="Tổng giá trị", anchor="e")

        self.tree.column("TenDanhMuc", width=220, minwidth=150, anchor="w")
        self.tree.column("SoLoaiHang", width=120, minwidth=100, anchor="e")
        self.tree.column("TongSoLuong", width=140, minwidth=110, anchor="e")
        self.tree.column("TongGiaTri", width=200, minwidth=150, anchor="e")

        # Scrollbar
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Tag màu xen kẽ
        self.tree.tag_configure("oddrow", background="#F8FAFC")
        self.tree.tag_configure("evenrow", background="#FFFFFF")

    def load_statistics(self):
        """
        Nạp dữ liệu thống kê từ CSDL và cập nhật giao diện:
        - 3 Thẻ tổng quan
        - Bảng thống kê theo danh mục
        """
        try:
            total_types = self.repository.get_total_product_types()
            total_quantity = self.repository.get_total_quantity()
            total_value = self.repository.get_total_inventory_value()
            category_stats: List[Dict[str, Any]] = self.repository.get_statistics_by_category()

            # 1. Cập nhật 3 thẻ
            self.var_total_types.set(_format_quantity(total_types))
            self.var_total_quantity.set(_format_quantity(total_quantity))
            self.var_total_value.set(_format_currency(total_value))

            # 2. Cập nhật bảng
            for item in self.tree.get_children():
                self.tree.delete(item)

            for idx, stat in enumerate(category_stats):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        stat.get("TenDanhMuc", ""),
                        _format_quantity(stat.get("SoLoaiHang", 0)),
                        _format_quantity(stat.get("TongSoLuong", 0)),
                        _format_currency(stat.get("TongGiaTri", 0)),
                    ),
                    tags=(tag,),
                )

        except Exception as e:
            messagebox.showerror(
                "Lỗi Thống Kê",
                f"Không thể tải dữ liệu thống kê:\n{e}"
            )
