#!/usr/bin/env python3
"""
Video Downloader Skill 安装脚本
"""

import subprocess
import sys
import os


def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n[安装] {description}...")
    print(f"命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"[成功] {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[失败] {description}")
        print(f"错误: {e}")
        if e.stderr:
            print(e.stderr)
        return False


def main():
    print("="*60)
    print("Video Downloader Skill 安装程序")
    print("="*60)

    # 检查 Python 版本
    print(f"\nPython 版本: {sys.version}")
    if sys.version_info < (3, 8):
        print("错误: 需要 Python 3.8 或更高版本")
        return 1

    # 安装依赖
    steps = [
        ([sys.executable, "-m", "pip", "install", "playwright"], "安装 Playwright"),
        ([sys.executable, "-m", "playwright", "install", "chromium"], "安装 Chromium 浏览器"),
        ([sys.executable, "-m", "pip", "install", "yt-dlp"], "安装 yt-dlp (可选)"),
    ]

    success_count = 0
    for cmd, desc in steps:
        if run_command(cmd, desc):
            success_count += 1

    print("\n" + "="*60)
    print(f"安装完成: {success_count}/{len(steps)}")
    print("="*60)

    if success_count == len(steps):
        print("\n✓ 所有依赖安装成功！")
        print("\n你可以使用以下命令测试:")
        print("  python scripts/get_video_links.py")
        return 0
    else:
        print("\n⚠ 部分安装失败，请检查错误信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
