import requests
import re
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

class VideoDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.tiktok.com/'
        }
        self.temp_ts = "temp_combined_raw.ts"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_ffmpeg(self):
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except:
            print("[!] Lỗi: Không tìm thấy FFmpeg. Vui lòng cài đặt FFmpeg trước.")
            return False

    def get_urls_from_m3u8(self, source):
        try:
            if source.startswith('http'):
                content = requests.get(source, headers=self.headers, timeout=15).text
            else:
                with open(source, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # Regex lấy tất cả các link (tuyệt đối hoặc tương đối)
            urls = re.findall(r'https?://[^\s<>"]+|(?<=^)[^\s#]+', content, re.M)
            return [u.strip() for u in urls if u.strip()]
        except Exception as e:
            print(f"[!] Lỗi khi đọc M3U8: {e}")
            return []

    def download_segment(self, url):
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            return res.content if res.status_code == 200 else None
        except:
            return None

    def process_conversion(self, input_file, output_file):
        print(f"[*] Đang ép FFmpeg xử lý luồng dữ liệu thô...")
        # Sử dụng -f mpegts để phá lớp mặt nạ PNG giả mạo
        cmd = [
            'ffmpeg', '-y', '-f', 'mpegts', '-i', input_file,
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '128k',
            '-movflags', '+faststart', output_file
        ]
        subprocess.run(cmd)

    def run(self):
        if not self.check_ffmpeg(): return

        while True:
            self.clear_screen()
            print("="*40)
            print("   HLS/TS VIDEO DOWNLOADER - FINAL")
            print("="*40)
            print("1. Tải từ Link M3U8 (URL)")
            print("2. Tải từ File M3U8 cục bộ")
            print("3. Chuyển đổi File .ts có sẵn sang .mp4")
            print("4. Thoát")
            choice = input("\nChọn tùy chọn (1-4): ")

            if choice == '4': break

            output_name = input("Nhập tên file đầu ra (VD: video.mp4): ") or "output.mp4"
            if not output_name.endswith('.mp4'): output_name += '.mp4'

            if choice in ['1', '2']:
                source = input("Nhập Link URL hoặc Đường dẫn file M3U8: ").strip('"')
                urls = self.get_urls_from_m3u8(source)
                
                if not urls:
                    print("[!] Không tìm thấy phân đoạn video nào."); input(); continue

                print(f"[*] Tìm thấy {len(urls)} đoạn. Đang tải đa luồng...")
                
                with open(self.temp_ts, 'wb') as f:
                    with ThreadPoolExecutor(max_workers=15) as executor:
                        results = list(executor.map(self.download_segment, urls))
                        for i, data in enumerate(results):
                            if data:
                                f.write(data)
                                print(f" -> Đã ghép đoạn {i+1}/{len(urls)}", end='\r')
                
                print("\n[*] Tải xong. Bắt đầu convert...")
                self.process_conversion(self.temp_ts, output_name)
                if os.path.exists(self.temp_ts): os.remove(self.temp_ts)

            elif choice == '3':
                ts_file = input("Nhập đường dẫn file .ts: ").strip('"')
                if os.path.exists(ts_file):
                    self.process_conversion(ts_file, output_name)
                else:
                    print("[!] File không tồn tại.")

            print(f"\n[!] HOÀN THÀNH: {output_name}")
            input("\nNhấn Enter để quay lại menu...")

if __name__ == "__main__":
    tool = VideoDownloader()
    tool.run()
