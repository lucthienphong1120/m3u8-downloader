## cài đặt FFmpeg trên Windows

### Cách 1: Cài nhanh bằng lệnh (Khuyên dùng cho Win 10/11)

Windows hiện nay có sẵn trình quản lý gói gọi là winget. Bạn không cần tải web gì cả, chỉ cần gõ lệnh:

Nhấn phím Windows, gõ cmd và chọn Run as Administrator.

Dán lệnh sau vào và nhấn Enter:

```
winget install ffmpeg
```

Đợi nó chạy xong. Sau đó tắt cửa sổ CMD đó đi và mở lại một cái mới.

Gõ `ffmpeg -version` để kiểm tra. Nếu hiện ra thông tin phiên bản là thành công!

### Cách 2: Cài thủ công (Nếu cách trên không chạy)

Nếu bạn muốn tự tay thiết lập, hãy làm theo các bước sau:

Bước 1: Tải file

Truy cập trang: gyan.dev/ffmpeg/builds

Kéo xuống phần release builds, tải file có tên: `ffmpeg-release-essentials.zip`

Bước 2: Giải nén và đặt tên

Giải nén file vừa tải về.

Đổi tên thư mục vừa giải nén thành ngắn gọn là ffmpeg.

Copy thư mục này vào ổ **C:**. (Đường dẫn bây giờ sẽ là C:\ffmpeg).

Bước 3: Thiết lập biến môi trường (Environment Variables)

Để bạn có thể gõ chữ ffmpeg ở bất cứ đâu mà máy tính vẫn hiểu, bạn cần làm bước này:

Nhấn phím Windows, gõ: env -> Chọn Edit the system environment variables.

Trong bảng hiện ra, nhấn nút Environment Variables... (ở dưới cùng).

Ở ô System variables (phía dưới), tìm dòng có tên là Path, nhấn đúp vào đó (hoặc chọn rồi nhấn Edit).

Nhấn nút New và dán đường dẫn này vào: C:\ffmpeg\bin

Nhấn OK cho tất cả các bảng.

Bước cuối: Kiểm tra xem đã "ngon" chưa?

Mở Command Prompt (CMD) mới và gõ:

```
ffmpeg -version
```

## Chuẩn bị Python

Bạn cần cài thư viện requests để tải file:

```
pip install requests
```
