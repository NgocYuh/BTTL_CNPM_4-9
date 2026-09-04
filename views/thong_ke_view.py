"""
Statistics View (Thống Kê Tổng Số Lượng & Theo Danh Mục)
Displays summary metric cards, category breakdown treeview, and stock charts.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Optional

from repositories.hang_hoa_repository import HangHoaRepository

# Thử import từ helpers nếu có, nếu chưa có thì dùng hàm nội bộ an toàn
try:
    from utils.helpers import format_currency, format_number
except ImportError:
    try:
        from utils.helpers import format_currency
        def format_number(val):
            if val is None:
                return "0"
            return f"{int(round(float(val))):,}"
    except ImportError:
        def format_currency(val):
            if val is None:
                return "0 ₫"
            try:
                return f"{int(round(float(val))):,} ₫"
            except (ValueError, TypeError):
                return "0 ₫"

        def format_number(val):
            if val is None:
                return "0"
            try:
                return f"{int(round(float(val))):,}"
            except (ValueError, TypeError):
                return "0"

# Thử import matplotlib cho biểu đồ với cơ chế fallback sang Tkinter Canvas
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class ThongKeView(ttk.Frame):
    """
    Statistics & Reporting Screen.
    """

    def __init__(self, parent, hang_hoa_service: Optional[Any] = None, repository: Optional[HangHoaRepository] = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.hang_hoa_service = hang_hoa_service
        self.repository = repository or HangHoaRepository()
        self.chart_canvas = None

        self._configure_styles()
        self._init_ui()
        self.load_statistics()

    def _configure_styles(self):
        """Cấu hình style giao diện nếu chưa có."""
        style = ttk.Style(self)
        try:
            style.configure(
                "Header.TLabel",
                font=("Segoe UI", 15, "bold"),
                foreground="#1E293B",
            )
            style.configure(
                "Primary.TButton",
                font=("Segoe UI", 10, "bold"),
            )
        except Exception:
            pass

    def _init_ui(self):
        """Build the statistics interface."""
        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # ---------------------------------------------------------------------
        # 1. HEADER BANNER
        # ---------------------------------------------------------------------
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))

        lbl_title = ttk.Label(
            header_frame,
            text="📊 THỐNG KÊ TỔNG SỐ LƯỢNG & TỒN KHO",
            style="Header.TLabel"
        )
        lbl_title.pack(side="left")

        btn_refresh = ttk.Button(
            header_frame,
            text="🔄 CẬP NHẬT THỐNG KÊ",
            style="Primary.TButton",
            command=self.load_statistics
        )
        btn_refresh.pack(side="right")

        # ---------------------------------------------------------------------
        # 2. STATISTIC SUMMARY CARDS (3 Big Cards)
        # ---------------------------------------------------------------------
        cards_frame = ttk.Frame(self)
        cards_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)

        # Card 1: Tổng số loại hàng
        card1 = ttk.LabelFrame(cards_frame, text="📦 TỔNG SỐ LOẠI HÀNG", padding=15)
        card1.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
        self.lbl_card1_val = ttk.Label(card1, text="0", font=("Segoe UI", 22, "bold"), foreground="#1E40AF")
        self.lbl_card1_val.pack(anchor="center", pady=5)
        ttk.Label(card1, text="Mặt hàng khác nhau", font=("Segoe UI", 9), foreground="#64748B").pack(anchor="center")

        # Card 2: Tổng số lượng hàng
        card2 = ttk.LabelFrame(cards_frame, text="🔢 TỔNG SỐ LƯỢNG TỒN", padding=15)
        card2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.lbl_card2_val = ttk.Label(card2, text="0", font=("Segoe UI", 22, "bold"), foreground="#059669")
        self.lbl_card2_val.pack(anchor="center", pady=5)
        ttk.Label(card2, text="Sản phẩm trong kho", font=("Segoe UI", 9), foreground="#64748B").pack(anchor="center")

        # Card 3: Tổng giá trị tồn kho
        card3 = ttk.LabelFrame(cards_frame, text="💰 TỔNG GIÁ TRỊ TỒN KHO", padding=15)
        card3.grid(row=0, column=2, sticky="nsew", padx=(10, 0), pady=5)
        self.lbl_card3_val = ttk.Label(card3, text="0 ₫", font=("Segoe UI", 20, "bold"), foreground="#D97706")
        self.lbl_card3_val.pack(anchor="center", pady=5)
        ttk.Label(card3, text="Ước tính theo đơn giá", font=("Segoe UI", 9), foreground="#64748B").pack(anchor="center")

        # ---------------------------------------------------------------------
        # 3. SPLIT PANE: CATEGORY BREAKDOWN TABLE + CHART
        # ---------------------------------------------------------------------
        split_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        split_pane.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 15))

        # --- LEFT: CATEGORY TABLE ---
        cat_table_frame = ttk.LabelFrame(split_pane, text="📋 THỐNG KÊ THEO DANH MỤC", padding=10)
        split_pane.add(cat_table_frame, weight=3)

        cat_table_frame.rowconfigure(0, weight=1)
        cat_table_frame.columnconfigure(0, weight=1)

        scroll_y = ttk.Scrollbar(cat_table_frame, orient="vertical")
        columns = ("ten_danh_muc", "so_loai_hang", "tong_so_luong", "tong_gia_tri")
        self.tree_cat = ttk.Treeview(
            cat_table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.tree_cat.yview)

        self.tree_cat.heading("ten_danh_muc", text="Tên danh mục", anchor="w")
        self.tree_cat.heading("so_loai_hang", text="Số loại hàng", anchor="center")
        self.tree_cat.heading("tong_so_luong", text="Tổng số lượng", anchor="center")
        self.tree_cat.heading("tong_gia_tri", text="Tổng giá trị tồn", anchor="e")

        self.tree_cat.column("ten_danh_muc", width=140, minwidth=110, anchor="w")
        self.tree_cat.column("so_loai_hang", width=90, minwidth=80, anchor="center")
        self.tree_cat.column("tong_so_luong", width=100, minwidth=90, anchor="center")
        self.tree_cat.column("tong_gia_tri", width=140, minwidth=110, anchor="e")

        self.tree_cat.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        self.tree_cat.tag_configure("even", background="#F8FAFC")
        self.tree_cat.tag_configure("odd", background="#FFFFFF")

        # --- RIGHT: CHART FRAME ---
        self.chart_frame = ttk.LabelFrame(split_pane, text="📊 Biểu đồ số lượng theo danh mục", padding=10)
        split_pane.add(self.chart_frame, weight=3)
        self.chart_frame.rowconfigure(0, weight=1)
        self.chart_frame.columnconfigure(0, weight=1)

    # -------------------------------------------------------------------------
    # DATA LOADING & CHART RENDERING
    # -------------------------------------------------------------------------
    def load_statistics(self):
        """Fetch updated statistics from database and refresh cards, table, and chart."""
        try:
            # 1. Load summary metrics
            if self.hang_hoa_service and hasattr(self.hang_hoa_service, "get_summary_statistics"):
                summary = self.hang_hoa_service.get_summary_statistics()
                val_types = summary.get("tong_so_loai", 0)
                val_quantity = summary.get("tong_so_luong", 0)
                val_total = summary.get("tong_gia_tri", 0)
            else:
                val_types = self.repository.get_total_product_types()
                val_quantity = self.repository.get_total_quantity()
                val_total = self.repository.get_total_inventory_value()

            self.lbl_card1_val.config(text=format_number(val_types))
            self.lbl_card2_val.config(text=format_number(val_quantity))
            self.lbl_card3_val.config(text=format_currency(val_total))

            # 2. Load category breakdown table
            if self.hang_hoa_service and hasattr(self.hang_hoa_service, "get_category_statistics"):
                cat_stats_raw = self.hang_hoa_service.get_category_statistics()
            else:
                cat_stats_raw = self.repository.get_statistics_by_category()

            # Chuẩn hóa cấu trúc dictionary
            cat_stats: List[Dict[str, Any]] = []
            for item in cat_stats_raw:
                cat_stats.append({
                    "ten_danh_muc": item.get("ten_danh_muc") or item.get("TenDanhMuc", ""),
                    "so_loai_hang": item.get("so_loai_hang", 0) if "so_loai_hang" in item else item.get("SoLoaiHang", 0),
                    "tong_so_luong": item.get("tong_so_luong", 0) if "tong_so_luong" in item else item.get("TongSoLuong", 0),
                    "tong_gia_tri": item.get("tong_gia_tri", 0) if "tong_gia_tri" in item else item.get("TongGiaTri", 0),
                })

            for item in self.tree_cat.get_children():
                self.tree_cat.delete(item)

            for idx, item in enumerate(cat_stats):
                tag = "even" if idx % 2 == 0 else "odd"
                self.tree_cat.insert(
                    "",
                    "end",
                    values=(
                        item["ten_danh_muc"],
                        format_number(item["so_loai_hang"]),
                        format_number(item["tong_so_luong"]),
                        format_currency(item["tong_gia_tri"])
                    ),
                    tags=(tag,)
                )

            # 3. Render chart
            self.render_chart(cat_stats)

        except Exception as e:
            messagebox.showerror("Lỗi thống kê", f"Không thể lấy dữ liệu thống kê:\n{str(e)}")

    def render_chart(self, cat_stats: List[Dict[str, Any]]):
        """Render a clean bar chart showing inventory quantity distribution."""
        # Clear existing chart canvas if present
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not cat_stats:
            lbl_empty = ttk.Label(self.chart_frame, text="Chưa có dữ liệu để vẽ biểu đồ", foreground="#64748B")
            lbl_empty.pack(expand=True)
            return

        categories = [item["ten_danh_muc"] for item in cat_stats]
        quantities = [item["tong_so_luong"] for item in cat_stats]

        if MATPLOTLIB_AVAILABLE:
            try:
                fig = Figure(figsize=(4.5, 3.2), dpi=100, facecolor="#F8FAFC")
                ax = fig.add_subplot(111)
                fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.3)

                bars = ax.bar(categories, quantities, color="#3B82F6", edgecolor="#1D4ED8", width=0.55)
                ax.set_facecolor("#FFFFFF")
                ax.set_ylabel("Số lượng tồn", fontsize=9, color="#334155")
                ax.set_title("Số lượng hàng hóa theo danh mục", fontsize=10, fontweight="bold", color="#1E293B")
                ax.tick_params(axis="x", rotation=25, labelsize=8)
                ax.tick_params(axis="y", labelsize=8)
                ax.grid(axis="y", linestyle="--", alpha=0.5)

                # Add value labels on top of bars
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        ax.annotate(
                            f'{int(height)}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 2),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1E40AF'
                        )

                canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                return
            except Exception:
                pass

        # Fallback pure Tkinter Canvas bar chart if matplotlib is unavailable or fails
        self._render_tk_canvas_chart(categories, quantities)

    def _render_tk_canvas_chart(self, categories: List[str], quantities: List[int]):
        """Pure Tkinter fallback bar chart with no third-party dependency."""
        canvas = tk.Canvas(self.chart_frame, bg="#FFFFFF", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        max_qty = max(quantities) if quantities and max(quantities) > 0 else 1
        num_bars = len(categories)
        if num_bars == 0:
            return

        def draw_bars(event=None):
            canvas.delete("all")
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            if w <= 10 or h <= 10:
                return

            margin_left = 40
            margin_bottom = 45
            margin_top = 25
            margin_right = 20

            chart_w = w - margin_left - margin_right
            chart_h = h - margin_bottom - margin_top

            # Draw axes
            canvas.create_line(margin_left, h - margin_bottom, w - margin_right, h - margin_bottom, fill="#CBD5E1", width=2)
            canvas.create_line(margin_left, margin_top, margin_left, h - margin_bottom, fill="#CBD5E1", width=2)

            bar_width = min(40, (chart_w / num_bars) * 0.6)
            spacing = chart_w / num_bars

            for idx, (cat, qty) in enumerate(zip(categories, quantities)):
                bar_h = (qty / max_qty) * (chart_h - 10)
                x0 = margin_left + idx * spacing + (spacing - bar_width) / 2
                x1 = x0 + bar_width
                y0 = h - margin_bottom - bar_h
                y1 = h - margin_bottom

                # Bar
                canvas.create_rectangle(x0, y0, x1, y1, fill="#3B82F6", outline="#1D4ED8")
                # Value label
                canvas.create_text((x0 + x1) / 2, y0 - 8, text=str(qty), fill="#1E40AF", font=("Segoe UI", 8, "bold"))
                # Category label (truncated if long)
                display_cat = cat if len(cat) <= 10 else cat[:9] + ".."
                canvas.create_text((x0 + x1) / 2, h - margin_bottom + 15, text=display_cat, fill="#475569", font=("Segoe UI", 8))

        canvas.bind("<Configure>", draw_bars)
