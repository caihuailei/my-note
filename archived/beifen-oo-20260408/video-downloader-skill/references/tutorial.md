# Video Downloader 使用教程

## 快速开始

### 1. 安装依赖

```bash
pip install playwright
python -m playwright install chromium
```

可选（推荐）：
```bash
pip install yt-dlp
```

### 2. 准备视频列表

创建 `video_config.json`：

```json
{
  "videos": [
    ["视频名称1", "https://example.com/video1"],
    ["视频名称2", "https://example.com/video2"]
  ]
}
```

### 3. 获取视频直链

```bash
python get_video_links.py
```

输出：`video_links.txt`

### 4. 下载视频

```bash
python download_videos.py
```

视频将保存到 `downloads/` 目录。

---

## 一键执行

```bash
python get_and_download.py \
  --urls "视频1|https://url1,视频2|https://url2" \
  --output "我的视频"
```

---

## 常见问题

### Q: 找不到视频链接？

A: 尝试增加等待时间：
```python
await asyncio.sleep(10)  # 改为10秒或更长
```

### Q: 视频需要登录？

A: 在代码中添加 cookies：
```python
await context.add_cookies([
    {'name': 'session', 'value': 'your_cookie', 'domain': '.example.com'}
])
```

### Q: 下载速度慢？

A: 使用 aria2 代替 curl：
```bash
aria2c -x 16 -s 16 "视频URL"
```

### Q: 视频是 m3u8 格式？

A: 使用 ffmpeg 下载：
```bash
ffmpeg -i "m3u8_url" -c copy output.mp4
```

---

## 高级技巧

### 有界面模式调试

```python
browser = await p.chromium.launch(headless=False)
```

### 截图调试

```python
await page.screenshot(path='debug.png')
```

### 拦截特定请求

```python
async def handle_route(route, request):
    if 'video' in request.url:
        print(f"视频请求: {request.url}")
    await route.continue_()

await page.route("**/*", handle_route)
```
