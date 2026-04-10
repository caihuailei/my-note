#!/bin/bash
# 安装 Video Downloader Skill 依赖

echo "Installing Video Downloader Skill dependencies..."

# 检查 Python
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed"
    exit 1
fi

# 安装 Python 依赖
echo "Installing Python packages..."
pip install playwright

# 安装浏览器
echo "Installing Chromium browser..."
python -m playwright install chromium

# 可选安装 yt-dlp
echo "Installing yt-dlp (optional but recommended)..."
pip install yt-dlp

echo "Installation complete!"
echo ""
echo "You can now use the video-downloader skill."
