"""
View: HangHoaView (Giao diện Quản lý Danh mục Hàng hóa)
Phụ trách: Thành viên 3 (TV3) - CRUD Hàng hóa
Phối hợp:
    - Thành viên 1 (TV1): Tích hợp vào MainWindow (content_frame)
    - Thành viên 4 (TV4): Tích hợp Tìm kiếm & Lọc nâng cao
Dự án: QuanLyHangHoa (Cửa hàng kinh doanh Gear Công Nghệ)
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Optional

from models.hang_hoa import HangHoa
from services.hang_hoa_service import HangHoaService


class HangHoaView(ttk.Frame):
    """
    Giao diện Quản lý Hàng hóa kế thừa từ ttk.Frame:
        - Khu vực Form nhập thông tin hàng hóa.
        - Cụm nút chức năng CRUD: Thêm, Sửa, Xóa, Làm mới.
        - Khung Tìm kiếm & Lọc (hỗ trợ mở rộng cho TV4).
        - Bảng hiển thị danh sách hàng hóa (ttk.Treeview) kèm thanh cuộn.
        - Cơ chế bắt sự kiện click chọn dòng tự động điền dữ liệu lên form.
    """

    def __init__(self, parent: tk.Widget, service: Optional[HangHoaService] = None) -> None:
        super().__init__(parent)
        self.service = service if service is not None else HangHoaService()

        # Biến quản lý dữ liệu Form
        self.var_ma_hang = tk.StringVar()
        self.var_ten_hang = tk.StringVar()
        self.var_danh_muc = tk.StringVar()
        self.var_don_gia = tk.StringVar()
        self.var_so_luong = tk.StringVar(value="0")
        self.var_trang_thai = tk.StringVar(value="Còn hàng")
        self.var_mo_ta = tk.StringVar()

        # Biến tìm kiếm nhanh
        self.var_search = tk.StringVar()
        self.var_filter_danh_muc = tk.StringVar(value="Tất cả danh mục")

        # Ánh xạ danh mục: {"Tên hiển thị": "Mã danh mục"}
        self.category_map = {}
        self.category_reverse_map = {}

        # Cấu hình grid co giãn
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Xây dựng các thành phần giao diện
        self._init_styles()
        self._create_header()
        self._create_form()
        self._create_search_filter_bar()
        self._create_table()

        # Nạp dữ liệu ban đầu
        self._load_categories()
        self.load_data()

    # =========================================================================
    # 1. KHỞI TẠO STYLE VÀ GIAO DIỆN
    # =========================================================================

    def _init_styles(self) -> None:
        """Định nghĩa style đồng bộ với MainWindow."""
        style = ttk.Style(self)
        style.configure("ViewHeader.TLabel", font=("Segoe UI", 16, "bold"), foreground="#0f172a")
        style.configure("ViewSubHeader.TLabel", font=("Segoe UI", 9), foreground="#64748b")
        style.configure("FormLabel.TLabel", font=("Segoe UI", 9, "bold"), foreground="#334155")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=26)

    def _create_header(self) -> None:
        """Tạo thanh tiêu đề module."""
        header_frame = ttk.Frame(self, padding=(12, 10, 12, 4))
        header_frame.grid(row=0, column=0, sticky="ew")

        ttk.Label(
            header_frame,
            text="QUẢN LÝ DANH MỤC HÀNG HÓA",
            style="ViewHeader.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text="Thêm mới, cập nhật, xóa và theo dõi danh sách gear công nghệ",
            style="ViewSubHeader.TLabel",
        ).pack(anchor="w", pady=(2, 0))

    def _create_form(self) -> None:
        """Tạo khung nhập liệu và các nút chức năng CRUD."""
        form_frame = ttk.LabelFrame(self, text=" Thông tin hàng hóa ", padding=12)
        form_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=6)

        for col in range(6):
            form_frame.grid_columnconfigure(col, weight=1)

        # Dòng 0: Mã hàng & Tên hàng
        ttk.Label(form_frame, text="Mã hàng (*):", style="FormLabel.TLabel").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.entry_ma_hang = ttk.Entry(form_frame, textvariable=self.var_ma_hang)
        self.entry_ma_hang.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form_frame, text="Tên hàng (*):", style="FormLabel.TLabel").grid(row=0, column=2, sticky="w", padx=4, pady=4)
        self.entry_ten_hang = ttk.Entry(form_frame, textvariable=self.var_ten_hang)
        self.entry_ten_hang.grid(row=0, column=3, columnspan=3, sticky="ew", padx=4, pady=4)

        # Dòng 1: Danh mục, Đơn giá, Số lượng
        ttk.Label(form_frame, text="Danh mục (*):", style="FormLabel.TLabel").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.cbo_danh_muc = ttk.Combobox(form_frame, textvariable=self.var_danh_muc, state="readonly")
        self.cbo_danh_muc.grid(row=1, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form_frame, text="Đơn giá (VNĐ):", style="FormLabel.TLabel").grid(row=1, column=2, sticky="w", padx=4, pady=4)
        self.entry_don_gia = ttk.Entry(form_frame, textvariable=self.var_don_gia)
        self.entry_don_gia.grid(row=1, column=3, sticky="ew", padx=4, pady=4)

        ttk.Label(form_frame, text="Số lượng tồn:", style="FormLabel.TLabel").grid(row=1, column=4, sticky="w", padx=4, pady=4)
        self.entry_so_luong = ttk.Spinbox(form_frame, from_=0, to=999999, textvariable=self.var_so_luong)
        self.entry_so_luong.grid(row=1, column=5, sticky="ew", padx=4, pady=4)

        # Dòng 2: Trạng thái & Mô tả
        ttk.Label(form_frame, text="Trạng thái:", style="FormLabel.TLabel").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.cbo_trang_thai = ttk.Combobox(
            form_frame,
            textvariable=self.var_trang_thai,
            values=["Còn hàng", "Ngừng kinh doanh"],
            state="readonly",
        )
        self.cbo_trang_thai.grid(row=2, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form_frame, text="Mô tả:", style="FormLabel.TLabel").grid(row=2, column=2, sticky="w", padx=4, pady=4)
        self.entry_mo_ta = ttk.Entry(form_frame, textvariable=self.var_mo_ta)
        self.entry_mo_ta.grid(row=2, column=3, columnspan=3, sticky="ew", padx=4, pady=4)

        # Dòng 3: Cụm nút bấm CRUD (Action Buttons)
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=6, sticky="e", pady=(10, 2))

        self.btn_them = tk.Button(
            btn_frame,
            text="✚ Thêm",
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=4,
            relief="flat",
            cursor="hand2",
            command=self.on_them,
        )
        self.btn_them.pack(side="left", padx=4)

        self.btn_sua = tk.Button(
            btn_frame,
            text="✎ Sửa",
            bg="#0d9488",
            fg="#ffffff",
            activebackground="#0f766e",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=4,
            relief="flat",
            cursor="hand2",
            command=self.on_sua,
        )
        self.btn_sua.pack(side="left", padx=4)

        self.btn_xoa = tk.Button(
            btn_frame,
            text="✕ Xóa",
            bg="#e11d48",
            fg="#ffffff",
            activebackground="#be123c",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=4,
            relief="flat",
            cursor="hand2",
            command=self.on_xoa,
        )
        self.btn_xoa.pack(side="left", padx=4)

        self.btn_lam_moi = tk.Button(
            btn_frame,
            text="↻ Làm mới",
            bg="#64748b",
            fg="#ffffff",
            activebackground="#475569",
            activeforeground="#ffffff",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=4,
            relief="flat",
            cursor="hand2",
            command=self.on_lam_moi,
        )
        self.btn_lam_moi.pack(side="left", padx=4)

    def _create_search_filter_bar(self) -> None:
        """Khu vực thanh Tìm kiếm & Bộ lọc (Phối hợp với TV4)."""
        self.frame_search_filter = ttk.Frame(self, padding=(12, 4, 12, 4))
        self.frame_search_filter.grid(row=2, column=0, sticky="ew")

        ttk.Label(self.frame_search_filter, text="Tìm kiếm:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 4))
        entry_search = ttk.Entry(self.frame_search_filter, textvariable=self.var_search, width=28)
        entry_search.pack(side="left", padx=(0, 6))
        entry_search.bind("<Return>", lambda _event: self.on_tim_kiem())

        btn_search = ttk.Button(self.frame_search_filter, text="Tìm", command=self.on_tim_kiem)
        btn_search.pack(side="left", padx=(0, 14))

        ttk.Label(self.frame_search_filter, text="Lọc theo danh mục:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 4))
        self.cbo_filter_dm = ttk.Combobox(self.frame_search_filter, textvariable=self.var_filter_danh_muc, state="readonly", width=22)
        self.cbo_filter_dm.pack(side="left", padx=(0, 6))
        self.cbo_filter_dm.bind("<<ComboboxSelected>>", lambda _event: self.on_filter_danh_muc())

        btn_reset_filter = ttk.Button(self.frame_search_filter, text="Đặt lại", command=self.on_reset_filter)
        btn_reset_filter.pack(side="left")

        # Label đếm số lượng bản ghi
        self.lbl_count = ttk.Label(self.frame_search_filter, text="Tổng số: 0", font=("Segoe UI", 9, "italic"), foreground="#475569")
        self.lbl_count.pack(side="right")

    def _create_table(self) -> None:
        """Tạo bảng dữ liệu ttk.Treeview hiển thị danh sách hàng hóa."""
        table_container = ttk.Frame(self, padding=(12, 4, 12, 12))
        table_container.grid(row=3, column=0, sticky="nsew")
        self.grid_rowconfigure(3, weight=1)

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        columns = ("ma_hang", "ten_hang", "danh_muc", "don_gia", "so_luong", "trang_thai", "mo_ta")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")

        # Định nghĩa tiêu đề cột
        self.tree.heading("ma_hang", text="Mã hàng")
        self.tree.heading("ten_hang", text="Tên hàng hóa")
        self.tree.heading("danh_muc", text="Danh mục")
        self.tree.heading("don_gia", text="Đơn giá (VNĐ)")
        self.tree.heading("so_luong", text="Số lượng tồn")
        self.tree.heading("trang_thai", text="Trạng thái")
        self.tree.heading("mo_ta", text="Mô tả")

        # Định nghĩa độ rộng cột
        self.tree.column("ma_hang", width=90, minwidth=70, anchor="center")
        self.tree.column("ten_hang", width=220, minwidth=140, anchor="w")
        self.tree.column("danh_muc", width=130, minwidth=100, anchor="w")
        self.tree.column("don_gia", width=110, minwidth=90, anchor="e")
        self.tree.column("so_luong", width=95, minwidth=80, anchor="center")
        self.tree.column("trang_thai", width=120, minwidth=100, anchor="center")
        self.tree.column("mo_ta", width=200, minwidth=120, anchor="w")

        # Thanh cuộn dọc & ngang
        v_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Bắt sự kiện chọn dòng để điền form
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    # =========================================================================
    # 2. XỬ LÝ DỮ LIỆU & BINDING
    # =========================================================================

    def _load_categories(self) -> None:
        """Nạp danh sách danh mục từ Database/Service vào Combobox."""
        categories = self.service.lay_danh_sach_danh_muc()
        self.category_map.clear()
        self.category_reverse_map.clear()

        names = []
        for cat in categories:
            ma = cat.get("ma_danh_muc", "")
            ten = cat.get("ten_danh_muc", "")
            if ma and ten:
                self.category_map[ten] = ma
                self.category_reverse_map[ma] = ten
                names.append(ten)

        self.cbo_danh_muc["values"] = names
        if names:
            self.cbo_danh_muc.current(0)

        # Cập nhật combobox lọc
        filter_options = ["Tất cả danh mục"] + names
        self.cbo_filter_dm["values"] = filter_options
        self.cbo_filter_dm.current(0)

    def load_data(self) -> None:
        """Tải lại toàn bộ dữ liệu hàng hóa từ CSDL lên bảng Treeview."""
        ok, msg, data = self.service.lay_danh_sach_hang_hoa()
        if not ok:
            messagebox.showwarning("Cảnh báo", msg)
        self.display_data(data)

    def display_data(self, items: List[HangHoa]) -> None:
        """
        Hiển thị danh sách hàng hóa lên Treeview.
        Phương thức công khai để TV4 có thể truyền danh sách sau khi tìm kiếm/lọc.
        """
        self.tree.delete(*self.tree.get_children())
        for item in items:
            self.tree.insert("", "end", values=item.to_treeview_tuple())
        self.lbl_count.config(text=f"Tổng số: {len(items)}")

    def on_tree_select(self, _event) -> None:
        """
        Khi người dùng click chọn 1 dòng trên bảng Treeview:
        Tự động trích xuất thông tin dòng đó và điền ngược lên form nhập liệu.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item[0], "values")
        if not values:
            return

        # Cột: (ma_hang, ten_hang, danh_muc, don_gia, so_luong, trang_thai, mo_ta)
        self.var_ma_hang.set(values[0])
        self.var_ten_hang.set(values[1])

        # Danh mục
        danh_muc_name = values[2]
        if danh_muc_name in self.category_map:
            self.var_danh_muc.set(danh_muc_name)

        # Đơn giá: bỏ dấu phẩy ngăn cách hàng nghìn
        don_gia_raw = str(values[3]).replace(",", "").replace(".", "").replace(" ", "").replace("đ", "")
        self.var_don_gia.set(don_gia_raw)

        # Số lượng
        self.var_so_luong.set(values[4])

        # Trạng thái
        self.var_trang_thai.set(values[5])

        # Mô tả
        self.var_mo_ta.set(values[6] if len(values) > 6 else "")

        # Khóa ô nhập mã hàng khi đang chọn sửa dòng để tránh sửa nhầm khóa chính
        self.entry_ma_hang.config(state="disabled")

    def _get_form_hang_hoa(self) -> Optional[HangHoa]:
        """Đọc và đóng gói dữ liệu từ form thành đối tượng HangHoa."""
        ma_hang = self.var_ma_hang.get().strip()
        ten_hang = self.var_ten_hang.get().strip()
        ten_dm = self.var_danh_muc.get().strip()
        ma_dm = self.category_map.get(ten_dm, "")
        mo_ta = self.var_mo_ta.get().strip()
        trang_thai_text = self.var_trang_thai.get().strip()

        # Đọc đơn giá
        don_gia_str = self.var_don_gia.get().strip().replace(",", "").replace(".", "").replace(" ", "")
        try:
            don_gia = float(don_gia_str) if don_gia_str else 0.0
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Đơn giá phải là số hợp lệ.")
            return None

        # Đọc số lượng
        so_luong_str = self.var_so_luong.get().strip()
        try:
            so_luong = int(so_luong_str) if so_luong_str else 0
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Số lượng phải là số nguyên hợp lệ.")
            return None

        return HangHoa(
            ma_hang=ma_hang,
            ten_hang=ten_hang,
            ma_danh_muc=ma_dm,
            ten_danh_muc=ten_dm,
            don_gia=don_gia,
            so_luong_ton=so_luong,
            trang_thai=trang_thai_text,
            mo_ta=mo_ta,
        )

    # =========================================================================
    # 3. CÁC HÀM XỬ LÝ SỰ KIỆN CLICK (EVENT HANDLERS - CRUD)
    # =========================================================================

    def on_them(self) -> None:
        """Xử lý sự kiện khi bấm nút Thêm."""
        # Nếu ô mã hàng đang bị disable (do đang chọn dòng), mở lại trước khi kiểm tra
        self.entry_ma_hang.config(state="normal")

        hang_hoa = self._get_form_hang_hoa()
        if hang_hoa is None:
            return

        ok, msg = self.service.them_hang_hoa(hang_hoa)
        if ok:
            messagebox.showinfo("Thành công", msg)
            self.on_lam_moi()
        else:
            messagebox.showerror("Lỗi thêm hàng hóa", msg)

    def on_sua(self) -> None:
        """Xử lý sự kiện khi bấm nút Sửa."""
        # Đảm bảo đọc được mã hàng kể cả khi entry đang disabled
        self.entry_ma_hang.config(state="normal")

        hang_hoa = self._get_form_hang_hoa()
        if hang_hoa is None:
            return

        if not hang_hoa.ma_hang:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mặt hàng trong danh sách để sửa.")
            return

        ok, msg = self.service.cap_nhat_hang_hoa(hang_hoa)
        if ok:
            messagebox.showinfo("Thành công", msg)
            self.on_lam_moi()
        else:
            messagebox.showerror("Lỗi cập nhật", msg)

    def on_xoa(self) -> None:
        """Xử lý sự kiện khi bấm nút Xóa."""
        ma_hang = self.var_ma_hang.get().strip()
        if not ma_hang:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mặt hàng cần xóa từ danh sách.")
            return

        xac_nhan = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa hàng hóa có mã '{ma_hang}' không?",
        )
        if not xac_nhan:
            return

        ok, msg = self.service.xoa_hang_hoa(ma_hang)
        if ok:
            messagebox.showinfo("Thành công", msg)
            self.on_lam_moi()
        else:
            messagebox.showerror("Lỗi xóa hàng hóa", msg)

    def on_lam_moi(self) -> None:
        """Xử lý sự kiện khi bấm nút Làm mới: Xóa trắng Form và tải lại bảng."""
        self.entry_ma_hang.config(state="normal")
        self.var_ma_hang.set("")
        self.var_ten_hang.set("")
        if self.cbo_danh_muc["values"]:
            self.cbo_danh_muc.current(0)
        self.var_don_gia.set("")
        self.var_so_luong.set("0")
        self.var_trang_thai.set("Còn hàng")
        self.var_mo_ta.set("")

        # Hủy chọn trên Treeview
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        # Tải lại bảng
        self.load_data()

    # =========================================================================
    # 4. TÌM KIẾM & BỘ LỌC (HỖ TRỢ TV4)
    # =========================================================================

    def on_tim_kiem(self) -> None:
        """Tìm kiếm cục bộ theo từ khóa (Mã hàng hoặc Tên hàng)."""
        keyword = self.var_search.get().strip().lower()
        ok, _msg, all_items = self.service.lay_danh_sach_hang_hoa()
        if not ok:
            return

        if not keyword:
            self.display_data(all_items)
            return

        filtered = [
            item for item in all_items
            if keyword in item.ma_hang.lower()
            or keyword in item.ten_hang.lower()
            or keyword in item.ten_danh_muc.lower()
        ]
        self.display_data(filtered)

    def on_filter_danh_muc(self) -> None:
        """Lọc danh sách theo danh mục được chọn từ combobox."""
        selected_cat = self.var_filter_danh_muc.get().strip()
        ok, _msg, all_items = self.service.lay_danh_sach_hang_hoa()
        if not ok:
            return

        if selected_cat == "Tất cả danh mục" or not selected_cat:
            self.display_data(all_items)
            return

        filtered = [item for item in all_items if item.ten_danh_muc == selected_cat]
        self.display_data(filtered)

    def on_reset_filter(self) -> None:
        """Đặt lại bộ lọc về mặc định."""
        self.var_search.set("")
        self.var_filter_danh_muc.set("Tất cả danh mục")
        self.load_data()


# Khối hỗ trợ chạy thử nghiệm giao diện độc lập
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kiểm tra độc lập HangHoaView (TV3)")
    root.geometry("980, 640")

    view = HangHoaView(root)
    view.pack(fill="both", expand=True)

    root.mainloop()
