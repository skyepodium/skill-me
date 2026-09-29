"""Flatten a painted albedo texture for toon shading (2026-09-30).

Purchased textures paint light into the albedo (shading gradients, metal reflections, fabric folds, hair shine). On a
toon shader that light is drawn twice and the result reads as realistic 3D. This keeps the colour regions and the line
art and removes the painted light, so the toon shader does all the shading:

1. Line art: pixels much darker than their neighbourhood keep their original colour.
2. Colour regions: a floating-range flood fill, so a painted gradient (small steps) stays one region and line art
   or part borders (sharp steps) end it.
3. Each region is filled with one colour: the median hue/chroma and a lit lightness (the
   LIT_PERCENTILE of its pixels), since the toon shader darkens the shaded side itself.

Usage: python3 flatten_albedo.py <source.png> <output.png> [--step S] [--lit P] [--drop-highlights] [--bands N] [--preview out.png]
The source is read, never written. Alpha is kept.
"""
import argparse
import cv2
import numpy as np

LINE_WINDOW = 21            # px (at 2048): neighbourhood for the line test
LINE_DROP = 40              # Lab L (0-255) below the neighbourhood median counts as line art
LINE_MAX_L = 110            # and only if it is dark in itself
MIN_REGION_PX = 40          # smaller islands keep their smoothed colour instead of their own fill
SMOOTH_SPATIAL, SMOOTH_COLOUR = 8, 18   # mean-shift first: removes texture noise, keeps edges
HIGHLIGHT_MAX_AREA_PX = 6000   # --drop-highlights: largest painted shine region (px at 2048)
HIGHLIGHT_LIFT_L = 18       # and how much brighter (Lab L) than its surroundings it must be
HIGHLIGHT_RING_PX = 4
BAND_RATIO_EDGES = (0.9, 0.78, 0.66)   # --bands: source/fill lightness ratios where the next darker band starts
BAND_DARKNESS = (1.0, 0.84, 0.7, 0.58)  # lightness of each band against the region fill
BAND_SMOOTH_PX = 5
SEED_STEP = 6               # px between flood-fill seeds; unfilled pixels keep their colour


def flatten(bgr, step_tolerance, lit_percentile, drop_highlights=False, bands=1):
    height, width = bgr.shape[:2]
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    lightness = lab[..., 0]

    local = cv2.medianBlur(lightness.astype(np.uint8), LINE_WINDOW).astype(np.float32)
    line = (lightness < local - LINE_DROP) & (lightness < LINE_MAX_L)

    # Regions by floating-range flood fill on the smoothed image: neighbour-to-neighbour steps below the tolerance
    # join, so a painted gradient is one region while line art and part borders (sharp steps) stop it. (k-means on
    # colour split gradients into bands and read as camouflage, 2026-09-30 first try.)
    smooth = cv2.pyrMeanShiftFiltering(bgr, SMOOTH_SPATIAL, SMOOTH_COLOUR)
    regions = np.zeros((height, width), np.int32)
    blocked = np.zeros((height + 2, width + 2), np.uint8)
    blocked[1:-1, 1:-1][line] = 1
    tolerance = (step_tolerance,) * 3
    flags = 4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8)
    next_region = 1
    for y in range(0, height, SEED_STEP):
        for x in range(0, width, SEED_STEP):
            if blocked[y + 1, x + 1]:
                continue
            mask = np.zeros_like(blocked)
            mask[blocked > 0] = 1
            cv2.floodFill(smooth, mask, (x, y), 0, tolerance, tolerance, flags)
            region = mask[1:-1, 1:-1] == 255
            regions[region] = next_region
            blocked[1:-1, 1:-1][region] = 1
            next_region += 1

    out_lab = lab.copy()
    for region_id in range(1, next_region):
        region = regions == region_id
        if int(region.sum()) < MIN_REGION_PX:
            continue
        pixels = lab[region]
        out_lab[region] = (np.percentile(pixels[:, 0], lit_percentile), np.median(pixels[:, 1]), np.median(pixels[:, 2]))
    if drop_highlights:
        drop_painted_highlights(out_lab, regions, next_region, line)
    if bands > 1:
        band_by_lightness(out_lab, cv2.cvtColor(smooth, cv2.COLOR_BGR2LAB).astype(np.float32), bands)
    out_lab[line] = lab[line]
    out = cv2.cvtColor(np.clip(out_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    return out, line, next_region - 1


def band_by_lightness(out_lab, smooth_lab, bands):
    """Rocks (2026-09-30): one flat colour per region lost the cracks and facets and read as a smooth lump. Here each
    pixel keeps its region colour but steps darker by how much darker the (smoothed) source is than the region fill,
    in a few flat bands, like a painted stone. The band map is median-filtered so single texels do not speckle."""
    ratio = smooth_lab[..., 0] / np.maximum(out_lab[..., 0], 1.0)
    edges = BAND_RATIO_EDGES[:bands - 1]
    band = np.zeros(ratio.shape, np.uint8)
    for index, edge in enumerate(edges):
        band[ratio < edge] = index + 1
    band = cv2.medianBlur(band, BAND_SMOOTH_PX)
    darkness = np.array(BAND_DARKNESS[:bands], np.float32)
    out_lab[..., 0] *= darkness[band]


def drop_painted_highlights(out_lab, regions, region_count, line):
    """Hair: small regions clearly brighter than the ring around them are painted shine (angel ring flecks, highlight
    strokes); they take the ring's colour. Clothes keep theirs (rivets, gems)."""
    kernel = np.ones((HIGHLIGHT_RING_PX * 2 + 1,) * 2, np.uint8)
    for region_id in range(1, region_count + 1):
        region = regions == region_id
        area = int(region.sum())
        if area == 0 or area > HIGHLIGHT_MAX_AREA_PX:
            continue
        ring = cv2.dilate(region.astype(np.uint8), kernel).astype(bool) & ~region & ~line
        if not ring.any():
            continue
        surround = np.median(out_lab[ring], axis=0)
        if out_lab[region][0, 0] - surround[0] > HIGHLIGHT_LIFT_L:
            out_lab[region] = surround


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('output')
    parser.add_argument('--step', type=int, default=4, help='largest neighbour step (per BGR channel) inside a region')
    parser.add_argument('--lit', type=float, default=65)
    parser.add_argument('--drop-highlights', action='store_true', help='hair: paint small bright shine regions with their surroundings')
    parser.add_argument('--bands', type=int, default=1, help='rocks: 2-4 flat lightness bands inside each region (cracks, facets)')
    parser.add_argument('--preview')
    args = parser.parse_args()

    image = cv2.imread(args.source, cv2.IMREAD_UNCHANGED)
    if image is None:   # OpenCV reads no TGA (common for vendor foliage); Pillow does
        from PIL import Image
        with Image.open(args.source) as source:
            rgba = np.array(source.convert('RGBA'))
        image = cv2.cvtColor(rgba, cv2.COLOR_RGBA2BGRA)
    alpha = image[..., 3] if image.ndim == 3 and image.shape[2] == 4 else None
    bgr = image[..., :3] if image.ndim == 3 else cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    flat, line, count = flatten(bgr, args.step, args.lit, args.drop_highlights, args.bands)
    result = np.dstack([flat, alpha]) if alpha is not None else flat
    if image.dtype != np.uint8:
        raise SystemExit('only 8-bit textures: ' + args.source)
    cv2.imwrite(args.output, result)
    print(f'{args.output}: {bgr.shape[1]}x{bgr.shape[0]}, {count} regions, line pixels {line.mean() * 100:.1f}%')
    if args.preview:
        side = np.hstack([cv2.resize(bgr, (1024, 1024)), cv2.resize(flat, (1024, 1024))])
        cv2.imwrite(args.preview, side)


if __name__ == '__main__':
    main()
