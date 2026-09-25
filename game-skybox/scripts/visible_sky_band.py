#!/usr/bin/env python3
"""Report which sky elevations a game camera can actually see.

Give either the camera's downward look angle directly (--look-down) or an orbit/chase
rig (--orbit-distance, --orbit-height, --pitch) that LookAt()s its focus point.
Optionally pass --band LOW HIGH (degrees) to test whether sky content placed in that
elevation band is ever on screen.

Example (QB-001 chase camera, FOV 58, 16:9, pitch -15..55):
  visible_sky_band.py --fov 58 --aspect 1.777 --orbit-distance 3 --orbit-height 0.65 \
      --pitch -15 55 5 --band 7 38
"""
import argparse
import math


def look_down_from_orbit(pitch_deg, distance, height):
    # Camera = focus + up*height + Euler(pitch, yaw) * back*distance, then LookAt(focus).
    pitch = math.radians(pitch_deg)
    rise = height + distance * math.sin(pitch)
    run = distance * math.cos(pitch)
    return math.degrees(math.atan2(rise, run))


def screen_edges(look_down_deg, vfov_deg, aspect):
    half_v = math.radians(vfov_deg / 2)
    top_center = -look_down_deg + vfov_deg / 2
    # Top corners sit slightly higher/lower than the top centre because of the wider ray.
    forward_elev = math.radians(-look_down_deg)
    tan_h = math.tan(half_v) * aspect
    up_y = math.cos(forward_elev)
    fwd_y = math.sin(forward_elev)
    corner_y = fwd_y + math.tan(half_v) * up_y
    corner_len = math.sqrt(1 + math.tan(half_v) ** 2 + tan_h ** 2)
    top_corner = math.degrees(math.asin(max(-1, min(1, corner_y / corner_len))))
    bottom_center = -look_down_deg - vfov_deg / 2
    return top_center, top_corner, bottom_center


def sky_fraction(top_center, vfov_deg):
    # Rough share of screen rows above the geometric horizon (ignores terrain occlusion).
    if top_center <= 0:
        return 0.0
    return min(1.0, top_center / vfov_deg)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fov", type=float, required=True, help="vertical field of view in degrees")
    parser.add_argument("--aspect", type=float, default=16 / 9)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--look-down", type=float, nargs="+", help="camera downward angle(s) in degrees")
    group.add_argument("--pitch", type=float, nargs=3, metavar=("MIN", "MAX", "STEP"), help="orbit pitch sweep")
    parser.add_argument("--orbit-distance", type=float)
    parser.add_argument("--orbit-height", type=float, default=0.0)
    parser.add_argument("--band", type=float, nargs=2, metavar=("LOW", "HIGH"), help="sky content elevation band")
    args = parser.parse_args()

    rows = []
    if args.look_down:
        rows = [(None, value) for value in args.look_down]
    else:
        if args.orbit_distance is None:
            parser.error("--pitch needs --orbit-distance")
        low, high, step = args.pitch
        value = low
        while value <= high + 1e-9:
            rows.append((value, look_down_from_orbit(value, args.orbit_distance, args.orbit_height)))
            value += step

    print(f"{'pitch':>6} {'lookDown':>8} {'topCtr':>7} {'topCnr':>7} {'sky%':>5}  band")
    misses = 0
    for pitch, look_down in rows:
        top_center, top_corner, _ = screen_edges(look_down, args.fov, args.aspect)
        sky = sky_fraction(top_center, args.fov)
        verdict = ""
        if args.band:
            low, high = args.band
            visible_top = max(top_center, top_corner)
            if visible_top <= 0:
                verdict = "no sky on screen"
            elif visible_top < low:
                verdict = "MISS: sky visible but band above screen"
                misses += 1
            else:
                verdict = f"visible {low:.1f}..{min(high, visible_top):.1f}"
        label = "-" if pitch is None else f"{pitch:.1f}"
        print(f"{label:>6} {look_down:8.1f} {top_center:7.1f} {top_corner:7.1f} {sky * 100:4.0f}%  {verdict}")
    if args.band:
        print(f"\n{misses} view(s) show sky but none of the band.")


if __name__ == "__main__":
    main()
