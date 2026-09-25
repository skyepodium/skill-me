#!/usr/bin/env python3
"""Measure which way water moves on screen between two captures of the same view.

  flow_direction.py first.png second.png x0,y0,x1,y1 [--max-shift 300]

The box should cover water only, with the flow running roughly horizontally on screen. Per-row means are
removed so static depth gradients do not dominate. Prints the best horizontal shift in pixels
(+ = content moved right) and its correlation.

For a reliable result, capture with the water opaque, reflection at maximum and twinkles/foam off (a static
riverbed seen through translucent water pins the peak at 0). Take the captures at least 1 s of game time apart
on the real game view, then restore the material.
Requires numpy and pillow.
"""
import argparse

import numpy as np
from PIL import Image


def best_shift(first, second, box, max_shift):
    x0, y0, x1, y1 = box
    a = np.asarray(Image.open(first).convert("L")).astype(np.float32)[y0:y1, x0:x1]
    b = np.asarray(Image.open(second).convert("L")).astype(np.float32)[y0:y1, x0:x1]
    a -= a.mean(axis=1, keepdims=True)
    b -= b.mean(axis=1, keepdims=True)
    best = (0, -1.0)
    for shift in range(-max_shift, max_shift + 1):
        left = a[:, : a.shape[1] - shift] if shift >= 0 else a[:, -shift:]
        right = b[:, shift:] if shift >= 0 else b[:, : b.shape[1] + shift]
        if left.shape[1] < 32:
            continue
        score = float((left * right).mean() / (left.std() * right.std() + 1e-6))
        if score > best[1]:
            best = (shift, score)
    return best


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("first")
    parser.add_argument("second")
    parser.add_argument("box", help="x0,y0,x1,y1")
    parser.add_argument("--max-shift", type=int, default=300)
    args = parser.parse_args()
    shift, score = best_shift(args.first, args.second, [int(v) for v in args.box.split(",")], args.max_shift)
    direction = "right" if shift > 0 else "left" if shift < 0 else "none (check time gap / static bed)"
    print(f"shift {shift:+d} px ({direction}), correlation {score:.3f}")


if __name__ == "__main__":
    main()
