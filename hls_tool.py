import requests
import re
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

class TikTokVideoDownloader:
    def __init__(self, m3u8_input, output_name="final_video.mp4"):
        self.m3u8_input = m3u8_input
        self.output_name = output_name
        self.temp_ts = "raw_segments.ts"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.tiktok.com/'
        }

    def get_urls(self):
        # Nếu input là URL
        if self.m3u8_input.startswith('http'):
            content = requests.get(self.m3u8_input, headers=self.headers).text
        else: # Nếu là file cục bộ
            with open(self.m3u8_input, 'r') as f:
                content = f.read()
        
        # Tìm tất cả các link https trong file
        return re.findall(r'https?://[^\s<>"]+|(?<=^)[^\s#]+', content, re.M)

    def download_segment(self, url):
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            return res.content if res.status_code == 200 else None
        except:
            return None

    def run(self):
        urls = self.get_urls()
        print(f"[*] Tìm thấy {len(urls)} đoạn video 'ẩn'. Đang tải...")

        # Tải đa luồng để tăng tốc (10 luồng cùng lúc)
        with open(self.temp_ts, 'wb') as f:
            with ThreadPoolExecutor(max_workers=10) as executor:
                results = list(executor.map(self.download_segment, urls))
                for data in results:
                    if data:
                        f.write(data)

        print("[*] Tải xong dữ liệu thô. Đang ép FFmpeg chuyển đổi định dạng...")
        
        # Lệnh then chốt: -f mpegts để phá vỡ lớp mặt nạ PNG
        cmd = [
            'ffmpeg', '-y', '-f', 'mpegts', '-i', self.temp_ts,
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart', self.output_name
        ]
        
        subprocess.run(cmd)
        os.remove(self.temp_ts)
        print(f"[!] HOÀN THÀNH: {self.output_name}")

if __name__ == "__main__":
    # Thay 'tt.m3u8' bằng đường dẫn file của bạn
    downloader = TikTokVideoDownloader('tt.m3u8', 'tiktok_unhidden.mp4')
    downloader.run()
