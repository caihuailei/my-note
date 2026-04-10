#!/usr/bin/env python3
"""
自动获取视频直链的脚本
使用 Playwright 拦截网络请求
"""

import asyncio
import json
import sys
from playwright.async_api import async_playwright

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')

# 需要获取的视频页面
VIDEO_URLS = [
    ("第一节课下午", "https://chgdegabxaa.kekpwl.cn/c/7NXTMn3"),
    ("3月21日上午", "https://chgdegabxaa.kekpwl.cn/c/ZFvrrw3"),
    ("3月21日下午", "https://chgdegabxaa.kekpwl.cn/c/Fr6Rrw3"),
    ("3月28日上午", "https://chgdegabxaa.kekpwl.cn/c/7ngrhp3"),
    ("3月28日下午", "https://chgdegabxaa.kekpwl.cn/c/9qaarzhp3"),
]

video_links = {}
current_video_name = None

async def get_video_url(name, url):
    """获取单个视频的直链"""
    global current_video_name
    current_video_name = name

    print(f"\n{'='*60}")
    print(f"正在获取: {name}")
    print(f"页面URL: {url}")
    print('='*60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        page = await context.new_page()

        found_urls = []

        # 监听响应
        async def handle_response(response):
            resp_url = response.url

            # 查找mp4直链
            if '.mp4' in resp_url and 'volcengine' in resp_url:
                print(f"[OK] 找到视频直链: {resp_url}")
                found_urls.append(resp_url)
                video_links[name] = resp_url

            # 查找包含视频信息的API响应
            if any(keyword in resp_url for keyword in ['api', 'vod', 'play', 'info', 'video']):
                try:
                    content_type = response.headers.get('content-type', '')
                    if 'json' in content_type or 'text' in content_type:
                        body = await response.body()
                        text = body.decode('utf-8', errors='ignore')
                        if '.mp4' in text or 'm3u8' in text:
                            print(f"[API] {resp_url}")
                            print(f"内容: {text[:500]}")
                except:
                    pass

        page.on("response", lambda response: asyncio.create_task(handle_response(response)))

        try:
            # 访问页面
            await page.goto(url, wait_until='networkidle', timeout=60000)

            # 等待页面加载
            await asyncio.sleep(3)

            # 尝试点击播放按钮
            try:
                play_selectors = ['video', '.play-btn', '[class*="play"]', 'button', '[class*="video"]', '.vjs-big-play-button']
                for selector in play_selectors:
                    try:
                        element = await page.query_selector(selector)
                        if element:
                            await element.click()
                            print(f"[点击] {selector}")
                            await asyncio.sleep(2)
                            break
                    except:
                        continue
            except Exception as e:
                print(f"点击失败: {e}")

            # 等待视频加载
            await asyncio.sleep(8)

            # 从页面中提取视频src
            video_elements = await page.query_selector_all('video')
            print(f"[信息] 找到 {len(video_elements)} 个 video 元素")

            for i, video in enumerate(video_elements):
                src = await video.get_attribute('src')
                if src:
                    print(f"[OK] video[{i}] src: {src}")
                    found_urls.append(src)
                    video_links[name] = src

                # 查找source子元素
                sources = await video.query_selector_all('source')
                for j, source in enumerate(sources):
                    src = await source.get_attribute('src')
                    if src:
                        print(f"[OK] source[{j}] src: {src}")
                        found_urls.append(src)
                        video_links[name] = src

            # 通过JavaScript获取视频地址
            js_video_urls = await page.evaluate('''() => {
                const urls = [];
                document.querySelectorAll('video').forEach(v => {
                    if (v.src) urls.push(v.src);
                    v.querySelectorAll('source').forEach(s => {
                        if (s.src) urls.push(s.src);
                    });
                });
                // 查找window中的视频数据
                for (let key in window) {
                    try {
                        const val = window[key];
                        if (val && typeof val === 'object') {
                            const str = JSON.stringify(val);
                            if (str && str.includes('.mp4')) {
                                urls.push('DATA_IN: ' + key);
                            }
                        }
                    } catch(e) {}
                }
                return urls;
            }''')

            for vurl in js_video_urls:
                print(f"[JS] 找到: {vurl}")

        except Exception as e:
            print(f"错误: {e}")

        await browser.close()

        if name not in video_links and found_urls:
            video_links[name] = found_urls[0]

async def main():
    """主函数"""
    print("开始自动获取视频直链...")
    print(f"共 {len(VIDEO_URLS)} 个视频")

    for name, url in VIDEO_URLS:
        await get_video_url(name, url)

    # 输出结果
    print("\n" + "="*60)
    print("获取结果汇总:")
    print("="*60)
    for name, url in VIDEO_URLS:
        if name in video_links:
            print(f"\n{name}:")
            print(f"  {video_links[name]}")
        else:
            print(f"\n{name}: [未找到]")

    # 保存到文件
    with open('video_links.txt', 'w', encoding='utf-8') as f:
        for name, url in VIDEO_URLS:
            if name in video_links:
                f.write(f"{name}\n{video_links[name]}\n\n")
    print("\n结果已保存到 video_links.txt")

if __name__ == "__main__":
    asyncio.run(main())
