import requests
import os
import subprocess

def download_and_convert(m3u8_file, output_name):
    print("--- Bắt đầu quét file m3u8 ---")
    
    # 1. Đọc file m3u8 để lấy danh sách link
    with open(m3u8_file, 'r') as f:
        lines = f.readlines()
    
    urls = [line.strip() for line in lines if line.startswith('http')]
    total = len(urls)
    print(f"Tìm thấy {total} đoạn video.")

    # 2. Tải và ghép nối nhị phân (Binary Concat)
    # Chúng ta tải về và lưu vào một file .ts tạm thời
    temp_ts = "temp_combined.ts"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    with open(temp_ts, 'wb') as merged_file:
        for i, url in enumerate(urls):
            print(f" Đang tải đoạn {i+1}/{total}...", end='\r')
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                merged_file.write(res.content)
            else:
                print(f"\n Lỗi đoạn {i+1}: Code {res.status_code}")

    print("\n--- Đã tải xong! Đang dùng FFmpeg để chuyển sang MP4 ---")

    # 3. Dùng FFmpeg để sửa header "PNG giả" và nén lại thành MP4 xịn
    # Lệnh này ép FFmpeg quét toàn bộ dữ liệu để tìm luồng video H.264
    cmd = [
        'ffmpeg', '-y', 
        '-f', 'mpegts',           # ÉP FFmpeg coi đầu vào là chuẩn video TS
        '-i', temp_ts, 
        '-c:v', 'libx264', 
        '-pix_fmt', 'yuv420p', 
        output_name
    ]
    
    subprocess.run(cmd)
    
    # Dọn dẹp file tạm
    if os.path.exists(temp_ts):
        os.remove(temp_ts)
    
    print(f"--- THÀNH CÔNG! File của bạn: {output_name} ---")

if __name__ == "__main__":
    download_and_convert('tt.m3u8', 'video_hoan_thien.mp4')
