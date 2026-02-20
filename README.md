# 🎬 HLS/TS Pro Downloader & Converter

Một công cụ dòng lệnh (CLI) mạnh mẽ được viết bằng Python, giúp tải xuống các luồng HLS (.m3u8) và chuyển đổi các phân đoạn video (.ts) sang định dạng MP4. 

Công cụ này được thiết kế đặc biệt để "phá đảo" các kỹ thuật **Content-Type Spoofing** (ngụy trang video dưới dạng file ảnh PNG/JPG) thường thấy trên các hệ thống CDN của TikTok hoặc các trang web phim.

## ✨ Tính năng nổi bật

* **Vượt rào Bảo mật:** Tự động xử lý lỗi `Invalid PNG signature` bằng cách ép định dạng luồng dữ liệu (MPEG-TS).
* **Tải Đa luồng (Multithreading):** Sử dụng 15 luồng tải song song, tối ưu hóa băng thông và tiết kiệm thời gian.
* **Tự động Đánh số (Auto-increment):** Kiểm tra file trùng tên và tự động thêm hậu tố `(1)`, `(2)`,... để bảo vệ dữ liệu cũ.
* **Giao diện Tối giản (Refined UX):** Menu điều khiển thông minh, sử dụng các gợi ý (VD) và hỗ trợ giá trị mặc định chỉ với phím **Enter**.
* **Xử lý Hậu kỳ Chuyên nghiệp:** Tích hợp FFmpeg để đảm bảo file đầu ra đạt chuẩn H.264/AAC, tương thích 100% với điện thoại và máy tính.

## 🛠 Yêu cầu hệ thống

1.  **Python 3.x**
2.  **FFmpeg:** Đã được cài đặt và thêm vào biến môi trường (PATH).
3.  **Thư viện Requests:**

```bash
pip install requests
```

## 🚀 Hướng dẫn sử dụng

1.  Mở Terminal/CMD tại thư mục chứa script.
2.  Chạy công cụ:

```bash
python hls_tool.py
```

Các tùy chọn trong Menu:
+ **Option 1**: Dán link .m3u8 trực tiếp để tải từ internet.
+ **Option 2**: Xử lý file .m3u8 có sẵn trong máy (Mặc định sẽ tìm file tt.m3u8).
+ **Option 3**: Chuyển đổi trực tiếp các file .ts thô sang .mp4 (Mặc định tìm file video.ts).

## 🔬 Giải pháp kỹ thuật

Dữ liệu từ server thường trả về nhãn `image/png` để đánh lừa các công cụ tải xuống thông thường. Tuy nhiên, bản chất của chúng là các gói tin **MPEG-TS** bắt đầu bằng byte đồng bộ `0x47`.

Script này hoạt động theo 3 bước:
1.  **Binary Fetching:** Tải dữ liệu nhị phân thô, bỏ qua mọi cảnh báo định dạng từ trình duyệt/hệ thống.
2.  **Concatenation:** Ghép nối các phân đoạn thành một luồng dữ liệu liên tục.
3.  **Forced Decoding:** Sử dụng tham số `-f mpegts` trong FFmpeg để ép bộ giải mã video vào làm việc, loại bỏ hoàn toàn các lớp "mặt nạ" ảnh giả mạo.

## 📝 Cơ chế hoạt động (Technical Note)

Công cụ này giải quyết lỗi `Invalid PNG signature` bằng cách:
1.  Sử dụng Python để tải dữ liệu nhị phân thô của các phân đoạn, bất kể Content-Type mà server trả về.
2.  Ghép các mảnh dữ liệu thành một khối luồng vận chuyển (MPEG-TS) duy nhất.
3.  Gọi FFmpeg với tham số `-f mpegts` để ép hệ thống giải mã theo cấu trúc gói tin video, loại bỏ hoàn toàn các header giả mạo của file ảnh.

## ⚖️ Miễn trừ trách nhiệm

Công cụ này được phát triển cho mục đích học tập và nghiên cứu kỹ thuật. Người dùng hoàn toàn chịu trách nhiệm về tính pháp lý và bản quyền của nội dung được tải xuống.

**Coded with ❤️ by Gemini & ltp1120**
