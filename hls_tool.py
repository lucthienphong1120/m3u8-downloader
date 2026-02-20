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
            print("[!] Lỗi: Không tìm thấy FFmpeg."); return False

    def get_unique_filename(self, filename):
        if not os.path.exists(filename): return filename
        name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(f"{name}({counter}){ext}"):
            counter += 1
        return f"{name}({counter}){ext}"

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
            print(f"[!] Lỗi đọc nguồn: {e}"); return []

    def download_segment(self, url):
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            return res.content if res.status_code == 200 else None
        except: return None

    def process_conversion(self, input_file, output_file):
        print(f"[*] Đang đóng gói: {output_file}...")
        cmd = [
            'ffmpeg', '-y', '-f', 'mpegts', '-i', input_file,
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '128k',
            '-movflags', '+faststart', output_file
        ]
        subprocess.run(cmd, capture_output=True)

    def ask_output_name(self):
        out_input = input("Tên file lưu (VD: video.mp4): ").strip()
        base_name = out_input if out_input else "video.mp4"
        if not base_name.endswith('.mp4'): base_name += '.mp4'
        return self.get_unique_filename(base_name)

    def run(self):
        if not self.check_ffmpeg(): return

        while True:
            self.clear_screen()
            print("="*45)
            print("   HLS/TS TOOL - BẢN CẬP NHẬT UX")
            print("="*45)
            print("1. Tải từ Link M3U8 (URL)")
            print("2. Tải từ File M3U8 (VD: tt.m3u8)")
            print("3. Convert File .ts (VD: video.ts)")
            print("4. Thoát")
            choice = input("\nChọn (1-4): ")

            if choice == '4': break

            if choice == '1':
                source = input("Nhập URL M3U8: ").strip('"')
                if not source: continue
                output_name = self.ask_output_name()
                self.handle_download(source, output_name)

            elif choice == '2':
                src_input = input("Đường dẫn file M3U8 (VD: tt.m3u8): ").strip('"')
                source = src_input if src_input else "tt.m3u8"
                if os.path.exists(source):
                    output_name = self.ask_output_name()
                    self.handle_download(source, output_name)
                else: print(f"[!] Không thấy file {source}"); input()

            elif choice == '3':
                ts_input = input("Đường dẫn file .ts (VD: video.ts): ").strip('"')
                source = ts_input if ts_input else "video.ts"
                if os.path.exists(source):
                    output_name = self.ask_output_name()
                    self.process_conversion(source, output_name)
                    print(f"\n[!] THÀNH CÔNG: {output_name}")
                else: print(f"[!] Không thấy file {source}"); input()

            input("\nNhấn Enter để tiếp tục...")

    def handle_download(self, source, output_name):
        urls = self.get_urls_from_m3u8(source)
        if not urls: return
        
        print(f"[*] Tìm thấy {len(urls)} đoạn. Đang tải...")
        with open(self.temp_ts, 'wb') as f:
            with ThreadPoolExecutor(max_workers=15) as executor:
                results = list(executor.map(self.download_segment, urls))
                for i, data in enumerate(results):
                    if data:
                        f.write(data)
                        print(f" -> Tiến độ: {i+1}/{len(urls)}", end='\r')
        
        self.process_conversion(self.temp_ts, output_name)
        if os.path.exists(self.temp_ts): os.remove(self.temp_ts)
        print(f"\n[!] THÀNH CÔNG: {output_name}")

if __name__ == "__main__":
    VideoDownloader().run()
