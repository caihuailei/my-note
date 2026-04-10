#!/usr/bin/env python3
"""
批量下载视频的简化脚本
"""

import subprocess
import os

# 视频链接（从 video_links.txt 复制）
VIDEOS = {
    "第一节课下午": "https://111453136245362688.tenwiseacademy.cn/111453136245362688/b3b19f6c5b1324c3a86b79eb5f3b642e.mp4?network=0.53",
    "3月21日上午": "https://111453136245362688.tenwiseacademy.cn/111453136245362688/e356227defb5650b61d53c4bc007a61b.mp4?network=0.77",
    "3月21日下午": "https://111453136245362688.tenwiseacademy.cn/111453136245362688/c72918c09cf99fd1b1441cdaef69a85a.mp4?network=0.56",
    "3月28日上午": "https://111453136245362688.tenwiseacademy.cn/111453136245362688/330cdf9d769bc85f83509d68677c36ca.mp4?network=0",
    "3月28日下午": "https://111453136245362688.tenwiseacademy.cn/111453136245362688/9363c15b4042b4b5d61b54b1e459f21b.mp4?network=0",
}

def download_with_ytdlp():
    """使用 yt-dlp 下载（推荐，支持断点续传）"""
    print("使用 yt-dlp 下载视频...")

    for name, url in VIDEOS.items():
        filename = f"{name}.mp4"
        print(f"\n正在下载: {name}")

        # 使用 yt-dlp 下载
        cmd = [
            "yt-dlp",
            "-o", filename,
            "--no-check-certificate",
            url
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"[OK] {name} 下载完成")
        except subprocess.CalledProcessError as e:
            print(f"[错误] {name} 下载失败: {e}")


def download_with_curl():
    """使用 curl 下载（备用方案）"""
    print("使用 curl 下载视频...")

    for name, url in VIDEOS.items():
        filename = f"{name}.mp4"
        print(f"\n正在下载: {name}")

        cmd = [
            "curl",
            "-L",  # 跟随重定向
            "-o", filename,
            "--progress-bar",
            url
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"[OK] {name} 下载完成")
        except subprocess.CalledProcessError as e:
            print(f"[错误] {name} 下载失败: {e}")


def check_tools():
    """检查可用的下载工具"""
    import shutil

    if shutil.which("yt-dlp"):
        return "yt-dlp"
    elif shutil.which("curl"):
        return "curl"
    else:
        return None


if __name__ == "__main__":
    # 创建下载目录
    download_dir = "课程回放"
    os.makedirs(download_dir, exist_ok=True)
    os.chdir(download_dir)

    print(f"视频将下载到: {os.path.abspath('.')}")

    # 检查工具
    tool = check_tools()

    if tool == "yt-dlp":
        download_with_ytdlp()
    elif tool == "curl":
        download_with_curl()
    else:
        print("错误: 未找到 yt-dlp 或 curl")
        print("请先安装 yt-dlp: pip install yt-dlp")

    print("\n全部下载完成!")
