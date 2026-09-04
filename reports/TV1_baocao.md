# Báo cáo Thành viên 1 - Giao diện chính và tích hợp

## 1. Phạm vi thực hiện

TV1 phụ trách cửa sổ gốc, navigation, giao diện HOME, `main.py`, các helper dùng chung và tích hợp các view của thành viên khác. Lần cập nhật này chỉ refactor phần frontend thuộc TV1, không làm lại CRUD, database hay thống kê.

## 2. Đã làm được

- Tách toàn bộ HOME khỏi `views/main_window.py` sang `views/home_view.py`.
- Giữ `MainWindow` gọn, chỉ chịu trách nhiệm tạo một `Tk` root, header, menu, navigation và vùng `content_container` để chuyển view.
- Thiết kế lại HOME theo hierarchy của ảnh tham khảo: header có brand/search, navigation, hero lớn và hai promo card, category strip, feature row, product preview.
- Đổi nền cửa sổ sang trắng/xám nhạt; dùng xanh dương làm màu chính, tím và teal cho promo. Không dùng nền cyan phủ toàn bộ giao diện.
- Dùng `grid()` cho các vùng layout chính; HOME có Canvas + scrollbar và hỗ trợ cuộn bằng con lăn chuột khi nội dung dài hơn cửa sổ.
- Tạo `HomeView.load_image()` dùng Pillow, `Image.Resampling.LANCZOS` và letterbox để giữ đúng tỷ lệ ảnh. Ảnh thiếu chỉ ghi log và hiển thị nhãn dự phòng, không làm chương trình dừng.
- Sử dụng ảnh thật trong `images/products/` cho hero, promo và sáu danh mục. Đã kiểm tra thư mục có 60 ảnh JPG hợp lệ.
- Bổ sung `Pillow>=10.0.0` vào `requirements.txt`.
- Hoàn thiện điều hướng HOME sang Danh mục hàng hóa và Thống kê. Khi click danh mục, `MainWindow` giữ lại category để TV3/TV4 nhận khi API filter được bàn giao.
- Hoàn thiện global search ở header: bấm Enter hoặc nút `TÌM` sẽ chuyển sang màn hàng hóa và giữ lại từ khóa để TV4 tích hợp vào search/filter panel.
- Tích hợp được `ThongKeView` của TV5 mà không sửa code TV5. TV5 đang dùng `pack()`, nên TV1 tạo một frame mount riêng; `MainWindow` vẫn dùng `grid()` ở lớp ngoài, không trộn hai geometry manager trong cùng parent.

## 3. Kết quả thu được

- Kiến trúc giao diện rõ ràng hơn:

```text
MainWindow
|-- Header + global search
|-- Navigation
`-- content_container
    |-- HomeView
    |-- HangHoaView (chờ TV3/TV4)
    `-- ThongKeView (TV5)
```

- HOME đã có visual hierarchy gần ảnh tham khảo nhưng vẫn là desktop app Tkinter, không biến project thành website.
- Ảnh sản phẩm được đọc từ tài nguyên có sẵn thay vì emoji hoặc hình gear vẽ giả bằng Canvas.
- Không có SQL trong UI và không tạo thêm cửa sổ `Tk()` khi đổi màn hình.

## 4. File đã tạo hoặc sửa

| File | Trạng thái | Nội dung |
|---|---|---|
| `views/home_view.py` | Tạo mới | Toàn bộ giao diện HOME, scroll, category strip và image loader Pillow. |
| `views/main_window.py` | Sửa | Root window, header, navigation, global search và adapter tích hợp view. |
| `requirements.txt` | Sửa | Thêm dependency Pillow. |
| `reports/TV1_baocao.md` | Sửa | Báo cáo tiến độ và cách kiểm tra của TV1. |

## 5. File cố tình không sửa

- TV2: `config/database.py`, `sql/database.sql`, `sql/gearvn_snapshot.sql`.
- TV3: `models/hang_hoa.py`, `repositories/hang_hoa_repository.py`, `services/hang_hoa_service.py`, `views/hang_hoa_view.py`.
- TV4: `utils/validators.py` và phần search/filter.
- TV5: `views/thong_ke_view.py`.

## 6. Những việc TV1 chưa thể hoàn tất và dependency

### Chờ TV2

- `HinhAnh` đã có trong database và dữ liệu mẫu. TV2 cần xác nhận đường dẫn lưu trong database luôn dùng được từ thư mục gốc project.
- Schema hiện chưa thấy `ThuongHieu`. Nếu nhóm cần filter theo hãng và hiển thị thương hiệu ở product preview, TV2 cần bổ sung field hoặc cung cấp mapping rõ ràng.

### Chờ TV3

- Cần bàn giao `class HangHoaView(ttk.Frame)` nhận `parent` để MainWindow mount trực tiếp.
- Cần `HangHoaService` có API lấy danh sách sản phẩm để HOME nạp product preview từ SQL Server; hiện HOME chỉ hiển thị trạng thái chờ dữ liệu, không hard-code danh sách giả.
- Model/Service cần trả `HinhAnh` hoặc `AnhChinh` để product card dùng ảnh do dữ liệu quyết định.

### Chờ TV4

- Cần thống nhất API nhận context từ global search và category, ví dụ `set_search_keyword(keyword)` và `set_category_filter(category)` trong `HangHoaView` hoặc `SearchFilterPanel`.
- Cần hoàn thiện search/filter theo hãng, giá, trạng thái và tồn kho. TV1 chỉ giữ và chuyển context, không tự viết SQL hoặc business logic.

### Chờ TV5

- Không còn dependency UI bắt buộc: `ThongKeView` đã mount được từ MainWindow.
- Chưa test dữ liệu thống kê thật vì cần SQL Server của TV2 chạy và có dữ liệu đầy đủ.

### Việc cuối của TV1 sau khi các bạn merge

- Kiểm thử end-to-end: HOME -> Danh mục -> CRUD -> tìm kiếm/lọc -> Thống kê -> HOME.
- Kiểm tra lỗi kết nối SQL Server, dữ liệu ảnh thiếu, resize 1280x720 và 1440x900.
- Chuẩn bị luồng demo trên lớp và kiểm tra bản merge cuối cùng.

## 7. Cách chạy thử

Tại thư mục gốc project, chạy:

```powershell
pip install -r requirements.txt
python main.py
```

Kết quả mong đợi:

1. Cửa sổ `HCMUTE_ChanBoMayDe - Quản lý gear công nghệ` mở ra.
2. Trang HOME hiện header, ô tìm kiếm rộng, navigation, hero, hai banner phụ, sáu danh mục và hàng thông tin.
3. Click `DANH MỤC HÀNG HÓA` hoặc category sẽ chuyển tới HangHoaView khi TV3/TV4 đã merge; trước lúc đó sẽ hiện màn thông báo tích hợp.
4. Click `THỐNG KÊ TỔNG SỐ LƯỢNG` sẽ mở ThongKeView của TV5. Để có số liệu thật cần chạy SQL Server theo tài liệu TV2.
5. Nhập từ khóa tại header rồi bấm Enter hoặc `TÌM`; từ khóa được lưu để TV4 xử lý tại màn danh mục.

## 8. Kiểm thử đã thực hiện

- `python -m py_compile main.py views/main_window.py views/home_view.py utils/helpers.py views/thong_ke_view.py`: thành công.
- Khởi tạo `MainWindow`, render `HomeView` và destroy root: thành công.
- Chạy event loop thật, sau đó resize cửa sổ từ 1280x720 sang 1440x900: HOME không phát sinh lỗi layout và Canvas nội dung phản hồi theo kích thước cửa sổ.
- Kiểm tra HomeView đang giữ 9 `PhotoImage` cho hero, promo và category; ảnh không bị biến mất do garbage collection.
- Kiểm tra thư mục ảnh: tìm thấy 60 ảnh JPG; kích thước mẫu là 800 x 536.
- Test chuyển `ThongKeView` với repository giả lập: thành công; view được quản lý bằng `pack()` trong mount riêng, sau đó quay HOME thành công.
- Test truyền context `category='Micro'`, `keyword='Logitech'` và global search `Razer`: MainWindow giữ đúng dữ liệu chờ TV3/TV4.
- `git diff --check`: không báo lỗi whitespace.

## 9. Chưa thể test

- Chưa test CRUD, search/filter thật và product preview lấy từ Service vì `HangHoaView`/`HangHoaService` của TV3/TV4 chưa có API bàn giao phù hợp.
- Chưa test thống kê với SQL Server thật vì phụ thuộc môi trường database và dữ liệu của TV2.
- Chưa thể chạy full demo khi các module còn lại chưa merge hoàn chỉnh.
