#!/usr/bin/env python3
"""Measure how much of the visible sky a plane-projected noise cloud layer covers.

Replicates the reference shader in references/cloud-layer-shader.md on the CPU:
  planePoint = dir.xz / (dir.y + horizonBias) * planeScale
  density    = shape(planePoint) - (1 - detail(planePoint * detailTiling)) * erosion
  body       = smoothstep(1 - coverage, 1 - coverage + softness, density) * fade(dir.y)
Reads the baked noise PNG (R = shape, G = detail, Unity UV convention: v=0 is the bottom row).

For each camera look-down angle and yaw it prints the share of above-horizon pixels
whose cloud alpha exceeds --alpha-threshold. Any 0% row with visible sky is a coverage hole.

Example:
  cloud_coverage.py MeadowCloudNoise.png --fov 58 --aspect 1.777 \
      --look-down -2.5 3.5 9.7 19.8 26.2 --coverage 0.44 --plane-scale 0.15
Requires numpy and pillow (e.g. `uv run --with numpy --with pillow cloud_coverage.py ...`).
"""
import argparse
import math

import numpy as np
from PIL import Image


def load_noise(path):
    pixels = np.asarray(Image.open(path).convert("RGBA")).astype(np.float32) / 255.0
    if pixels.shape[0] != pixels.shape[1]:
        raise SystemExit(f"expected a square tileable texture, got {pixels.shape[1]}x{pixels.shape[0]}")
    return pixels


def sample_bilinear(noise, uv, channel):
    size = noise.shape[0]
    x = np.mod(uv[..., 0], 1.0) * size - 0.5
    y = (size - 1) - (np.mod(uv[..., 1], 1.0) * size - 0.5)
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    fx = x - x0
    fy = y - y0

    def texel(row, col):
        return noise[np.mod(row, size), np.mod(col, size), channel]

    top = texel(y0, x0) * (1 - fx) + texel(y0, x0 + 1) * fx
    bottom = texel(y0 + 1, x0) * (1 - fx) + texel(y0 + 1, x0 + 1) * fx
    return top * (1 - fy) + bottom * fy


def smoothstep(edge0, edge1, value):
    t = np.clip((value - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def cloud_alpha(noise, directions, args, time_seconds):
    height = directions[..., 1]
    plane = directions[..., [0, 2]] / (np.maximum(height, 1e-4) + args.horizon_bias)[..., None] * args.plane_scale
    wind = np.array(args.wind) * time_seconds
    shape = sample_bilinear(noise, plane + wind, 0)
    detail = sample_bilinear(noise, plane * args.detail_tiling + wind * args.detail_wind, 1)
    density = shape - (1 - detail) * args.erosion
    edge = 1 - args.coverage
    body = smoothstep(edge, edge + args.softness, density)
    fade = smoothstep(0.0, args.horizon_fade, height)
    return np.where(height > 0, body * args.opacity * fade, 0.0)


def view_directions(look_down_deg, yaw_deg, vfov_deg, aspect, width):
    height_px = max(2, int(width / aspect))
    look = math.radians(-look_down_deg)
    yaw = math.radians(yaw_deg)
    forward = np.array([math.cos(look) * math.sin(yaw), math.sin(look), math.cos(look) * math.cos(yaw)])
    right = np.cross([0.0, 1.0, 0.0], forward)
    right /= np.linalg.norm(right)
    up = np.cross(forward, right)
    tan_half = math.tan(math.radians(vfov_deg / 2))
    rows, cols = np.mgrid[0:height_px, 0:width]
    screen_x = (2 * (cols + 0.5) / width - 1) * tan_half * aspect
    screen_y = (1 - 2 * (rows + 0.5) / height_px) * tan_half
    rays = forward + screen_x[..., None] * right + screen_y[..., None] * up
    return rays / np.linalg.norm(rays, axis=-1, keepdims=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("noise_png")
    parser.add_argument("--fov", type=float, required=True, help="vertical FOV in degrees")
    parser.add_argument("--aspect", type=float, default=16 / 9)
    parser.add_argument("--look-down", type=float, nargs="+", required=True, help="camera downward angles (deg)")
    parser.add_argument("--yaw-count", type=int, default=12)
    parser.add_argument("--time", type=float, default=0.0, help="shader time in seconds")
    parser.add_argument("--coverage", type=float, default=0.44)
    parser.add_argument("--softness", type=float, default=0.02)
    parser.add_argument("--plane-scale", type=float, default=0.15)
    parser.add_argument("--horizon-bias", type=float, default=0.1)
    parser.add_argument("--detail-tiling", type=float, default=2.7)
    parser.add_argument("--erosion", type=float, default=0.26)
    parser.add_argument("--horizon-fade", type=float, default=0.025)
    parser.add_argument("--opacity", type=float, default=0.95)
    parser.add_argument("--wind", type=float, nargs=2, default=(0.004, 0.0015))
    parser.add_argument("--detail-wind", type=float, default=1.6)
    parser.add_argument("--alpha-threshold", type=float, default=0.2)
    parser.add_argument("--width", type=int, default=320, help="evaluation resolution width")
    args = parser.parse_args()

    noise = load_noise(args.noise_png)
    yaws = [index * 360.0 / args.yaw_count for index in range(args.yaw_count)]
    holes = 0
    print(f"{'lookDown':>8} {'sky%':>5} {'minCov':>7} {'maxCov':>7}")
    for look_down in args.look_down:
        coverages = []
        sky_share = 0.0
        for yaw in yaws:
            directions = view_directions(look_down, yaw, args.fov, args.aspect, args.width)
            sky = directions[..., 1] > 0
            sky_share = sky.mean()
            if not sky.any():
                continue
            alpha = cloud_alpha(noise, directions, args, args.time)
            coverages.append((alpha[sky] > args.alpha_threshold).mean() * 100)
        if not coverages:
            print(f"{look_down:8.1f} {0:4.0f}%   no sky on screen")
            continue
        holes += sum(1 for value in coverages if value == 0)
        print(f"{look_down:8.1f} {sky_share * 100:4.0f}% {min(coverages):6.0f}% {max(coverages):6.0f}%")
    print(f"\n{holes} view(s) show sky with no cloud above alpha {args.alpha_threshold}.")


if __name__ == "__main__":
    main()
