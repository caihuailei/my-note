#!/usr/bin/env python3
"""
打包 Video Downloader Skill
生成 .skill 文件供安装
"""

import os
import shutil
import sys
from pathlib import Path


def package_skill(skill_dir, output_dir=None):
    """打包 skill 为 zip 文件"""

    skill_dir = Path(skill_dir).resolve()
    skill_name = skill_dir.name

    if output_dir is None:
        output_dir = skill_dir.parent
    else:
        output_dir = Path(output_dir).resolve()

    output_file = output_dir / f"{skill_name}.skill"

    print(f"打包 skill: {skill_name}")
    print(f"源目录: {skill_dir}")
    print(f"输出文件: {output_file}")

    # 创建临时目录
    temp_dir = output_dir / f"temp_{skill_name}"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    # 复制文件（排除不需要的文件）
    shutil.copytree(skill_dir, temp_dir, ignore=shutil.ignore_patterns(
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.git',
        '.gitignore',
        '*.skill',
        'downloads',
        '课程回放',
        '*.mp4',
        '*.log'
    ))

    # 创建 zip 文件
    shutil.make_archive(
        str(output_file).replace('.skill', ''),
        'zip',
        temp_dir
    )

    # 重命名为 .skill
    zip_file = output_file.with_suffix('.zip')
    if zip_file.exists():
        zip_file.rename(output_file)

    # 清理临时目录
    shutil.rmtree(temp_dir)

    print(f"\n[OK] 打包完成: {output_file}")
    print(f"文件大小: {output_file.stat().st_size / 1024:.1f} KB")

    return output_file


def main():
    # 默认打包当前目录的 skill
    skill_dir = Path(__file__).parent.parent

    print("="*60)
    print("Video Downloader Skill 打包工具")
    print("="*60)

    output_file = package_skill(skill_dir)

    print("\n使用说明:")
    print(f"1. 将 {output_file.name} 复制到目标位置")
    print(f"2. 解压到 ~/.claude/skills/ 目录")
    print(f"3. 在 Claude 中使用 /skill video-downloader")

    return 0


if __name__ == "__main__":
    sys.exit(main())
