# Video Downloader Skill

自动获取网页视频直链并批量下载的 Claude Skill。

## 功能

- 🔍 使用 Playwright 自动获取视频直链
- 📥 批量下载多个视频
- 🎯 处理 Vue/React 动态加载的视频网站
- 📝 生成完整项目代码和教程

## 文件结构

```
video-downloader-skill/
├── SKILL.md                    # Skill 定义文件
├── scripts/
│   ├── get_and_download.py     # 一键获取并下载
│   ├── get_video_links.py      # 仅获取直链
│   └── download_videos.py      # 仅下载视频
├── references/
│   ├── video_config.example.json  # 配置示例
│   └── tutorial.md             # 使用教程
├── evals/
│   └── evals.json              # 测试用例
└── README.md                   # 本文件
```

## 安装

1. 复制 skill 文件夹到 Claude skills 目录：
```bash
cp -r video-downloader-skill ~/.claude/skills/
```

2. 或在 Claude Code 中使用：
```
/skill video-downloader
```

## 使用方法

### 场景 1：用户有视频页面链接

```
用户：帮我下载这些视频
https://example.com/video1
https://example.com/video2

Claude：
- 生成 get_video_links.py 脚本
- 生成 download_videos.py 脚本
- 提供运行命令
```

### 场景 2：用户需要教程

```
用户：怎么获取动态加载的视频地址？

Claude：
- 解释 Playwright 原理
- 提供完整代码示例
- 说明常见问题处理
```

### 场景 3：一键执行

```
用户：直接帮我下载这些视频

Claude：
- 运行脚本获取直链
- 批量下载视频
- 返回下载结果
```

## 触发条件

Skill 会在以下情况自动触发：

- 用户说"下载视频"、"获取视频链接"
- 提到"视频回放"、"课程下载"
- 问"Playwright 视频"相关问题
- 需要"批量下载视频"

## 依赖

- Python 3.8+
- playwright
- yt-dlp（可选，推荐）

## 安装依赖

```bash
pip install playwright
python -m playwright install chromium
pip install yt-dlp
```

## 示例输出

运行后会生成以下项目结构：

```
video-download-project/
├── get_video_links.py
├── download_videos.py
├── video_links.txt          # 生成的直链列表
└── downloads/               # 下载的视频
    ├── 第一节课下午.mp4
    └── ...
```

## 注意事项

- 只下载有权限访问的视频
- 尊重网站版权和 robots.txt
- 不用于破解 DRM 或绕过付费墙

## License

MIT
