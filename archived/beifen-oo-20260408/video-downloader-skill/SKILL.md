---
name: video-downloader
description: |
  自动获取网页视频直链并批量下载。适用于在线教育平台、视频网站等使用动态加载的站点。

  使用场景：
  - 用户提到"下载视频"、"获取视频链接"、"视频回放"
  - 需要批量下载课程视频、直播回放
  - 视频网站使用 Vue/React 动态加载，无法直接找到视频地址
  - 想要用 Python 自动化下载网页视频

  触发关键词：视频下载、获取直链、视频回放、课程下载、批量下载视频、playwright 视频
compatibility: |
  需要：Python 3.8+, playwright, yt-dlp (可选)
---

# Video Downloader Skill

帮助用户自动获取网页视频直链并批量下载。

## 能力范围

本 skill 可以：
- ✓ 使用 Playwright 自动化浏览器获取视频直链
- ✓ 批量下载多个视频
- ✓ 处理动态加载的视频网站（Vue/React）
- ✓ 生成完整的项目代码和教程

本 skill 不能：
- ✗ 破解 DRM 加密的视频
- ✗ 绕过付费墙获取未授权内容
- ✗ 处理需要复杂验证码的站点

## 工作流程

### 快速开始（一键执行）

如果用户只想快速下载视频，直接运行：

```bash
python scripts/get_and_download.py --urls "url1,url2,url3" --output "下载目录"
```

### 分步执行（推荐学习用）

**Step 1: 获取视频直链**

```python
# get_video_links.py
import asyncio
from playwright.async_api import async_playwright

VIDEO_URLS = [
    ("视频名称1", "https://example.com/video1"),
    ("视频名称2", "https://example.com/video2"),
]

async def get_video_url(name, url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        found_urls = []

        async def handle_response(response):
            resp_url = response.url
            if '.mp4' in resp_url or '.m3u8' in resp_url:
                print(f"[发现] {resp_url}")
                found_urls.append(resp_url)

        page.on("response", lambda r: asyncio.create_task(handle_response(r)))

        await page.goto(url, wait_until='networkidle')
        await asyncio.sleep(5)  # 等待视频加载

        await browser.close()
        return found_urls[0] if found_urls else None

async def main():
    results = {}
    for name, url in VIDEO_URLS:
        link = await get_video_url(name, url)
        if link:
            results[name] = link

    # 保存结果
    with open('video_links.txt', 'w') as f:
        for name, url in results.items():
            f.write(f"{name}\n{url}\n\n")

asyncio.run(main())
```

**Step 2: 批量下载视频**

```python
# download_videos.py
import subprocess
import os

with open('video_links.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

# 创建下载目录
os.makedirs('downloads', exist_ok=True)
os.chdir('downloads')

# 每两行一组：名称 + URL
for i in range(0, len(lines), 2):
    name = lines[i]
    url = lines[i+1]

    print(f"下载: {name}")
    subprocess.run([
        'yt-dlp', '-o', f'{name}.mp4', url
    ])
```

## 核心原理

```
用户访问页面 → 加载HTML/JS → JS请求视频API → 返回视频直链 → 播放器加载
     ↑                                                       ↓
     └──────────── Playwright 拦截响应 ←─────────────────────┘
```

Playwright 在浏览器层面拦截所有网络请求，因此可以捕获动态加载的视频地址。

## 关键技巧

| 技巧 | 作用 | 代码示例 |
|-----|------|---------|
| 响应监听 | 捕获视频请求 | `page.on("response", handler)` |
| 点击播放 | 触发视频加载 | `await page.click('.play-btn')` |
| 等待加载 | 给JS执行时间 | `await asyncio.sleep(5)` |
| DOM查询 | 提取video标签 | `await page.query_selector_all('video')` |
| JS执行 | 获取页面变量 | `await page.evaluate('...')` |

## 常见问题处理

### 1. 视频需要登录

```python
# 添加 cookies
await context.add_cookies([
    {'name': 'session_id', 'value': 'xxx', 'domain': '.example.com'}
])
```

### 2. 视频格式是 m3u8

```python
# 检测 m3u8
if '.m3u8' in resp_url:
    found_urls.append(resp_url)

# 下载时使用 ffmpeg
subprocess.run(['ffmpeg', '-i', m3u8_url, '-c', 'copy', 'output.mp4'])
```

### 3. Windows 中文乱码

```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### 4. 找不到视频链接

增加等待时间和调试：
```python
await asyncio.sleep(10)  # 增加等待
await page.screenshot(path='debug.png')  # 截图查看
```

## 完整项目结构

为用户生成项目时，创建以下结构：

```
video-download-project/
├── get_video_links.py      # 获取直链脚本
├── download_videos.py      # 批量下载脚本
├── video_links.txt         # 直链列表（生成）
├── downloads/              # 下载的视频（生成）
└── 教程.md                  # 详细教程
```

## 用户输入示例

用户可能会这样说：

- "帮我下载这些视频链接"
- "怎么获取这个网站的视频直链"
- "写个脚本批量下载课程回放"
- "Playwright 能用来下载视频吗"
- "这些视频链接用 IDM 下载不了"

## 输出说明

根据用户需求，输出可以是：

1. **完整项目** - 生成包含所有代码的项目文件夹
2. **单个脚本** - 只提供 get_video_links.py 或 download_videos.py
3. **教程文档** - 详细的 markdown 教程
4. **直接执行** - 运行脚本帮用户下载

## 进阶：下载工具选择

| 工具 | 优点 | 适用场景 |
|-----|------|---------|
| yt-dlp | 断点续传、自动重试 | 大文件、网络不稳定 |
| curl | 系统自带 | 简单快速下载 |
| wget | 支持递归 | Linux 服务器 |
| ffmpeg | 处理 m3u8 | 流媒体视频 |
| aria2 | 多线程高速 | 批量高速下载 |

## 安全提示

- 只下载用户有权限访问的视频
- 尊重网站的 robots.txt 和版权
- 不要用于破解 DRM 或绕过付费墙
