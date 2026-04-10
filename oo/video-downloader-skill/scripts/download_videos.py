#!/usr/bin/env python3
"""
批量下载视频
从 video_links.txt 读取链接并下载
"""

import subprocess
import os
import shutil


def parse_video_links(filename):
    """解析视频链接文件"""
    videos = {}

    with open(filename, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    # 每两行一组：名称 + URL
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            name = lines[i]
            url = lines[i + 1]
            videos[name] = url

    return videos


def download_with_ytdlp(name, url, output_dir):
    """使用 yt-dlp 下载"""
    filename = f"{name}.mp4"
    filepath = os.path.join(output_dir, filename)

    cmd = [
        'yt-dlp',
        '-o', filepath,
        '--no-check-certificate',
        '--progress',
        url
    ]

    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def download_with_curl(name, url, output_dir):
    """使用 curl 下载"""
    filename = f"{name}.mp4"
    filepath = os.path.join(output_dir, filename)

    cmd = [
        'curl',
        '-L',
        '-o', filepath,
        '--progress-bar',
        url
    ]

    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def check_tools():
    """检查可用的下载工具"""
    if shutil.which("yt-dlp"):
        return "yt-dlp"
    elif shutil.which("curl"):
        return "curl"
    else:
        return None


def main():
    # 配置
    LINKS_FILE = 'video_links.txt'
    OUTPUT_DIR = 'downloads'

    # 检查文件
    if not os.path.exists(LINKS_FILE):
        print(f"错误: 找不到 {LINKS_FILE}")
        print("请先运行 get_video_links.py 获取视频链接")
        return

    # 创建目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 解析链接
    videos = parse_video_links(LINKS_FILE)
    print(f"找到 {len(videos)} 个视频")

    # 检查工具
    tool = check_tools()
    if not tool:
        print("错误: 未找到 yt-dlp 或 curl")
        print("请安装 yt-dlp: pip install yt-dlp")
        return

    print(f"使用工具: {tool}")

    # 下载
    success_count = 0
    for name, url in videos.items():
        print(f"\n{'='*60}")
        print(f"下载: {name}")
        print(f"URL: {url[:80]}...")
        print('='*60)

        if tool == "yt-dlp":
            success = download_with_ytdlp(name, url, OUTPUT_DIR)
        else:
            success = download_with_curl(name, url, OUTPUT_DIR)

        if success:
            print(f"[OK] {name} 下载完成")
            success_count += 1
        else:
            print(f"[失败] {name}")

    print(f"\n{'='*60}")
    print(f"下载完成: {success_count}/{len(videos)}")
    print(f"视频保存在: {os.path.abspath(OUTPUT_DIR)}")
    print('='*60)


if __name__ == "__main__":
    main()
