#!/usr/bin/env python3
"""把一个目录里的 HTML 页面批量截成 1242x1656 的 PNG。

用法:
    python3 render.py <页面目录> [--width 1242] [--height 1656]

每个 xxx.html 生成同名 xxx.png。需要装好 Chrome / Chromium，
以及中文字体（比如 Noto Sans CJK），不然中文会变方块。
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

CANDIDATES = ["google-chrome", "chromium", "chromium-browser", "chrome"]


def find_browser():
    for name in CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    sys.exit("找不到 Chrome/Chromium，先装一个")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="放 HTML 页面的目录")
    ap.add_argument("--width", type=int, default=1242)
    ap.add_argument("--height", type=int, default=1656)
    args = ap.parse_args()

    root = pathlib.Path(args.dir).resolve()
    pages = sorted(root.glob("*.html"))
    if not pages:
        sys.exit(f"{root} 里没有 .html 文件")

    browser = find_browser()
    for page in pages:
        out = page.with_suffix(".png")
        subprocess.run(
            [
                browser,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                f"--window-size={args.width},{args.height}",
                f"--screenshot={out}",
                page.as_uri(),
            ],
            check=True,
            capture_output=True,
        )
        print(f"ok  {out.name}")


if __name__ == "__main__":
    main()
