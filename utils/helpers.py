from datetime import date, datetime
from tkinter import messagebox


def format_currency(value):
    """Dinh dang tien Viet Nam."""
    try:
        amount = float(value or 0)
    except (TypeError, ValueError):
        amount = 0

    return f"{amount:,.0f} đ"


def format_date(value, output_format="%d/%m/%Y"):
    """Dinh dang ngay thang de hien thi tren giao dien."""
    if not value:
        return ""

    if isinstance(value, (datetime, date)):
        return value.strftime(output_format)

    return str(value)


def show_error_message(message, title="Lỗi"):
    messagebox.showerror(title, message)


def show_success_message(message, title="Thành công"):
    messagebox.showinfo(title, message)


def show_info_message(message, title="Thông báo"):
    messagebox.showinfo(title, message)
