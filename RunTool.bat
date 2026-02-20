@echo off
title HLS/TS Pro Downloader
color 0b

:: Kiểm tra xem Python đã được cài đặt chưa
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Loi: Khong tim thay Python. Vui long cai dat Python truoc!
    pause
    exit
)

:: Kiểm tra xem file script co ton tai khong
if not exist "hls_tool.py" (
    echo [!] Loi: Khong tim thay file hls_tool.py trong thu muc nay.
    echo Hay dam bao file .bat va file .py nam cung mot cho.
    pause
    exit
)

:: Chạy script
echo [*] Dang khoi dong cong cu...
python hls_tool.py

pause
