"""
研报分析系统 - PDF图片提取工具

从研报PDF中提取所有有意义的图表和图片，
保存到 reports/{TICKER}/analysis/images/ 目录下。

用法: uv run python extract_images.py GOOGL
      uv run python extract_images.py GOOGL --min-size 200
"""

import sys
import os
import argparse
from pathlib import Path

# Windows环境下强制使用UTF-8编码输出
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ 请先安装 pymupdf: uv add pymupdf")
    sys.exit(1)

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"


def extract_images(ticker: str, min_size: int = 100) -> dict:
    """
    从指定标的的所有PDF研报中提取图片

    参数:
        ticker: 标的代码
        min_size: 最小图片尺寸（宽和高都必须 >= 此值），过滤小图标

    返回:
        提取结果字典 {pdf_filename: [image_info, ...]}
    """
    originals_dir = REPORTS_DIR / ticker / "originals"
    output_dir = REPORTS_DIR / ticker / "analysis" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not originals_dir.exists():
        print(f"❌ 研报目录不存在: {originals_dir}")
        return {}

    pdf_files = list(originals_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ 未找到PDF文件: {originals_dir}")
        return {}

    print(f"\n{'='*60}")
    print(f"  🖼️  提取 {ticker} 研报图表")
    print(f"{'='*60}\n")
    print(f"  📁 来源: {originals_dir}")
    print(f"  📁 输出: {output_dir}")
    print(f"  📏 最小尺寸: {min_size}x{min_size}")
    print()

    results = {}

    for pdf_path in sorted(pdf_files):
        pdf_name = pdf_path.name
        # 截断文件名前缀（最多30字符）用于图片命名
        prefix = pdf_name.replace(".pdf", "")[:30]

        doc = fitz.open(str(pdf_path))
        total_pages = len(doc)
        extracted = []

        for page_num in range(total_pages):
            page = doc[page_num]
            images = page.get_images(full=True)

            for img_idx, img_info in enumerate(images):
                xref = img_info[0]
                try:
                    base_image = doc.extract_image(xref)
                except Exception:
                    continue

                if not base_image:
                    continue

                w = base_image["width"]
                h = base_image["height"]

                # 过滤小图标
                if w < min_size or h < min_size:
                    continue

                ext = base_image["ext"]
                img_data = base_image["image"]
                img_filename = f"{prefix}_p{page_num + 1}_img{img_idx + 1}.{ext}"
                img_path = output_dir / img_filename

                with open(img_path, "wb") as f:
                    f.write(img_data)

                img_info_dict = {
                    "filename": img_filename,
                    "page": page_num + 1,
                    "width": w,
                    "height": h,
                    "size_bytes": len(img_data),
                    "format": ext,
                }
                extracted.append(img_info_dict)
                print(f"  📸 {img_filename} ({w}x{h})")

        doc.close()
        results[pdf_name] = extracted

        # 统计有效图表（排除纯黑/纯深色背景图）
        meaningful = [img for img in extracted if img["width"] >= 400 and img["height"] >= 300]
        print(f"  📄 {pdf_name}: {len(extracted)} 张图片提取, {len(meaningful)} 张有效图表")
        print()

    # 汇总
    total_images = sum(len(imgs) for imgs in results.values())
    print(f"{'='*60}")
    print(f"  ✅ 提取完成! 共 {len(results)} 份PDF, {total_images} 张图片")
    print(f"  📁 保存至: {output_dir}")
    print(f"{'='*60}\n")

    return results


def main():
    parser = argparse.ArgumentParser(description="从研报PDF中提取图片")
    parser.add_argument("ticker", type=str, help="标的代码，如 GOOGL")
    parser.add_argument(
        "--min-size", type=int, default=100,
        help="最小图片尺寸（像素），过滤小图标 (默认: 100)"
    )
    args = parser.parse_args()

    extract_images(args.ticker.upper(), args.min_size)


if __name__ == "__main__":
    main()
