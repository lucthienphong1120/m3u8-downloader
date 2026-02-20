import requests
import re
import os
import subprocess
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
            print("[!] Lỗi: Không tìm thấy FFmpeg trong hệ thống."); return False

    def get_urls_from_m3u8(self, source):
        try:
            if source.startswith('http'):
                content = requests.get(source, headers=self.headers, timeout=15).text
            else:
                with open(source, 'r', encoding='utf-8') as f:
                    content = f.read()
            urls = re.findall(r'https?://[^\s<>"]+|(?<=^)[^\s#]+', content, re.M)
            return [u.strip() for u in urls if u.strip()]
        except Exception as e:
            print(f"[!] Lỗi đọc file/link: {e}"); return []

    def download_segment(self, url):
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            return res.content if res.status_code == 200 else None
        except: return None

    def process_conversion(self, input_file, output_file):
        print(f"[*] Đang chuyển đổi {input_file} -> {output_file}...")
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
            print("="*45)
            print("      HLS/TS TOOL - PHIÊN BẢN ENTER NHANH")
            print("="*45)
            print("1. Tải từ Link M3U8 (URL)")
            print("2. Tải từ File M3U8 (Mặc định: tt.m3u8)")
            print("3. Convert File .ts (Mặc định: video.ts)")
            print("4. Thoát")
            choice = input("\nChọn (1-4): ")

            if choice == '4': break

            # Thiết lập tên file đầu ra mặc định
            out_input = input("Tên file lưu (Mặc định: video.mp4): ").strip()
            output_name = out_input if out_input else "video.mp4"
            if not output_name.endswith('.mp4'): output_name += '.mp4'

            if choice == '1':
                source = input("Nhập URL M3U8: ").strip('"')
                if not source: print("[!] Link không được để trống."); input(); continue
                self.handle_download(source, output_name)

            elif choice == '2':
                src_input = input("Đường dẫn file M3U8 (Mặc định: tt.m3u8): ").strip('"')
                source = src_input if src_input else "tt.m3u8"
                if os.path.exists(source):
                    self.handle_download(source, output_name)
                else:
                    print(f"[!] Không tìm thấy file {source}"); input()

            elif choice == '3':
                ts_input = input("Đường dẫn file .ts (Mặc định: video.ts): ").strip('"')
                ts_file = ts_input if ts_input else "video.ts"
                if os.path.exists(ts_file):
                    self.process_conversion(ts_file, output_name)
                    print(f"\n[!] XONG: {output_name}")
                else:
                    print(f"[!] Không tìm thấy file {ts_file}"); input()

            input("\nNhấn Enter để quay lại menu...")

    def handle_download(self, source, output_name):
        urls = self.get_urls_from_m3u8(source)
        if not urls: return
        
        print(f"[*] Tải {len(urls)} đoạn bằng 15 luồng...")
        with open(self.temp_ts, 'wb') as f:
            with ThreadPoolExecutor(max_workers=15) as executor:
                results = list(executor.map(self.download_segment, urls))
                for i, data in enumerate(results):
                    if data:
                        f.write(data)
                        print(f" -> Tiến độ: {i+1}/{len(urls)}", end='\r')
        
        print("\n[*] Tải hoàn tất. Đang đóng gói MP4...")
        self.process_conversion(self.temp_ts, output_name)
        if os.path.exists(self.temp_ts): os.remove(self.temp_ts)
        print(f"\n[!] HOÀN THÀNH: {output_name}")

if __name__ == "__main__":
    VideoDownloader().run()
