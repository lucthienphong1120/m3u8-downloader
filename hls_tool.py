import requests
import re
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    def get_unique_filename(self, filename):
        name, ext = os.path.splitext(filename)
        if not os.path.exists(filename): return filename
        
        counter = 1
        while True:
            new_name = f"{name}_{counter}{ext}"
            if not os.path.exists(new_name):
                return new_name
            counter += 1

    def get_urls_from_m3u8(self, source):
        try:
            if source.startswith('http'):
                res = requests.get(source, headers=self.headers, timeout=15)
                res.raise_for_status()
                content = res.text
                base_url = source.rsplit('/', 1)[0]
            else:
                with open(source, 'r', encoding='utf-8') as f:
                    content = f.read()
                base_url = ""

            lines = content.splitlines()
            urls = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('http'):
                        urls.append(line)
                    else:
                        urls.append(f"{base_url}/{line}" if base_url else line)
            return urls
        except Exception as e:
            print(f"[!] Lỗi đọc nguồn: {e}"); return []

    def download_segment(self, url, index):
        try:
            res = requests.get(url, headers=self.headers, timeout=15)
            if res.status_code == 200:
                return index, res.content
            return index, None
        except: return index, None

    def get_duration_seconds(self, ts_file):
        """Lấy tổng thời lượng của file TS để tính % FFmpeg"""
        try:
            cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', ts_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return float(result.stdout.strip())
        except: return None

    def process_conversion(self, input_file, output_file):
        total_duration = self.get_duration_seconds(input_file)
        print(f"[*] Đang đóng gói: {output_file}...")
        
        cmd = [
            'ffmpeg', '-y', '-f', 'mpegts', '-i', input_file,
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '128k',
            '-movflags', '+faststart', output_file
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')
        
        pattern = re.compile(r"time=(\d+):(\d+):(\d+.\d+)")
        
        while True:
            line = process.stdout.readline()
            if not line: break
            
            if total_duration:
                match = pattern.search(line)
                if match:
                    h, m, s = map(float, match.groups())
                    current_time = h * 3600 + m * 60 + s
                    percent = min(100, (current_time / total_duration) * 100)
                    print(f" -> Đang xử lý: {percent:.1f}%", end='\r')
        
        process.wait()
        print(f" -> Đang xử lý: 100.0%  (Xong!)")

    def ask_output_name(self, default_name="video.mp4"):
        out_input = input(f"Tên file lưu (Để trống tự động: {default_name}): ").strip()
        final_name = out_input if out_input else default_name
        if not final_name.lower().endswith('.mp4'): final_name += '.mp4'
        return self.get_unique_filename(final_name)

    def run(self):
        if not self.check_ffmpeg(): return

        while True:
            self.clear_screen()
            print("="*45)
            print("   HLS/TS TOOL - BẢN CẬP NHẬT PRO UX")
            print("="*45)
            print("1. Tải từ Link M3U8 (URL)")
            print("2. Tải từ File M3U8 (Nội bộ)")
            print("3. Convert File .ts sang .mp4")
            print("4. Thoát")
            choice = input("\nChọn (1-4): ")

            if choice == '4': break
            
            if choice == '1':
                while True:
                    url = input("\nNhập URL M3U8 (Nhấn Enter để quay lại menu): ").strip('" ')
                    if not url: break
                    output_name = self.ask_output_name()
                    self.handle_download(url, output_name)
                    print(f"\n[!] THÀNH CÔNG: {output_name}")

            elif choice == '2':
                while True:
                    path = input("\nĐường dẫn file M3U8 (Nhấn Enter để quay lại menu): ").strip('" ')
                    if not path: break
                    if os.path.exists(path):
                        output_name = self.ask_output_name()
                        self.handle_download(path, output_name)
                        print(f"\n[!] THÀNH CÔNG: {output_name}")
                    else: print(f"[!] Không thấy file {path}")

            elif choice == '3':
                while True:
                    ts_path = input("\nĐường dẫn file .ts (Nhấn Enter để quay lại menu): ").strip('" ')
                    if not ts_path: break
                    if os.path.exists(ts_path):
                        output_name = self.ask_output_name()
                        self.process_conversion(ts_path, output_name)
                        print(f"\n[!] THÀNH CÔNG: {output_name}")
                    else: print(f"[!] Không thấy file {ts_path}")

    def handle_download(self, source, output_name):
        urls = self.get_urls_from_m3u8(source)
        if not urls: 
            print("[!] Không tìm thấy link video nào trong nguồn."); return
        
        total = len(urls)
        print(f"[*] Tìm thấy {total} đoạn. Đang tải...")
        
        segments = {}
        completed = 0
        
        with ThreadPoolExecutor(max_workers=15) as executor:
            future_to_url = {executor.submit(self.download_segment, url, i): i for i, url in enumerate(urls)}
            
            for future in as_completed(future_to_url):
                index, data = future.result()
                if data:
                    segments[index] = data
                completed += 1
                print(f" -> Tiến độ tải: {completed}/{total} đoạn ({int(completed/total*100)}%)", end='\r')
        
        print(f"\n[*] Đang ghép các đoạn thành file tạm...")
        with open(self.temp_ts, 'wb') as f:
            for i in range(total):
                if i in segments:
                    f.write(segments[i])
        
        self.process_conversion(self.temp_ts, output_name)
        if os.path.exists(self.temp_ts): os.remove(self.temp_ts)

if __name__ == "__main__":
    try:
        VideoDownloader().run()
    except KeyboardInterrupt:
        print("\n[!] Đã dừng chương trình.")
        sys.exit()
