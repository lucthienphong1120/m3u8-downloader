# 🎬 HLS/TS Pro Downloader & Converter

Một công cụ dòng lệnh (CLI) mạnh mẽ được viết bằng Python, giúp tải xuống các luồng HLS (.m3u8) và chuyển đổi các phân đoạn video (.ts) sang định dạng MP4. 

Công cụ này được thiết kế đặc biệt để "phá đảo" các kỹ thuật **Content-Type Spoofing** (ngụy trang video dưới dạng file ảnh PNG/JPG) thường thấy trên các hệ thống CDN của TikTok hoặc các trang web phim.

## ✨ Tính năng nổi bật

+ **Vượt rào Bảo mật:** Tự động xử lý lỗi `Invalid PNG signature` bằng cách ép định dạng luồng dữ liệu (MPEG-TS).
+ **Tải Đa luồng (Multithreading):** Sử dụng 15 luồng tải song song, tối ưu hóa băng thông và tiết kiệm thời gian.
+ **Tiến độ tải chi tiết:** Hiển thị số lượng phân đoạn đã tải và % hoàn thành theo thời gian thực (Real-time).
+ **Tự động Đánh số (Auto-increment):** Tự động kiểm tra file trùng tên và thêm hậu tố `_1`, `_2`,... (Ví dụ: `video.mp4` -> `video_1.mp4`).
+ **Tiến độ đóng gói (%)** Tích hợp logic đọc thời lượng video từ FFmpeg để hiển thị chính xác phần trăm quá trình chuyển đổi.
+ **Luồng làm việc liên tục:** Sau khi hoàn thành một tác vụ, bạn có thể tiếp tục dán link tiếp theo ngay lập tức mà không cần quay lại menu chính. Nhấn Enter trống để thoát về menu.

## 🛠 Yêu cầu hệ thống

1. **Python 3.x**
2. **Thư viện Requests**: Cài đặt bằng lệnh `pip install requests`
3. **FFmpeg**: Bắt buộc phải có để đóng gói và chuyển đổi video.

## 📦 Hướng dẫn cài đặt FFmpeg trên Windows

Nếu script báo lỗi `Không tìm thấy FFmpeg`, hãy thực hiện các bước sau:

1. **Tải xuống:** Truy cập [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) và tải file `ffmpeg-git-full.7z` (mục release builds).
2. **Giải nén:** Giải nén file vừa tải vào thư mục dễ nhớ, ví dụ: `C:\ffmpeg`.
3. **Thêm vào Path:**
   + Nhấn phím `Windows`, gõ "env" và chọn **Edit the system environment variables**.
   + Click vào nút **Environment Variables**.
   + Tại mục **System variables**, tìm dòng `Path`, chọn nó và nhấn **Edit**.
   + Nhấn **New** và dán đường dẫn đến thư mục `bin` của FFmpeg (Ví dụ: `C:\ffmpeg\bin`).
   + Nhấn **OK** để lưu lại.
4. Kiểm tra: Mở CMD mới và gõ `ffmpeg -version`. Nếu hiện thông tin phiên bản là thành công.

## 🚀 Hướng dẫn sử dụng Script

1. Mở Terminal/CMD tại thư mục chứa file `hls_tool.py`.
2. Chạy lệnh: `python hls_tool.py`

Các tùy chọn trong Menu:
+ **Option 1 (Link URL)**: Dán link .m3u8 trực tiếp để tải từ internet.
+ **Option 2 (File nội bộ)**: Xử lý file .m3u8 có sẵn trong máy (Mặc định sẽ tìm file tt.m3u8).
+ **Option 3 (Convert TS)**: Chuyển đổi trực tiếp các file .ts thô sang .mp4 (Mặc định tìm file video.ts).

## 🔬 Giải pháp kỹ thuật

Dữ liệu từ server thường trả về nhãn `image/png` để đánh lừa các công cụ tải xuống thông thường. Tuy nhiên, bản chất của chúng là các gói tin **MPEG-TS** bắt đầu bằng byte đồng bộ `0x47`.

Hệ thống xử lý dựa trên cơ chế:
1.  **Binary Fetching:** Tải dữ liệu nhị phân thô, bỏ qua mọi nhãn định dạng giả mạo (như image/png).
2.  **Concatenation:** Ghép nối các phân đoạn nhị phân thành một luồng MPEG-TS duy nhất.
3.  **Forced Decoding:** Sử dụng tham số `-f mpegts` trong FFmpeg để ép bộ giải mã video vào làm việc, loại bỏ hoàn toàn các header giả mạo của file ảnh.

## ⚖️ Miễn trừ trách nhiệm

Công cụ này được phát triển cho mục đích học tập và nghiên cứu kỹ thuật. Người dùng hoàn toàn chịu trách nhiệm về tính pháp lý và bản quyền của nội dung được tải xuống.
