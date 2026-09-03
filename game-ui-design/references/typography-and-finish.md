# Typography and Finish

Use this reference to turn a game UI direction into measurable typography, spacing, alignment,
and surface decisions. The values below are starting checkpoints, not universal platform laws.
Judge them on the actual display at the intended viewing distance.

## Start from the display

Record the reference resolution, physical display class, viewing distance, input method, and
locales before setting type. A 24 px label on a handheld screen and a television does not have
the same apparent size.

For a 1920×1080 landscape reference viewed at desktop or handheld distance, these are useful
first-pass ranges:

| Role | Typical use | Starting size |
| --- | --- | ---: |
| Micro | timestamps, secondary abbreviations, noncritical hints | 16–18 px |
| Metadata | counts, resource captions, secondary status | 18–22 px |
| Body / label | menu items, objectives, ordinary controls | 22–28 px |
| Primary action | card names, important buttons, active state | 28–38 px |
| Section | screen or group headings | 36–48 px |
| Display | rare event, reward, or mode title | 48–72 px |

Scale from the reference resolution as a starting point, then correct optically. At a 1280×720
reference, do not let critical interactive text fall below roughly 16–18 px merely because a
mathematical scale says so. Micro text may be smaller only when it is genuinely optional.

Use no more roles than the screen needs. A five-role scale applied consistently is usually more
polished than many one-off sizes. Create contrast with role, weight, width, value, and placement;
do not solve every hierarchy problem by making the text larger.

## CJK and numeric handling

- Test the actual Korean, Japanese, or Chinese strings. CJK glyphs often need more apparent size
  and vertical room than Latin captions in the same nominal font size.
- Use approximately 1.2–1.4 line height for multi-line CJK UI copy unless the chosen face proves
  otherwise. Do not apply Latin-style wide tracking to Korean sentences.
- Reserve condensed or decorative faces for short headings and numbers. Use a highly legible UI
  face for objectives, menus, and instructions.
- Use at most two families unless a third numeric/display face has a clear systemic role.
- Prefer tabular numerals for currencies, timers, levels, damage, and changing aligned values.
- Define fallback fonts with compatible width and baseline metrics; missing glyph fallback should
  not visibly change weight or line height.

## Legibility over art

Text placed on game art needs a controlled local backing: a value gradient, shape, outline, or
shadow belonging to the visual grammar. Avoid stacking all four.

At a 1080p reference, a 1–2 px outline or restrained shadow is a reasonable first test for
ordinary UI text; busy pixel art or broadcast-distance viewing may require more. Inspect the
result at 100% scale. Fractional positioning, soft resampling, and thin light text can destroy
clarity even when nominal contrast passes.

For pixel-art games, align UI geometry and bitmap text to the chosen integer render scale.
Either use a legible bitmap-compatible CJK face or deliberately contrast crisp vector UI with
the world; do not accidentally mix soft web-like cards, fractional borders, and pixel scenery.

## Spacing and alignment

Derive a base unit from the reference canvas. `short edge / 135` gives about 8 px at 1080p and
about 5 px at 720p, which is a useful initial unit `u` for landscape UI.

- tight icon/text gap: `1u`;
- ordinary internal gap: `1–2u`;
- panel padding: `2–3u`;
- separation between semantic groups: `3–5u`;
- safe edge margin: commonly `3–6u`, then reconcile with platform safe areas;
- touch controls: commonly at least `6–8u` in both dimensions at the reference scale.

Do not cargo-cult these values. Round them to the engine's render constraints and adjust for the
actual input target. What matters is that the screen uses a small repeatable spacing family.

Draw the alignment map before polishing:

- outer safe edges;
- major vertical and horizontal axes;
- shared card edges and gutters;
- icon box sizes;
- text baselines;
- repeated control heights;
- optical corrections for irregular icons and character silhouettes.

A clean screen usually has fewer invisible axes than it appears to. Elements that are almost
aligned look less finished than elements that are deliberately offset.

## Character art and content panels

When a character or environment is the emotional anchor, reserve a stable stage for its face,
pose, weapon, and animation envelope. Route dense navigation around the silhouette rather than
placing unrelated rectangles wherever empty pixels remain.

For portrait cards and collection grids:

- fix crop logic, eye-line bands, card aspect ratio, gutters, and metadata zones;
- keep names, levels, rarity, and faction marks on shared baselines;
- use faction or rarity color in controlled semantic areas rather than tinting every surface;
- dim or simplify the background enough that the grid owns the reading plane.

## Surface and component finish

Choose one primary container family and at most a few deliberate variants. Define corner or cut
geometry, border weight, fill opacity, selected edge, shadow or depth rule, and how the surface
meets the world art. Buttons of equal importance should share a skeleton before their content
changes.

Polish in this order:

1. hierarchy and content grouping;
2. type roles and actual sizes;
3. grid, padding, baselines, and hit areas;
4. component silhouette and selected/disabled states;
5. palette, surfaces, icons, and illustration integration;
6. motion and decorative effects.

If a screen still looks unfinished after step 3, adding glow or texture will not repair it.

## Comparison loop

When reference images are supplied, extract relationships rather than copying assets:

- ratio of heading to body text;
- number and ownership of screen zones;
- panel padding relative to text height;
- recurring axes, gutters, and card crops;
- how the background is quieted behind information;
- where high saturation, strong contrast, and motion are permitted.

Render the current and revised screen at the same state and resolution. Compare them at full
size and as a small thumbnail. The thumbnail should still reveal the intended focal order; the
full-size view should reveal consistent baselines, padding, and text rendering. Record concrete
remaining defects instead of declaring the result "clean" or "polished."
