#!/usr/bin/env python3
"""Measure water regions in reference images and game captures.

Each argument is IMAGE:x0,y0,x1,y1:LABEL (pixel box). For every box it prints hue, saturation, value,
mean RGB and the share of bright twinkle pixels (luminance > --glint-threshold). Use one box per
zone you care about: shallows at the bank, the body of the water, far/grazing water.

  water_palette_compare.py ref.png:0,150,652,200:ref-near  capture.png:1050,520,1150,600:game-centre
Requires numpy and pillow (e.g. `uv run --with numpy --with pillow water_palette_compare.py ...`).
Keep boxes on water only: grass, foam-free sand or UI inside a box skews the numbers.
"""
import argparse
import colorsys

import numpy as np
from PIL import Image


def measure(path, box, glint_threshold):
    pixels = np.asarray(Image.open(path).convert("RGB")).astype(np.float32) / 255.0
    x0, y0, x1, y1 = box
    region = pixels[y0:y1, x0:x1].reshape(-1, 3)
    mean = region.mean(0)
    hue, saturation, value = colorsys.rgb_to_hsv(*mean)
    luminance = region @ np.array([0.3, 0.59, 0.11], dtype=np.float32)
    return hue * 360, saturation, value, tuple(int(round(channel * 255)) for channel in mean), (luminance > glint_threshold).mean() * 100


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("regions", nargs="+", metavar="IMAGE:x0,y0,x1,y1:LABEL")
    parser.add_argument("--glint-threshold", type=float, default=0.9)
    args = parser.parse_args()
    print(f"{'label':<22} {'hue':>5} {'S':>5} {'V':>5} {'RGB':>16} {'glint%':>7}")
    for item in args.regions:
        path, box_text, label = item.rsplit(":", 2)
        box = [int(value) for value in box_text.split(",")]
        hue, saturation, value, rgb, glints = measure(path, box, args.glint_threshold)
        print(f"{label:<22} {hue:5.0f} {saturation:5.2f} {value:5.2f} {str(rgb):>16} {glints:7.1f}")


if __name__ == "__main__":
    main()
