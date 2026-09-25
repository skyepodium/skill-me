---
name: worley-cloud-noise
description: Generate game sky clouds from tileable Perlin-Worley (워리 노이즈) noise projected on a cloud plane, with stylized toon shading and wind. Use when clouds need texture, puffiness, motion or coverage fixes, when implementing Worley/cellular noise for skies, or when tuning cloud coverage, edges or shade. Also used by game-skybox when it picks a 2D cloud layer.
---

# Worley Cloud Noise

Build clouds as one **cloud plane**: each view ray is projected onto a flat layer above the world, and density comes from baked **Perlin-Worley** noise. The plane gives coverage at every angle and perspective toward the horizon. The noise gives puffy lobes and cauliflower edges.

If the camera's visible sky band is not known yet, measure it first with the `game-skybox` skill (step 1). Clouds tuned outside the band the player sees are invisible work.

## 1. Bake tileable noise

Implement the baker from [noise-baker.md](references/noise-baker.md) as an editor/offline tool.

- R channel: Perlin-Worley shape.
- G channel: inverted Worley fBm detail.
- 256², wrapped lattice on every octave, normalized to 0..1.

Import the result linear (sRGB off), Repeat, mipmapped and uncompressed, and assign it to the sky material from the same tool.

**Done when:** the PNG tiles without a visible seam (check a 2×2 tiled view), both channels span 0..1, and the material references it.

## 2. Shade the cloud plane

Start from [cloud-layer-shader.md](references/cloud-layer-shader.md). It is written for URP; its porting notes cover Built-in and other engines.

- plane projection `dir.xz / (dir.y + bias) * scale`
- a low-frequency cluster mask that raises coverage in some regions and lowers it in others, so big masses, scattered small clouds and open blue sky appear together
- density = shape − (1 − detail) × erosion
- a crisp `smoothstep` edge at `1 − coverage`
- a second density sample toward the sun that splits a lit rim from a shade core (two-tone toon)
- `_Time` wind with the detail layer moving faster than the shape
- horizon fade and haze into the horizon colour

**Done when:** the shader compiles without errors in the target pipeline and the sky shows clouds in the editor.

## 3. Tune in the game view

Tune against [tuning.md](references/tuning.md) at the player's default camera. Change one parameter group per pass, capture each pass, and name what the capture showed before choosing the next change. When the user gives a reference image, measure the reference and each pass with `game-skybox/scripts/sky_palette_compare.py`. A "dull" or "rainy" complaint is usually the visible band and the gradient, not the clouds; check the symptom table first. Copy the kept values back into the shader property defaults.

**Done when:** the kept pass is chosen from captures, not from numbers alone, and the user's art direction (stylized by default in that file) is visible: crisp edges, a lit rim with a shade core, mixed cloud sizes, no confetti specks, no shade that reads as holes. With a reference, sky saturation and cloud cover are within about ±0.1 and ±5 percentage points of it.

## 4. Prove coverage and motion

- Run [scripts/cloud_coverage.py](scripts/cloud_coverage.py) with the final values, including the cluster mask arguments, over every look-down angle that shows sky and at least 12 yaws. It must report 0 holes.
- Capture a fixed sky camera twice, several seconds apart, and measure the pixel difference to prove the wind works. In Unity the editor must be focused or time stops, as noted in [game-skybox/references/unity-verification.md](../game-skybox/references/unity-verification.md).
- Update the project's docs or agent notes wherever they describe the sky.

**Done when:** the numeric sweep, the angle captures and the motion probe all exist, and the report names which checks ran and which did not.
