import tkinter as tk
from tkinter import ttk

from utils.helpers import show_info_message


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("HCMUTE_ChanBoMayDe - Quản lý gear công nghệ")
        self.geometry("1280x760")
        self.minsize(1100, 680)
        self.configure(bg="#b9f3fb")

        self.nav_buttons = {}

        self._configure_style()
        self._create_menu()
        self._create_shell()
        self.show_home()

    def _configure_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("App.TFrame", background="#b9f3fb")
        style.configure("Page.TFrame", background="#ffffff")

        style.configure(
            "Logo.TLabel",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 15, "bold"),
        )
        style.configure(
            "Nav.TButton",
            background="#ffffff",
            foreground="#111827",
            borderwidth=0,
            padding=(12, 8),
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Nav.TButton",
            background=[("active", "#e0f7ff"), ("pressed", "#c7eefc")],
            foreground=[("active", "#0284c7"), ("pressed", "#0369a1")],
        )
        style.configure(
            "ActiveNav.TButton",
            background="#e0f7ff",
            foreground="#0284c7",
            borderwidth=0,
            padding=(12, 8),
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "ActiveNav.TButton",
            background=[("active", "#c7eefc"), ("pressed", "#bae6fd")],
            foreground=[("active", "#0369a1"), ("pressed", "#075985")],
        )
        style.configure(
            "Primary.TButton",
            background="#ffffff",
            foreground="#0284c7",
            padding=(16, 10),
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#f0f9ff"), ("pressed", "#e0f2fe")],
            foreground=[("active", "#0369a1"), ("pressed", "#075985")],
        )
        style.configure(
            "Action.TButton",
            background="#f8fafc",
            foreground="#111827",
            borderwidth=0,
            padding=(10, 8),
            font=("Segoe UI", 11, "bold"),
        )
        style.map("Action.TButton", background=[("active", "#e0f2fe")])

        style.configure(
            "Tiny.TLabel",
            background="#ffffff",
            foreground="#64748b",
            font=("Segoe UI", 8),
        )
        style.configure(
            "SectionTitle.TLabel",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 13, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background="#ffffff",
            foreground="#475569",
            font=("Segoe UI", 10),
        )
        style.configure(
            "FeatureTitle.TLabel",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 9, "bold"),
        )
        style.configure(
            "FeatureText.TLabel",
            background="#ffffff",
            foreground="#64748b",
            font=("Segoe UI", 8),
        )

    def _create_menu(self):
        menu_bar = tk.Menu(self)
        danh_muc_menu = tk.Menu(menu_bar, tearoff=0)
        danh_muc_menu.add_command(
            label="Danh mục hàng hóa",
            command=self.show_hang_hoa_view,
        )
        danh_muc_menu.add_command(
            label="Thống kê tổng số lượng",
            command=self.show_thong_ke_view,
        )
        danh_muc_menu.add_separator()
        danh_muc_menu.add_command(label="Thoát", command=self.destroy)

        menu_bar.add_cascade(label="DANH MỤC", menu=danh_muc_menu)
        self.config(menu=menu_bar)

    def _create_shell(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        background = tk.Canvas(self, bg="#b9f3fb", highlightthickness=0)
        background.grid(row=0, column=0, sticky="nsew")
        background.bind("<Configure>", self._draw_background)

        self.page = ttk.Frame(background, style="Page.TFrame")
        self.page_window = background.create_window(
            70,
            52,
            anchor="nw",
            window=self.page,
        )
        background.bind(
            "<Configure>",
            lambda event: self._resize_page(background, event.width, event.height),
            add="+",
        )

        self.page.grid_columnconfigure(0, weight=1)
        self.page.grid_rowconfigure(2, weight=1)

        self._create_header()
        self._create_navigation()

        self.content_frame = ttk.Frame(self.page, style="Page.TFrame")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def _draw_background(self, event):
        canvas = event.widget
        canvas.delete("background")
        width = event.width
        height = event.height

        for index in range(0, width, 36):
            canvas.create_line(
                index,
                0,
                index,
                height,
                fill="#d8fbff",
                tags="background",
            )
        for index in range(0, height, 36):
            canvas.create_line(
                0,
                index,
                width,
                index,
                fill="#d8fbff",
                tags="background",
            )
        canvas.create_oval(
            -180,
            -180,
            520,
            520,
            fill="#74e4f5",
            outline="",
            tags="background",
        )
        canvas.create_oval(
            width - 420,
            height - 360,
            width + 180,
            height + 180,
            fill="#a7d8ff",
            outline="",
            tags="background",
        )
        canvas.tag_lower("background")

    def _resize_page(self, canvas, width, height):
        page_width = max(980, min(width - 140, 1260))
        page_height = max(620, height - 104)
        left = max(30, (width - page_width) // 2)
        top = max(24, (height - page_height) // 2)

        canvas.coords(self.page_window, left, top)
        canvas.itemconfigure(self.page_window, width=page_width, height=page_height)

    def _create_header(self):
        header = ttk.Frame(self.page, style="Page.TFrame", padding=(34, 18, 34, 8))
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        logo_area = ttk.Frame(header, style="Page.TFrame")
        logo_area.grid(row=0, column=0, sticky="w")

        logo_icon = tk.Canvas(
            logo_area,
            width=30,
            height=30,
            bg="#ffffff",
            highlightthickness=0,
        )
        logo_icon.grid(row=0, column=0, padx=(0, 8))
        logo_icon.create_rectangle(7, 8, 23, 25, outline="#0ea5e9", width=2)
        logo_icon.create_arc(9, 2, 21, 14, start=0, extent=180, outline="#0ea5e9", width=2)
        logo_icon.create_text(15, 17, text="H", fill="#111827", font=("Segoe UI", 9, "bold"))

        ttk.Label(
            logo_area,
            text="HCMUTE_ChanBoMayDe",
            style="Logo.TLabel",
        ).grid(row=0, column=1, sticky="w")

        search_frame = tk.Frame(
            header,
            bg="#ffffff",
            highlightthickness=1,
            highlightbackground="#e2e8f0",
        )
        search_frame.grid(row=0, column=1, sticky="ew", padx=34)
        search_frame.grid_columnconfigure(1, weight=1)

        tk.Label(
            search_frame,
            text="⌕",
            bg="#ffffff",
            fg="#0284c7",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, padx=(14, 8), pady=8)
        self.search_var = tk.StringVar(value="Tìm kiếm gear công nghệ...")
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew", pady=8)
        search_entry.bind("<FocusIn>", self._clear_search_placeholder)

        action_area = ttk.Frame(header, style="Page.TFrame")
        action_area.grid(row=0, column=2, sticky="e")

        for text, title in (
            ("♡", "Yêu thích"),
            ("🛒", "Giỏ mẫu"),
            ("⚙", "Cài đặt"),
        ):
            ttk.Button(
                action_area,
                text=text,
                width=3,
                style="Action.TButton",
                command=lambda message=title: show_info_message(
                    f"{message} sẽ được tích hợp sau.",
                    "Thông báo",
                ),
            ).pack(side="left", padx=3)

    def _clear_search_placeholder(self, _event):
        if self.search_var.get() == "Tìm kiếm gear công nghệ...":
            self.search_var.set("")

    def _create_navigation(self):
        nav = ttk.Frame(self.page, style="Page.TFrame", padding=(34, 4, 34, 12))
        nav.grid(row=1, column=0, sticky="ew")
        nav.grid_columnconfigure(5, weight=1)

        self._add_nav_button(nav, "home", "HOME", self.show_home, 0)
        self._add_nav_button(nav, "hang_hoa", "DANH MỤC HÀNG HÓA", self.show_hang_hoa_view, 1)
        self._add_nav_button(nav, "thong_ke", "THỐNG KÊ TỔNG SỐ LƯỢNG", self.show_thong_ke_view, 2)

        quick_links = ttk.Frame(nav, style="Page.TFrame")
        quick_links.grid(row=0, column=5, sticky="e")
        for text in ("Hot Deals", "Kiểm kho", "Demo lớp"):
            ttk.Label(quick_links, text=text, style="Tiny.TLabel").pack(side="left", padx=10)

    def _add_nav_button(self, parent, key, text, command, column):
        button = ttk.Button(parent, text=text, command=command, style="Nav.TButton")
        button.grid(row=0, column=column, sticky="w", padx=(0, 8))
        self.nav_buttons[key] = button

    def _set_active_nav(self, active_key):
        for key, button in self.nav_buttons.items():
            button.configure(style="ActiveNav.TButton" if key == active_key else "Nav.TButton")

    def _clear_content(self):
        for child in self.content_frame.winfo_children():
            child.destroy()

    def show_home(self):
        self._set_active_nav("home")
        self._clear_content()

        home = ttk.Frame(self.content_frame, style="Page.TFrame")
        home.grid(row=0, column=0, sticky="nsew")
        home.grid_columnconfigure(0, weight=2)
        home.grid_columnconfigure(1, weight=1)
        home.grid_rowconfigure(0, weight=1)

        left = ttk.Frame(home, style="Page.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)

        right = ttk.Frame(home, style="Page.TFrame")
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure((0, 1), weight=1)

        self._create_hero(left)
        self._create_category_strip(left)
        self._create_service_row(left)
        self._create_feature_products(left)

        self._create_side_banner(
            right,
            row=0,
            title="BÀN PHÍM CƠ",
            subtitle="Switch êm, layout gọn",
            accent="#a855f7",
            command=self.show_hang_hoa_view,
        )
        self._create_side_banner(
            right,
            row=1,
            title="TAI NGHE GAMING",
            subtitle="Âm thanh rõ, mic ổn định",
            accent="#14b8a6",
            command=self.show_hang_hoa_view,
        )

    def _create_hero(self, parent):
        hero = tk.Canvas(parent, height=300, bg="#0ea5e9", highlightthickness=0)
        hero.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 8))
        hero.bind("<Configure>", self._draw_hero)
        hero.bind("<Button-1>", lambda _event: self.show_hang_hoa_view())

    def _draw_hero(self, event):
        canvas = event.widget
        canvas.delete("all")
        width = event.width
        height = event.height

        canvas.create_rectangle(0, 0, width, height, fill="#0284c7", outline="")
        canvas.create_rectangle(0, 0, width, height // 2, fill="#0ea5e9", outline="")
        canvas.create_rectangle(0, height - 72, width, height, fill="#075985", outline="")

        canvas.create_text(
            42,
            90,
            text="GAMING GEAR",
            fill="#dff9ff",
            anchor="w",
            font=("Segoe UI", 10, "bold"),
        )
        canvas.create_text(
            42,
            125,
            text="QUẢN LÝ CỬA HÀNG",
            fill="#ffffff",
            anchor="w",
            font=("Segoe UI", 24, "bold"),
        )
        canvas.create_text(
            42,
            160,
            text="Chuột, phím cơ, tai nghe, ghế, micro và màn hình",
            fill="#e0f2fe",
            anchor="w",
            font=("Segoe UI", 10),
        )
        canvas.create_rectangle(42, 190, 132, 226, fill="#ffffff", outline="")
        canvas.create_text(
            87,
            208,
            text="MỞ DANH MỤC",
            fill="#0284c7",
            font=("Segoe UI", 8, "bold"),
        )

        cx = max(470, width - 275)
        cy = 154
        canvas.create_oval(cx - 155, cy - 52, cx + 155, cy + 54, fill="#111827", outline="")
        canvas.create_oval(
            cx - 128,
            cy - 35,
            cx - 58,
            cy + 35,
            fill="#0f172a",
            outline="#38bdf8",
            width=3,
        )
        canvas.create_oval(
            cx + 58,
            cy - 35,
            cx + 128,
            cy + 35,
            fill="#0f172a",
            outline="#38bdf8",
            width=3,
        )
        canvas.create_rectangle(
            cx - 82,
            cy - 42,
            cx + 82,
            cy + 42,
            fill="#1e293b",
            outline="#38bdf8",
            width=2,
        )
        canvas.create_oval(cx - 70, cy - 20, cx - 34, cy + 16, fill="#334155", outline="")
        canvas.create_oval(cx + 34, cy - 20, cx + 70, cy + 16, fill="#334155", outline="")
        canvas.create_text(cx - 52, cy - 2, text="+", fill="#ffffff", font=("Segoe UI", 18, "bold"))
        for dx, dy, label, color in (
            (52, -17, "Y", "#22c55e"),
            (69, 0, "B", "#ef4444"),
            (35, 0, "X", "#3b82f6"),
            (52, 17, "A", "#f59e0b"),
        ):
            canvas.create_oval(
                cx + dx - 10,
                cy + dy - 10,
                cx + dx + 10,
                cy + dy + 10,
                fill=color,
                outline="",
            )
            canvas.create_text(cx + dx, cy + dy, text=label, fill="#ffffff", font=("Segoe UI", 7, "bold"))

        for dot in range(5):
            x = width // 2 - 42 + dot * 21
            fill = "#0284c7" if dot == 0 else "#e0f2fe"
            canvas.create_oval(x, height - 26, x + 7, height - 19, fill=fill, outline="")

    def _create_side_banner(self, parent, row, title, subtitle, accent, command):
        banner = tk.Canvas(parent, height=146, bg=accent, highlightthickness=0)
        banner.grid(row=row, column=0, sticky="nsew", pady=(0, 8) if row == 0 else (8, 0))
        banner.bind(
            "<Configure>",
            lambda event: self._draw_side_banner(event, title, subtitle, accent),
        )
        banner.bind("<Button-1>", lambda _event: command())

    def _draw_side_banner(self, event, title, subtitle, accent):
        canvas = event.widget
        canvas.delete("all")
        width = event.width
        height = event.height

        canvas.create_rectangle(0, 0, width, height, fill=accent, outline="")
        canvas.create_oval(width - 160, -60, width + 54, height + 70, fill="#ffffff", outline="")
        canvas.create_text(28, 48, text="NEW ARRIVALS", fill="#dcfce7", anchor="w", font=("Segoe UI", 8, "bold"))
        canvas.create_text(28, 76, text=title, fill="#ffffff", anchor="w", font=("Segoe UI", 17, "bold"))
        canvas.create_text(28, 102, text=subtitle, fill="#f8fafc", anchor="w", font=("Segoe UI", 9))
        canvas.create_text(28, 126, text="Xem ngay  →", fill="#ffffff", anchor="w", font=("Segoe UI", 8, "bold"))

        center_x = width - 74
        center_y = height // 2
        if "PHÍM" in title:
            for index in range(4):
                canvas.create_rectangle(
                    center_x - 58 + index * 28,
                    center_y - 14,
                    center_x - 38 + index * 28,
                    center_y + 8,
                    fill="#0f172a",
                    outline="#38bdf8",
                    width=2,
                )
            canvas.create_rectangle(
                center_x - 70,
                center_y + 16,
                center_x + 68,
                center_y + 36,
                fill="#111827",
                outline="",
            )
            canvas.create_line(
                center_x - 56,
                center_y + 26,
                center_x + 54,
                center_y + 26,
                fill="#38bdf8",
                width=2,
            )
        else:
            canvas.create_oval(
                center_x - 54,
                center_y - 50,
                center_x + 54,
                center_y + 50,
                outline="#0f172a",
                width=10,
            )
            canvas.create_oval(center_x - 72, center_y - 14, center_x - 34, center_y + 44, fill="#0f172a", outline="")
            canvas.create_oval(center_x + 34, center_y - 14, center_x + 72, center_y + 44, fill="#0f172a", outline="")
            canvas.create_line(center_x + 56, center_y + 40, center_x + 84, center_y + 58, fill="#0f172a", width=4)

    def _create_category_strip(self, parent):
        strip = tk.Frame(parent, bg="#dff9ff", height=122)
        strip.grid(row=1, column=0, sticky="ew", pady=8)
        strip.grid_propagate(False)
        strip.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        categories = (
            ("🖱", "Chuột gaming"),
            ("⌨", "Bàn phím cơ"),
            ("🎧", "Tai nghe"),
            ("▣", "Ghế gaming"),
            ("🎙", "Micro"),
            ("▭", "Màn hình"),
        )
        for column, (icon, label) in enumerate(categories):
            item = tk.Frame(strip, bg="#dff9ff")
            item.grid(row=0, column=column, sticky="nsew", pady=14)
            item.bind("<Button-1>", lambda _event: self.show_hang_hoa_view())

            circle = tk.Canvas(item, width=66, height=66, bg="#dff9ff", highlightthickness=0)
            circle.pack()
            circle.create_oval(5, 5, 61, 61, fill="#ffffff", outline="#bae6fd", width=2)
            circle.create_text(33, 33, text=icon, fill="#0284c7", font=("Segoe UI", 19, "bold"))
            tk.Label(
                item,
                text=label,
                bg="#dff9ff",
                fg="#334155",
                font=("Segoe UI", 8, "bold"),
            ).pack(pady=(4, 0))

    def _create_service_row(self, parent):
        row = ttk.Frame(parent, style="Page.TFrame")
        row.grid(row=2, column=0, sticky="ew", pady=14)
        row.grid_columnconfigure((0, 1, 2, 3), weight=1)

        services = (
            ("📦", "QUẢN LÝ KHO", "Theo dõi số lượng tồn"),
            ("🛡", "DỮ LIỆU AN TOÀN", "Tách GUI, Service, Repository"),
            ("🔁", "TÍCH HỢP MODULE", "Sẵn sàng nối CRUD và thống kê"),
            ("☎", "DEMO TRÊN LỚP", "Giao diện rõ, dễ thao tác"),
        )
        for column, (icon, title, description) in enumerate(services):
            box = ttk.Frame(row, style="Page.TFrame")
            box.grid(row=0, column=column, sticky="ew", padx=8)
            tk.Label(box, text=icon, bg="#ffffff", fg="#0284c7", font=("Segoe UI", 17)).pack()
            ttk.Label(box, text=title, style="FeatureTitle.TLabel").pack(pady=(6, 2))
            ttk.Label(box, text=description, style="FeatureText.TLabel").pack()

    def _create_feature_products(self, parent):
        row = ttk.Frame(parent, style="Page.TFrame")
        row.grid(row=3, column=0, sticky="ew", pady=(4, 0))
        row.grid_columnconfigure((0, 1, 2), weight=1, uniform="products")

        products = (
            ("CHUỘT GAMING", "Logitech G Pro X Superlight", "#e0f2fe", self._draw_mouse),
            ("MICRO", "HyperX SoloCast", "#fee2e2", self._draw_micro),
            ("MÀN HÌNH", "LG UltraGear 24GN60R", "#dcfce7", self._draw_monitor),
        )
        for column, (title, name, color, draw_func) in enumerate(products):
            card = tk.Canvas(row, height=150, bg=color, highlightthickness=0)
            card.grid(row=0, column=column, sticky="ew", padx=6)
            card.bind(
                "<Configure>",
                lambda event, card_title=title, product_name=name, drawer=draw_func: self._draw_product_card(
                    event,
                    card_title,
                    product_name,
                    drawer,
                ),
            )
            card.bind("<Button-1>", lambda _event: self.show_hang_hoa_view())

    def _draw_product_card(self, event, title, name, draw_func):
        canvas = event.widget
        canvas.delete("content")
        width = event.width
        height = event.height

        draw_func(canvas, width, height)
        canvas.create_text(
            width // 2,
            height - 38,
            text=title,
            fill="#111827",
            font=("Segoe UI", 9, "bold"),
            tags="content",
        )
        canvas.create_text(
            width // 2,
            height - 18,
            text=name,
            fill="#475569",
            font=("Segoe UI", 8),
            tags="content",
        )

    def _draw_mouse(self, canvas, width, _height):
        x = width // 2
        canvas.create_oval(
            x - 38,
            26,
            x + 38,
            96,
            fill="#111827",
            outline="#38bdf8",
            width=2,
            tags="content",
        )
        canvas.create_line(x, 28, x, 58, fill="#38bdf8", width=2, tags="content")
        canvas.create_oval(x - 5, 43, x + 5, 55, fill="#38bdf8", outline="", tags="content")

    def _draw_micro(self, canvas, width, _height):
        x = width // 2
        canvas.create_oval(
            x - 32,
            20,
            x + 32,
            84,
            fill="#111827",
            outline="#38bdf8",
            width=2,
            tags="content",
        )
        canvas.create_rectangle(x - 22, 47, x + 22, 84, fill="#1e293b", outline="", tags="content")
        canvas.create_line(x, 84, x, 105, fill="#111827", width=5, tags="content")
        canvas.create_line(x - 30, 105, x + 30, 105, fill="#111827", width=5, tags="content")

    def _draw_monitor(self, canvas, width, _height):
        x = width // 2
        canvas.create_rectangle(
            x - 60,
            24,
            x + 60,
            88,
            fill="#111827",
            outline="#38bdf8",
            width=3,
            tags="content",
        )
        canvas.create_rectangle(x - 48, 34, x + 48, 76, fill="#0ea5e9", outline="", tags="content")
        canvas.create_line(x, 88, x, 108, fill="#111827", width=5, tags="content")
        canvas.create_line(x - 34, 108, x + 34, 108, fill="#111827", width=5, tags="content")

    def show_hang_hoa_view(self):
        self._set_active_nav("hang_hoa")
        self._show_external_view(
            module_name="views.hang_hoa_view",
            class_name="HangHoaView",
            placeholder_title="DANH MỤC HÀNG HÓA",
            placeholder_message="Màn hình quản lý hàng hóa sẽ được TV3 và TV4 triển khai.",
        )

    def show_thong_ke_view(self):
        self._set_active_nav("thong_ke")
        self._show_external_view(
            module_name="views.thong_ke_view",
            class_name="ThongKeView",
            placeholder_title="THỐNG KÊ TỔNG SỐ LƯỢNG",
            placeholder_message="Màn hình thống kê tổng số lượng sẽ được TV5 triển khai.",
        )

    def _show_external_view(self, module_name, class_name, placeholder_title, placeholder_message):
        self._clear_content()

        try:
            module = __import__(module_name, fromlist=[class_name])
            view_class = getattr(module, class_name)
            view = view_class(self.content_frame)
            view.grid(row=0, column=0, sticky="nsew")
        except (ImportError, AttributeError):
            self._show_placeholder(placeholder_title, placeholder_message)
        except Exception as exc:
            self._show_placeholder(placeholder_title, f"Không thể mở chức năng này: {exc}")
            show_info_message(
                "Chức năng đang được tích hợp. Vui lòng kiểm tra lại module liên quan.",
                "Thông báo",
            )

    def _show_placeholder(self, title, message):
        placeholder = ttk.Frame(self.content_frame, style="Page.TFrame", padding=34)
        placeholder.grid(row=0, column=0, sticky="nsew")
        placeholder.grid_columnconfigure(0, weight=1)

        ttk.Label(placeholder, text=title, style="SectionTitle.TLabel").grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 10),
        )
        ttk.Label(
            placeholder,
            text=message,
            style="Body.TLabel",
            wraplength=720,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(0, 18))
        ttk.Button(
            placeholder,
            text="Về trang chủ",
            command=self.show_home,
            style="Primary.TButton",
        ).grid(row=2, column=0, sticky="w")


def run_app():
    app = MainWindow()
    app.mainloop()
