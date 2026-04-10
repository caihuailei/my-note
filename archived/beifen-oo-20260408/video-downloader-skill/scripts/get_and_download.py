#!/usr/bin/env python3
"""
一键获取并下载视频
合并了获取直链和下载两个步骤
"""

import argparse
import asyncio
import os
import subprocess
import sys
from playwright.async_api import async_playwright


async def get_video_links(urls_dict):
    """获取视频直链"""
    results = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        for name, url in urls_dict.items():
            print(f"\n[获取] {name}: {url}")
            page = await context.new_page()
            found_urls = []

            async def handle_response(response):
                resp_url = response.url
                if '.mp4' in resp_url or '.m3u8' in resp_url:
                    print(f"  [发现] {resp_url[:80]}...")
                    found_urls.append(resp_url)

            page.on("response", lambda r: asyncio.create_task(handle_response(r)))

            try:
                await page.goto(url, wait_until='networkidle', timeout=60000)
                await asyncio.sleep(5)

                # 尝试点击播放
                for selector in ['video', '.play-btn', '[class*="play"]']:
                    try:
                        elem = await page.query_selector(selector)
                        if elem:
                            await elem.click()
                            await asyncio.sleep(2)
                            break
                    except:
                        pass

                await asyncio.sleep(5)

                if found_urls:
                    results[name] = found_urls[0]
                    print(f"  [成功] 找到 {len(found_urls)} 个链接")
                else:
                    print(f"  [失败] 未找到视频链接")

            except Exception as e:
                print(f"  [错误] {e}")

            await page.close()

        await browser.close()

    return results


def download_videos(links_dict, output_dir):
    """批量下载视频"""
    os.makedirs(output_dir, exist_ok=True)

    for name, url in links_dict.items():
        filename = f"{name}.mp4"
        filepath = os.path.join(output_dir, filename)

        print(f"\n[下载] {name}")

        # 优先使用 yt-dlp
        if subprocess.run(['which', 'yt-dlp'], capture_output=True).returncode == 0:
            cmd = ['yt-dlp', '-o', filepath, '--no-check-certificate', url]
        else:
            # 备用 curl
            cmd = ['curl', '-L', '-o', filepath, url]

        try:
            subprocess.run(cmd, check=True)
            print(f"  [完成] {filepath}")
        except subprocess.CalledProcessError as e:
            print(f"  [失败] {e}")


def main():
    parser = argparse.ArgumentParser(description='一键获取并下载视频')
    parser.add_argument('--urls', required=True, help='视频URL，格式: "名称1|url1,名称2|url2"')
    parser.add_argument('--output', default='downloads', help='输出目录')
    parser.add_argument('--skip-download', action='store_true', help='只获取链接，不下载')

    args = parser.parse_args()

    # 解析URL
    urls_dict = {}
    for item in args.urls.split(','):
        if '|' in item:
            name, url = item.split('|', 1)
            urls_dict[name.strip()] = url.strip()

    print(f"共 {len(urls_dict)} 个视频")
    print(f"输出目录: {args.output}")

    # 获取直链
    links = asyncio.run(get_video_links(urls_dict))

    # 保存链接
    with open('video_links.txt', 'w', encoding='utf-8') as f:
        for name, url in links.items():
            f.write(f"{name}\n{url}\n\n")
    print(f"\n链接已保存到 video_links.txt")

    # 下载视频
    if not args.skip_download and links:
        print(f"\n开始下载...")
        download_videos(links, args.output)

    print("\n全部完成!")


if __name__ == '__main__':
    main()
