#!/usr/bin/env python3
"""SVG → PNG converter for meeting minutes cards.

Usage:
    python3 scripts/svg2png.py input.svg              # → input.png (2x)
    python3 scripts/svg2png.py input.svg output.png    # explicit output path
    python3 scripts/svg2png.py input.svg --scale 3     # 3x resolution
"""
import subprocess, sys, os

def ensure_cairosvg():
    try:
        import cairosvg
        return cairosvg
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               "--break-system-packages", "-q", "cairosvg"])
        import cairosvg
        return cairosvg

def convert(svg_path, png_path=None, scale=2):
    cairosvg = ensure_cairosvg()
    if png_path is None:
        png_path = os.path.splitext(svg_path)[0] + ".png"
    cairosvg.svg2png(url=svg_path, write_to=png_path, scale=scale)
    from PIL import Image
    w, h = Image.open(png_path).size
    print(f"✔ {png_path}  ({w}×{h}px, scale={scale})")
    return png_path

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("svg")
    p.add_argument("png", nargs="?")
    p.add_argument("--scale", type=int, default=2)
    args = p.parse_args()
    convert(args.svg, args.png, args.scale)
