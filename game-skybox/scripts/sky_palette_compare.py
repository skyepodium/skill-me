#!/usr/bin/env python3
"""Compare the sky of a reference screenshot with game captures.

Each argument is IMAGE:SKY_FRACTION, where SKY_FRACTION is the share of the image height
(from the top) that is sky, e.g. `ref.png:0.37 capture.png:0.40`. Crop out UI and subtitles
from that band before measuring, or pass a smaller fraction.

Reports per image: sky share of the frame, mean saturation/value of blue sky pixels, cloud
cover (low-saturation bright pixels), cloud brightness, and top-vs-bottom band saturation
(the horizon-to-zenith gradient). Use it to turn "the sky looks dull/rainy" into numbers.

  sky_palette_compare.py reference.webp:0.37 before.png:0.19 after.png:0.40
Requires numpy and pillow (e.g. `uv run --with numpy --with pillow sky_palette_compare.py ...`).
"""
import argparse

import numpy as np
from PIL import Image

CLOUD_MAX_SATURATION = 0.2
CLOUD_MIN_VALUE = 0.8
BAND_SHARE = 1 / 6


def to_hsv(rgb):
    maximum = rgb.max(axis=-1)
    minimum = rgb.min(axis=-1)
    saturation = np.where(maximum > 0, (maximum - minimum) / np.maximum(maximum, 1e-6), 0)
    return saturation, maximum


def describe(path, sky_fraction):
    pixels = np.asarray(Image.open(path).convert("RGB")).astype(np.float32) / 255.0
    sky_rows = max(1, int(pixels.shape[0] * sky_fraction))
    sky = pixels[:sky_rows]
    saturation, value = to_hsv(sky)
    cloud = (saturation < CLOUD_MAX_SATURATION) & (value > CLOUD_MIN_VALUE)
    blue = ~cloud
    band = max(1, int(sky_rows * BAND_SHARE))

    def band_saturation(rows):
        s, v = to_hsv(rows)
        mask = s >= CLOUD_MAX_SATURATION
        return s[mask].mean() if mask.any() else float("nan")

    return {
        "sky%": sky_fraction * 100,
        "skyS": saturation[blue].mean(),
        "skyV": value[blue].mean(),
        "cloud%": cloud.mean() * 100,
        "cloudV": value[cloud].mean() if cloud.any() else float("nan"),
        "topS": band_saturation(sky[:band]),
        "bottomS": band_saturation(sky[-band:]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("images", nargs="+", metavar="IMAGE:SKY_FRACTION")
    args = parser.parse_args()
    print(f"{'image':<28} {'sky%':>5} {'skyS':>5} {'skyV':>5} {'cloud%':>6} {'cloudV':>6} {'topS':>5} {'botS':>5}")
    for item in args.images:
        path, _, fraction = item.rpartition(":")
        if not path:
            parser.error(f"expected IMAGE:SKY_FRACTION, got {item}")
        row = describe(path, float(fraction))
        name = path.rsplit("/", 1)[-1][:28]
        print(f"{name:<28} {row['sky%']:5.0f} {row['skyS']:5.2f} {row['skyV']:5.2f} {row['cloud%']:6.0f} "
              f"{row['cloudV']:6.2f} {row['topS']:5.2f} {row['bottomS']:5.2f}")


if __name__ == "__main__":
    main()
