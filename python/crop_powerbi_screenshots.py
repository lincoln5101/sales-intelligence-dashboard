"""
crop_powerbi_screenshots.py
Crop full Power BI Desktop window captures to the report page canvas.

Prefer exporting pre-cropped screenshots from Power BI (View → Fit to page,
then capture the canvas) and copying them directly into powerbi/screenshots/.
Only use this script when you have full-window captures that still include
the ribbon, tabs, or side panes.

Usage:
    python python/crop_powerbi_screenshots.py path/to/screenshot.png
    python python/crop_powerbi_screenshots.py assets/*.png --out powerbi/screenshots/
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

# Calibrated for 1024x661 Power BI Desktop captures (100% zoom, standard layout)
REPORT_PAGE_BOX = (56, 109, 938, 603)  # left, top, right, bottom (PIL exclusive right/bottom)


def crop_report_canvas(image_path: Path, output_path: Path | None = None) -> Path:
    """Crop a Power BI window screenshot to the report page bounds."""
    output_path = output_path or image_path
    with Image.open(image_path) as im:
        cropped = im.convert("RGB").crop(REPORT_PAGE_BOX)
        cropped.save(output_path, format="PNG", optimize=True)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Crop Power BI screenshots to report canvas.")
    parser.add_argument("images", nargs="+", type=Path, help="Input screenshot file(s)")
    parser.add_argument("--out", type=Path, help="Output directory (defaults to in-place)")
    args = parser.parse_args()

    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)

    for image_path in args.images:
        if args.out:
            out_path = args.out / image_path.name
        else:
            out_path = image_path
        crop_report_canvas(image_path, out_path)
        print(f"Cropped {image_path.name} -> {out_path}")


if __name__ == "__main__":
    main()
