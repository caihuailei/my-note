#!/usr/bin/env python3
"""
获取视频直链
独立脚本，只负责获取链接，不负责下载
"""

import asyncio
import json
import sys
from playwright.async_api import async_playwright


async def get_video_url(name, url):
    """获取单个视频的直链"""
    print(f"\n{'='*60}")
    print(f"正在获取: {name}")
    print(f"页面URL: {url}")
    print('='*60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()

        found_urls = []

        async def handle_response(response):
            """监听响应，筛选视频链接"""
            resp_url = response.url

            if '.mp4' in resp_url:
                print(f"[OK] 找到视频直链: {resp_url}")
                found_urls.append(resp_url)

            if any(kw in resp_url for kw in ['api', 'vod', 'play']):
                try:
                    content_type = response.headers.get('content-type', '')
                    if 'json' in content_type:
                        body = await response.body()
                        text = body.decode('utf-8', errors='ignore')
                        if '.mp4' in text:
                            print(f"[API] {resp_url}")
                except:
                    pass

        page.on("response", lambda r: asyncio.create_task(handle_response(r)))

        try:
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(3)

            # 尝试点击播放按钮
            play_selectors = ['video', '.play-btn', '[class*="play"]', 'button']
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

            await asyncio.sleep(8)

            # 从DOM提取
            video_elements = await page.query_selector_all('video')
            for i, video in enumerate(video_elements):
                src = await video.get_attribute('src')
                if src:
                    print(f"[OK] video[{i}] src: {src}")
                    found_urls.append(src)

                sources = await video.query_selector_all('source')
                for j, source in enumerate(sources):
                    src = await source.get_attribute('src')
                    if src:
                        print(f"[OK] source[{j}] src: {src}")
                        found_urls.append(src)

        except Exception as e:
            print(f"[错误] {e}")

        await browser.close()
        return found_urls[0] if found_urls else None


async def main():
    """主函数"""
    # 从配置文件读取
    try:
        with open('video_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            VIDEO_URLS = config['videos']
    except FileNotFoundError:
        # 默认配置
        VIDEO_URLS = [
            ("示例视频", "https://example.com/video"),
        ]

    print("开始获取视频直链...")
    print(f"共 {len(VIDEO_URLS)} 个视频")

    results = {}
    for name, url in VIDEO_URLS:
        link = await get_video_url(name, url)
        if link:
            results[name] = link

    # 输出结果
    print("\n" + "="*60)
    print("获取结果汇总:")
    print("="*60)
    for name, url in results.items():
        print(f"\n{name}:\n  {url}")

    # 保存
    with open('video_links.txt', 'w', encoding='utf-8') as f:
        for name, url in results.items():
            f.write(f"{name}\n{url}\n\n")
    print("\n结果已保存到 video_links.txt")


if __name__ == "__main__":
    asyncio.run(main())
