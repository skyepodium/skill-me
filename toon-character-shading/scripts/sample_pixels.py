#!/usr/bin/env python3
"""Average RGB / HSV at named points of one or more captures, to compare skin or surfaces across renders.

Usage: sample_pixels.py image.png name:x,y [name:x,y ...] [--radius 2]
Several images: repeat --image path before the points apply to all images.
"""
import argparse, colorsys
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', action='append', required=True, help='capture to sample (repeatable)')
    parser.add_argument('--radius', type=int, default=2, help='half size of the sampled square in pixels')
    parser.add_argument('points', nargs='+', help='name:x,y in pixels (origin top-left)')
    args = parser.parse_args()
    for path in args.image:
        image = Image.open(path).convert('RGB')
        print(path)
        for point in args.points:
            name, xy = point.split(':')
            x, y = (int(v) for v in xy.split(','))
            box = [image.getpixel((x + dx, y + dy)) for dx in range(-args.radius, args.radius + 1) for dy in range(-args.radius, args.radius + 1)]
            rgb = tuple(sum(c[i] for c in box) // len(box) for i in range(3))
            h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
            print(f'  {name:<12} rgb {rgb}  hue {h * 360:5.1f}  sat {s:.2f}  val {v:.2f}')

if __name__ == '__main__':
    main()
