import subprocess
import os
import re
from datetime import datetime

def parse_time_from_filename(filename):
    pattern = r'T(\d{6})Z'
    matches = re.findall(pattern, filename)
    if len(matches) >= 2:
        start_str = f"{matches[0][0:2]}:{matches[0][2:4]}:{matches[0][4:6]}"
        end_str = f"{matches[1][0:2]}:{matches[1][2:4]}:{matches[1][4:6]}"
        return start_str, end_str
    return None, None

def time_str_to_seconds(time_str):
    try:
        h, m, s = map(int, time_str.split(":"))
        return h * 3600 + m * 60 + s
    except:
        return None

def seconds_to_time_str(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}-{minutes:02d}-{secs:02d}"

def get_file_modify_date(file_path):
    try:
        return datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d")
    except:
        return "unknown_date"

def calculate_overlap_time(target_start, target_end, video_start, video_end):
    overlap_start = max(target_start, video_start)
    overlap_end = min(target_end, video_end)
    return (overlap_start, overlap_end) if overlap_start < overlap_end else (None, None)

def extract_single_video_frames(video_path, root_output_dir, target_start_str, target_end_str, interval=1):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_start_str, video_end_str = parse_time_from_filename(video_name)
    if not video_start_str or not video_end_str:
        print(f"❌ {video_name} - 文件名解析失败")
        return False
    print(f"📌 {video_name} - 录制时间：{video_start_str} ~ {video_end_str}")

    target_start = time_str_to_seconds(target_start_str)
    target_end = time_str_to_seconds(target_end_str)
    video_start = time_str_to_seconds(video_start_str)
    video_end = time_str_to_seconds(video_end_str)
    if None in [target_start, target_end, video_start, video_end]:
        return False

    overlap_start, overlap_end = calculate_overlap_time(target_start, target_end, video_start, video_end)
    if not overlap_start:
        print(f"⚠️ {video_name} - 无重叠时段，跳过")
        return False
    print(f"✅ 重叠时段：{seconds_to_time_str(overlap_start)} ~ {seconds_to_time_str(overlap_end)}")

    # ✅ 关键修复：转换为视频内部的相对时间
    relative_start = overlap_start - video_start
    relative_end = overlap_end - video_start
    print(f"➡️  相对切帧时间：{relative_start} 秒 ~ {relative_end} 秒")

    video_date = get_file_modify_date(video_path)
    time_label = f"{seconds_to_time_str(overlap_start)}_to_{seconds_to_time_str(overlap_end)}"
    output_dir = os.path.join(root_output_dir, video_date, f"{video_name}_{time_label}")
    os.makedirs(output_dir, exist_ok=True)

    frame_format = "png"
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(relative_start),  # ✅ 用相对时间，从视频开头算
        "-to", str(relative_end),    # ✅ 用相对时间
        "-i", video_path,
        "-vf", f"fps=1/{interval}",  # 1秒1帧（interval=1）
        "-c:v", "png",
        "-hide_banner",
        os.path.join(output_dir, f"{video_name}_%04d.{frame_format}")
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        if result.returncode == 0:
            frame_files = [f for f in os.listdir(output_dir) if f.startswith(video_name) and f.endswith(f".{frame_format}")]
            frame_count = len(frame_files)
            expected_frames = int((relative_end - relative_start) // interval)
            print(f"📊 预期帧数：{expected_frames} | 实际提取：{frame_count}")
            if frame_count == 0:
                print(f"⚠️ {video_name} - 0帧！请检查相对时间是否正确")
            else:
                print(f"🎉 {video_name} - 成功提取{frame_count}帧 → {output_dir}")
            return True
        else:
            print(f"❌ {video_name} - 切帧失败：{result.stderr[:300]}")
            return False
    except Exception as e:
        print(f"❌ {video_name} - 程序异常：{str(e)}")
        return False

def batch_extract_video_frames(video_dir, root_output_dir, target_start_str, target_end_str, interval=1):
    if not os.path.isdir(video_dir):
        print(f"错误：视频文件夹不存在 → {video_dir}")
        return
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.split(".")[-1].lower() in ("mp4", "mov", "avi", "mkv")]
    if not video_files:
        print("提示：未找到支持的视频文件")
        return
    print(f"\n📢 开始批量处理：共{len(video_files)}个视频 | 目标时段：{target_start_str} ~ {target_end_str} | 帧率：1/{interval} 帧/秒")
    success, fail = 0, 0
    for f in video_files:
        if extract_single_video_frames(f, root_output_dir, target_start_str, target_end_str, interval):
            success += 1
        else:
            fail += 1
        print("-" * 80)
    print(f"\n📊 批量处理完成 | 成功：{success} | 失败：{fail}")
    print(f"📁 所有帧图片保存至：{root_output_dir}")

if __name__ == "__main__":
    # VIDEO_DIR = r"F:\a5_102"
    # ROOT_OUTPUT_DIR = r"F:\a5_102\img"
    VIDEO_DIR = r"F:\a12_401"
    ROOT_OUTPUT_DIR = r"F:\a12_401\img"

    TARGET_START_STR = "15:10:00"#目标开始时间（可改为09:00:00等）
    TARGET_END_STR = "15:35:00"#目标结束时间（可改为11:00:00等）
    INTERVAL = 145  # ✅ 1秒1帧（可改为2、5等）

    batch_extract_video_frames(VIDEO_DIR, ROOT_OUTPUT_DIR, TARGET_START_STR, TARGET_END_STR, INTERVAL)