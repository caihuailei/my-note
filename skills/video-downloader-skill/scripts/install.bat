@echo off
REM 安装 Video Downloader Skill 依赖（Windows）

echo Installing Video Downloader Skill dependencies...

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    exit /b 1
)

REM 安装 Python 依赖
echo Installing Python packages...
pip install playwright

REM 安装浏览器
echo Installing Chromium browser...
python -m playwright install chromium

REM 可选安装 yt-dlp
echo Installing yt-dlp (optional but recommended)...
pip install yt-dlp

echo Installation complete!
echo.
echo You can now use the video-downloader skill.
pause
