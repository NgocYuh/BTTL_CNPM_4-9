"""Cửa sổ gốc, header và điều hướng của ứng dụng QuanLyHangHoa."""

import tkinter as tk
from tkinter import ttk

from utils.helpers import show_info_message
from views.home_view import HomeView


class MainWindow(tk.Tk):
    """Chỉ tạo một Tk root và mount các view vào vùng nội dung chung."""

    def __init__(self):
        super().__init__()
        self.title("HCMUTE_ChanBoMayDe - Quản lý gear công nghệ")
        self.geometry("1280x760")
        self.minsize(1080, 680)
        self.configure(bg="#f7f9fc")

        self.nav_buttons = {}
        self.current_view = None
        self.pending_search_keyword = ""
        self.pending_category = None
        self._configure_style()
        self._create_menu()
        self._create_shell()
        self.show_home()

    def _configure_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Shell.TFrame", background="#ffffff")
        style.configure(
            "Brand.TLabel", background="#ffffff", foreground="#0f172a", font=("Segoe UI", 17, "bold")
        )
        style.configure(
            "Nav.TButton", background="#ffffff", foreground="#475569", borderwidth=0,
            padding=(12, 9), font=("Segoe UI", 9, "bold")
        )
        style.map("Nav.TButton", background=[("active", "#f0f9ff")], foreground=[("active", "#0284c7")])
        style.configure(
            "ActiveNav.TButton", background="#e0f2fe", foreground="#0369a1", borderwidth=0,
            padding=(12, 9), font=("Segoe UI", 9, "bold")
        )
        style.map("ActiveNav.TButton", background=[("active", "#bae6fd")])
        style.configure(
            "HeaderAction.TButton", background="#ffffff", foreground="#475569", borderwidth=0,
            padding=(8, 7), font=("Segoe UI", 9, "bold")
        )
        style.map(
            "HeaderAction.TButton", background=[("active", "#f1f5f9")], foreground=[("active", "#0284c7")]
        )

    def _create_menu(self):
        menu_bar = tk.Menu(self)
        danh_muc_menu = tk.Menu(menu_bar, tearoff=0)
        danh_muc_menu.add_command(label="Trang chủ", command=self.show_home)
        danh_muc_menu.add_command(label="Danh mục hàng hóa", command=self.show_hang_hoa_view)
        danh_muc_menu.add_command(label="Thống kê tổng số lượng", command=self.show_thong_ke_view)
        danh_muc_menu.add_separator()
        danh_muc_menu.add_command(label="Thoát", command=self.destroy)
        menu_bar.add_cascade(label="DANH MỤC", menu=danh_muc_menu)
        self.config(menu=menu_bar)

    def _create_shell(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        shell = ttk.Frame(self, style="Shell.TFrame", padding=(26, 14, 26, 18))
        shell.grid(row=0, column=0, sticky="nsew", padx=24, pady=20)
        shell.grid_columnconfigure(0, weight=1)
        shell.grid_rowconfigure(2, weight=1)
        self._create_header(shell)
        self._create_navigation(shell)
        self.content_container = ttk.Frame(shell, style="Shell.TFrame")
        self.content_container.grid(row=2, column=0, sticky="nsew", pady=(8, 0))
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

    def _create_header(self, parent):
        header = ttk.Frame(parent, style="Shell.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header.grid_columnconfigure(1, weight=1)
        brand = ttk.Frame(header, style="Shell.TFrame")
        brand.grid(row=0, column=0, sticky="w")
        logo = tk.Canvas(brand, width=32, height=32, bg="#ffffff", highlightthickness=0)
        logo.grid(row=0, column=0, padx=(0, 8))
        logo.create_rectangle(7, 10, 25, 26, outline="#0284c7", width=2)
        logo.create_arc(10, 3, 22, 15, start=0, extent=180, outline="#0284c7", width=2)
        logo.create_text(16, 18, text="H", fill="#0f172a", font=("Segoe UI", 9, "bold"))
        ttk.Label(brand, text="HCMUTE_ChanBoMayDe", style="Brand.TLabel").grid(row=0, column=1, sticky="w")

        search_box = tk.Frame(header, bg="#ffffff", highlightbackground="#dbe3ef", highlightthickness=1)
        search_box.grid(row=0, column=1, sticky="ew", padx=32)
        search_box.grid_columnconfigure(0, weight=1)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_box, textvariable=self.search_var, font=("Segoe UI", 10))
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(14, 6), pady=8)
        self.search_entry.insert(0, "Tìm kiếm gear công nghệ...")
        self.search_entry.bind("<FocusIn>", self._clear_search_placeholder)
        self.search_entry.bind("<Return>", self._handle_search)
        ttk.Button(search_box, text="TÌM", style="HeaderAction.TButton", command=self._handle_search).grid(
            row=0, column=1, padx=(0, 5), pady=4
        )

        actions = ttk.Frame(header, style="Shell.TFrame")
        actions.grid(row=0, column=2, sticky="e")
        ttk.Button(
            actions, text="GIỚI THIỆU", style="HeaderAction.TButton",
            command=lambda: show_info_message("Phần mềm quản lý cửa hàng gear công nghệ.", "Giới thiệu")
        ).pack(side="left", padx=(0, 4))
        ttk.Button(
            actions, text="TRỢ GIÚP", style="HeaderAction.TButton",
            command=lambda: show_info_message("Chọn Danh mục hàng hóa hoặc Thống kê để bắt đầu.", "Trợ giúp")
        ).pack(side="left")

    def _create_navigation(self, parent):
        navigation = ttk.Frame(parent, style="Shell.TFrame")
        navigation.grid(row=1, column=0, sticky="ew")
        self._add_nav_button(navigation, "home", "HOME", self.show_home, 0)
        self._add_nav_button(navigation, "hang_hoa", "DANH MỤC HÀNG HÓA", self.show_hang_hoa_view, 1)
        self._add_nav_button(navigation, "thong_ke", "THỐNG KÊ TỔNG SỐ LƯỢNG", self.show_thong_ke_view, 2)
        ttk.Separator(parent, orient="horizontal").grid(row=1, column=0, sticky="sew")

    def _add_nav_button(self, parent, key, text, command, column):
        button = ttk.Button(parent, text=text, command=command, style="Nav.TButton")
        button.grid(row=0, column=column, sticky="w", padx=(0, 8))
        self.nav_buttons[key] = button

    def _set_active_nav(self, active_key):
        for key, button in self.nav_buttons.items():
            button.configure(style="ActiveNav.TButton" if key == active_key else "Nav.TButton")

    def _clear_content(self):
        for child in self.content_container.winfo_children():
            child.destroy()
        self.current_view = None

    def _clear_search_placeholder(self, _event=None):
        if self.search_var.get() == "Tìm kiếm gear công nghệ...":
            self.search_var.set("")

    def _handle_search(self, _event=None):
        keyword = self.search_var.get().strip()
        if keyword == "Tìm kiếm gear công nghệ...":
            keyword = ""
        self.show_hang_hoa_view(keyword=keyword)

    def show_home(self):
        self._set_active_nav("home")
        self._clear_content()
        home_view = HomeView(
            self.content_container,
            on_open_products=self.show_hang_hoa_view,
            on_open_statistics=self.show_thong_ke_view,
            on_search=self._handle_home_search,
        )
        home_view.grid(row=0, column=0, sticky="nsew")
        self.current_view = home_view

    def _handle_home_search(self, keyword):
        self.search_var.set(keyword)
        self.show_hang_hoa_view(keyword=keyword)

    def show_hang_hoa_view(self, category=None, keyword=None):
        self._set_active_nav("hang_hoa")
        self.pending_category = category
        self.pending_search_keyword = keyword or ""
        self._show_external_view(
            "views.hang_hoa_view", "HangHoaView", "DANH MỤC HÀNG HÓA",
            "Màn hình quản lý hàng hóa đang chờ TV3 và TV4 bàn giao. Từ khóa hoặc danh mục "
            "từ trang chủ đã được giữ để tích hợp tiếp.",
        )

    def show_thong_ke_view(self):
        self._set_active_nav("thong_ke")
        self._show_external_view(
            "views.thong_ke_view", "ThongKeView", "THỐNG KÊ TỔNG SỐ LƯỢNG",
            "Không thể nạp màn hình thống kê của TV5.",
        )

    def _show_external_view(self, module_name, class_name, placeholder_title, placeholder_message):
        self._clear_content()
        mount = ttk.Frame(self.content_container, style="Shell.TFrame")
        mount.grid(row=0, column=0, sticky="nsew")
        mount.grid_columnconfigure(0, weight=1)
        mount.grid_rowconfigure(0, weight=1)
        try:
            module = __import__(module_name, fromlist=[class_name])
            view_class = getattr(module, class_name)
            view = view_class(mount)
            # TV5 hiện dùng pack(), còn các view khác có thể dùng grid(). Mount riêng
            # cho phép cả hai cách mà không trộn geometry manager trong cùng parent.
            if not view.winfo_manager():
                view.grid(row=0, column=0, sticky="nsew")
            self.current_view = view
            self._pass_pending_context(view)
        except (ImportError, AttributeError):
            mount.destroy()
            self._show_placeholder(placeholder_title, placeholder_message)
        except Exception as error:
            mount.destroy()
            self._show_placeholder(placeholder_title, f"Không thể mở chức năng này: {error}")

    def _pass_pending_context(self, view):
        """Gọi API TV3/TV4 khi được bàn giao, không tự xử lý SQL trong MainWindow."""
        if self.pending_search_keyword and hasattr(view, "set_search_keyword"):
            view.set_search_keyword(self.pending_search_keyword)
        if self.pending_category and hasattr(view, "set_category_filter"):
            view.set_category_filter(self.pending_category)

    def _show_placeholder(self, title, message):
        placeholder = ttk.Frame(self.content_container, style="Shell.TFrame", padding=32)
        placeholder.grid(row=0, column=0, sticky="nsew")
        placeholder.grid_columnconfigure(0, weight=1)
        ttk.Label(
            placeholder, text=title, background="#ffffff", foreground="#0f172a",
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))
        ttk.Label(
            placeholder, text=message, background="#ffffff", foreground="#475569",
            font=("Segoe UI", 10), justify="left", wraplength=760
        ).grid(row=1, column=0, sticky="w", pady=(0, 18))
        ttk.Button(
            placeholder, text="VỀ TRANG CHỦ", command=self.show_home, style="HeaderAction.TButton"
        ).grid(row=2, column=0, sticky="w")


def run_app():
    app = MainWindow()
    app.mainloop()
