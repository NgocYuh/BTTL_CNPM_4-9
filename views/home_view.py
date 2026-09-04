"""Trang HOME độc lập cho ứng dụng quản lý gear công nghệ."""

import logging
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import Image, ImageTk


LOGGER = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_IMAGE_DIR = PROJECT_ROOT / "images" / "products"


class HomeView(ttk.Frame):
    """Trang chủ ecommerce chỉ hiển thị UI, không chứa SQL hay nghiệp vụ CRUD."""

    CATEGORY_ITEMS = (
        ("Chuột gaming", "chuot-logitech-g-pro-x-superlight-2.jpg"),
        ("Bàn phím cơ", "ban-phim-keychron-k2-v2.jpg"),
        ("Tai nghe gaming", "tai-nghe-logitech-g-pro-x2.jpg"),
        ("Ghế gaming", "ghe-secretlab-titan-evo.jpg"),
        ("Micro", "micro-hyperx-quadcast-2.jpg"),
        ("Màn hình", "man-hinh-lg-ultragear-27gn800.jpg"),
    )

    def __init__(self, parent, on_open_products, on_open_statistics, on_search=None):
        super().__init__(parent, style="Home.TFrame")
        self.on_open_products = on_open_products
        self.on_open_statistics = on_open_statistics
        self.on_search = on_search
        self._images = []
        self._configure_styles()
        self._build_scroll_area()
        self._build_content()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.configure("Home.TFrame", background="#ffffff")
        style.configure(
            "HomeSection.TLabel", background="#ffffff", foreground="#0f172a", font=("Segoe UI", 15, "bold")
        )
        style.configure(
            "HomeBody.TLabel", background="#ffffff", foreground="#64748b", font=("Segoe UI", 9)
        )
        style.configure(
            "HomePrimary.TButton", background="#ffffff", foreground="#0369a1", borderwidth=0,
            padding=(14, 9), font=("Segoe UI", 9, "bold")
        )
        style.map(
            "HomePrimary.TButton", background=[("active", "#f0f9ff")], foreground=[("active", "#075985")]
        )
        style.configure(
            "HomeLink.TButton", background="#f0f9ff", foreground="#0369a1", borderwidth=0,
            padding=(11, 7), font=("Segoe UI", 9, "bold")
        )
        style.map("HomeLink.TButton", background=[("active", "#e0f2fe")])

    def _build_scroll_area(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.body = ttk.Frame(self.canvas, style="Home.TFrame", padding=(0, 0, 8, 8))
        self.body_window = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.body.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_body)
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _update_scroll_region(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_body(self, event):
        self.canvas.itemconfigure(self.body_window, width=event.width)

    def _bind_mousewheel(self, _event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event=None):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def _build_content(self):
        self.body.grid_columnconfigure(0, weight=1)
        self._build_hero()
        self._build_categories()
        self._build_feature_row()
        self._build_product_preview()

    def _build_hero(self):
        hero_area = ttk.Frame(self.body, style="Home.TFrame")
        hero_area.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        hero_area.grid_columnconfigure(0, weight=3, uniform="hero")
        hero_area.grid_columnconfigure(1, weight=1, uniform="hero")
        hero_area.grid_rowconfigure(0, weight=1)

        hero = tk.Frame(hero_area, bg="#0284c7", height=282)
        hero.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        hero.grid_propagate(False)
        hero.grid_columnconfigure(0, weight=1)
        hero.grid_columnconfigure(1, weight=1)
        hero.grid_rowconfigure(0, weight=1)
        copy = tk.Frame(hero, bg="#0284c7")
        copy.grid(row=0, column=0, sticky="nsew", padx=(28, 10), pady=28)
        tk.Label(copy, text="GAMING GEAR", bg="#0284c7", fg="#dff9ff", font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        tk.Label(
            copy, text="QUẢN LÝ CỬA HÀNG", bg="#0284c7", fg="#ffffff", font=("Segoe UI", 23, "bold")
        ).grid(row=1, column=0, sticky="w", pady=(7, 8))
        tk.Label(
            copy, text="Chuột, bàn phím cơ, tai nghe, ghế gaming,\nmicro và màn hình.",
            bg="#0284c7", fg="#e0f2fe", font=("Segoe UI", 10), justify="left"
        ).grid(row=2, column=0, sticky="w")
        ttk.Button(copy, text="MỞ DANH MỤC", style="HomePrimary.TButton", command=self.on_open_products).grid(
            row=3, column=0, sticky="w", pady=(18, 0)
        )
        self._image_label(
            hero, "chuot-logitech-g-pro-x-superlight-2.jpg", (360, 220), "#0284c7", "Ảnh chuột gaming"
        ).grid(row=0, column=1, sticky="nsew", padx=(4, 22), pady=20)

        promos = ttk.Frame(hero_area, style="Home.TFrame")
        promos.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        promos.grid_columnconfigure(0, weight=1)
        promos.grid_rowconfigure((0, 1), weight=1)
        self._build_promo(
            promos, 0, "BÀN PHÍM CƠ", "Switch êm, layout gọn", "#7c3aed", "ban-phim-keychron-k2-v2.jpg"
        )
        self._build_promo(
            promos, 1, "TAI NGHE GAMING", "Âm thanh rõ ràng, ổn định", "#0f766e", "tai-nghe-logitech-g-pro-x2.jpg"
        )

    def _build_promo(self, parent, row, title, subtitle, color, image_name):
        promo = tk.Frame(parent, bg=color, height=134)
        promo.grid(row=row, column=0, sticky="nsew", pady=(0, 8) if row == 0 else (8, 0))
        promo.grid_propagate(False)
        promo.grid_columnconfigure(0, weight=1)
        promo.grid_columnconfigure(1, weight=1)
        promo.grid_rowconfigure(0, weight=1)
        copy = tk.Frame(promo, bg=color)
        copy.grid(row=0, column=0, sticky="nsew", padx=(18, 4), pady=16)
        tk.Label(copy, text="NEW ARRIVALS", bg=color, fg="#e0f2fe", font=("Segoe UI", 7, "bold")).pack(anchor="w")
        tk.Label(copy, text=title, bg=color, fg="#ffffff", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", pady=(5, 3)
        )
        tk.Label(
            copy, text=subtitle, bg=color, fg="#f8fafc", font=("Segoe UI", 8), wraplength=132, justify="left"
        ).pack(anchor="w")
        ttk.Button(copy, text="XEM DANH MỤC", style="HomePrimary.TButton", command=self.on_open_products).pack(
            anchor="w", pady=(8, 0)
        )
        self._image_label(promo, image_name, (128, 102), color, "Ảnh sản phẩm").grid(
            row=0, column=1, sticky="nsew", padx=(2, 14), pady=14
        )

    def _build_categories(self):
        section = tk.Frame(self.body, bg="#eafaff", padx=14, pady=14)
        section.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        section.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="categories")
        for column, (category, image_name) in enumerate(self.CATEGORY_ITEMS):
            card = tk.Frame(section, bg="#eafaff", cursor="hand2")
            card.grid(row=0, column=column, sticky="nsew", padx=3)
            image = self._image_label(card, image_name, (62, 62), "#ffffff", category)
            image.pack(pady=(0, 7))
            label = tk.Label(
                card, text=category, bg="#eafaff", fg="#334155", font=("Segoe UI", 8, "bold"),
                wraplength=112, justify="center"
            )
            label.pack()
            self._bind_open_products(card, category)
            self._bind_open_products(image, category)
            self._bind_open_products(label, category)

    def _bind_open_products(self, widget, category):
        widget.bind("<Button-1>", lambda _event: self.on_open_products(category=category))

    def _build_feature_row(self):
        feature_area = ttk.Frame(self.body, style="Home.TFrame")
        feature_area.grid(row=2, column=0, sticky="ew", pady=(0, 22))
        feature_area.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="feature")
        features = (
            ("QUẢN LÝ KHO", "Theo dõi sản phẩm và tồn kho"),
            ("DỮ LIỆU AN TOÀN", "SQL Server và Stored Procedure"),
            ("CRUD HOÀN CHỈNH", "Thêm, sửa, xóa hàng hóa"),
            ("THỐNG KÊ", "Số lượng và giá trị tồn kho"),
        )
        for column, (title, text) in enumerate(features):
            item = ttk.Frame(feature_area, style="Home.TFrame")
            item.grid(row=0, column=column, sticky="nsew", padx=8)
            ttk.Label(item, text=title, style="HomeSection.TLabel", font=("Segoe UI", 9, "bold")).pack(anchor="center")
            ttk.Label(item, text=text, style="HomeBody.TLabel", justify="center").pack(anchor="center", pady=(4, 0))

    def _build_product_preview(self):
        section = ttk.Frame(self.body, style="Home.TFrame")
        section.grid(row=3, column=0, sticky="ew")
        section.grid_columnconfigure(0, weight=1)
        heading = ttk.Frame(section, style="Home.TFrame")
        heading.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        heading.grid_columnconfigure(0, weight=1)
        ttk.Label(heading, text="SẢN PHẨM NỔI BẬT", style="HomeSection.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(heading, text="XEM TẤT CẢ", style="HomeLink.TButton", command=self.on_open_products).grid(
            row=0, column=1, sticky="e"
        )
        waiting = tk.Frame(section, bg="#f8fafc", padx=20, pady=22)
        waiting.grid(row=1, column=0, sticky="ew")
        tk.Label(
            waiting, text="Đang chờ dữ liệu sản phẩm từ HangHoaService", bg="#f8fafc", fg="#334155",
            font=("Segoe UI", 10, "bold")
        ).pack()
        tk.Label(
            waiting, text="Khi TV3 bàn giao Service, trang chủ sẽ nạp danh sách theo dữ liệu SQL Server.",
            bg="#f8fafc", fg="#64748b", font=("Segoe UI", 9)
        ).pack(pady=(5, 10))
        ttk.Button(waiting, text="XEM THỐNG KÊ KHO", style="HomeLink.TButton", command=self.on_open_statistics).pack()

    def _image_label(self, parent, image_name, size, background, alternate_text):
        image = self.load_image(image_name, size, background)
        if image is None:
            return tk.Label(
                parent, text=alternate_text, bg=background, fg="#64748b", font=("Segoe UI", 8),
                justify="center", wraplength=size[0] - 8
            )
        label = tk.Label(parent, image=image, bg=background, bd=0)
        label.image = image
        return label

    def load_image(self, image_path, size, background="#ffffff"):
        """Nạp ảnh theo aspect ratio; thiếu ảnh chỉ ghi log, không làm app lỗi."""
        path = Path(image_path)
        if not path.is_absolute():
            path = PRODUCT_IMAGE_DIR / path
        if not path.is_file():
            LOGGER.warning("Không tìm thấy ảnh sản phẩm: %s", path)
            return None
        try:
            with Image.open(path) as source:
                image = source.convert("RGB")
                image.thumbnail(size, Image.Resampling.LANCZOS)
                canvas = Image.new("RGB", size, background)
                offset = ((size[0] - image.width) // 2, (size[1] - image.height) // 2)
                canvas.paste(image, offset)
            photo = ImageTk.PhotoImage(canvas)
            self._images.append(photo)
            return photo
        except (OSError, ValueError) as error:
            LOGGER.warning("Không thể tải ảnh %s: %s", path, error)
            return None
