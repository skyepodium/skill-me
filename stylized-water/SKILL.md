---
name: stylized-water
description: Build or fix stylized game water (rivers, streams, shallow seas) that reads clear, emerald and clean on mobile, without a depth or opaque texture. Use when water looks flat, neon or plastic, when matching a reference's water colour and sparkle, when adding foam, ripples or translucency, or when choosing a mobile-friendly water technique in Unity URP.
---

# Stylized Water

Clear stylized water comes from a few layers:
- depth colour (emerald shallows → clear blue)
- translucency over a painted bed
- a sky-coloured Fresnel reflection
- flowing ripples
- a few sparkles
- broken foam where water meets things

The mobile question is how to get **depth** without paying for the camera depth texture. Answer it first.

## 1. Measure the reference and the current water

Capture the current water at the views players use:
- the default camera
- a high view down at the water
- a view along the water

Run [scripts/water_palette_compare.py](scripts/water_palette_compare.py) on the same zones in the reference and in the captures: shallows at the edge, the body, grazing/far water. It reports hue, saturation, value, RGB and the share of twinkle pixels.

**Done when:** a table lists each zone for the reference and the current water, and each gap is named (colour, translucency, reflection, sparkle, foam).

## 2. Choose the depth source

| Depth source | Use when | Cost |
|---|---|---|
| **Analytic from known geometry** (e.g. distance from a straight river's centre line) | The channel shape is known in code | Free |
| Baked distance-to-shore texture or per-vertex shore distance | Curved rivers, lakes, fixed coastlines | One texture read or none |
| Camera depth texture (scene depth − surface depth) | The project already enables it, or foam must hug arbitrary moving objects | A depth pre-pass/copy: significant on low-end mobile |

Prefer the first two on mobile. Reject off-the-shelf water shaders that silently require the depth and opaque textures unless the project already pays for them.

**Done when:** the chosen source and the rejected ones are stated with their cost for the target device.

## 3. Build the surface, the bed and the ripples

Start from [water-shader.md](references/water-shader.md), and from [riverbed-and-ripples.md](references/riverbed-and-ripples.md) for the riverbed snippet and the ripple normal map.

- Copy the sky's horizon and zenith colours into the water material from the sky material, so the two always match (single source).
- Keep channel width, water height and foam-box sizes in one layout constant shared by the terrain, water and gameplay code.
- Feed moving-object foam (boats, platforms) from script with explicit references, not lookups by name.
- Set the flow direction (`_FlowDirection`, world xz) from the default camera's screen axes so the water runs the way the player expects on screen.

**Done when:**
- The shader compiles with no errors (check `ShaderUtil.ShaderHasError` in Unity).
- The water is translucent, and the bed shows at the edges.
- No new render textures are enabled.

## 4. Tune against the numbers

Use [tuning.md](references/tuning.md). Change one group per pass, capture the same views, and re-measure the same zones. When the camera faces away from the sun, a physically correct glint gives no sparkle; add view-independent twinkles.

Compare like with like: a narrow river's body against the reference's near water, not against an open sea's horizon.

**Done when:**
- Shallows and body hues are within about ±10° of the reference, and value within about ±0.08.
- Twinkles cover roughly 0.5–2 % of water pixels.
- Foam reads as broken lines, not a painted stroke.
- The kept values are copied into the shader defaults.

## 5. Verify in the game

For Unity CLI capture tips, see [game-skybox/references/unity-verification.md](../game-skybox/references/unity-verification.md). Remember that an unfocused editor stops time, so ripples and flow will not move.

- Capture the three views after the final pass. Also capture a moving object (boat) to see its foam follow.
- Verify the on-screen flow direction by measurement:
  1. Make the water opaque with maximum reflection and no twinkles or foam; a translucent surface lets the static bed dominate.
  2. Capture the real game view twice, at least 1 s of game time apart. Manual camera renders may not advance the shader time.
  3. Cross-correlate a water strip horizontally with [scripts/flow_direction.py](scripts/flow_direction.py).
  4. Restore the material values afterwards.
- Record draw calls, SetPass calls and triangles before and after.
- Record which checks did not run: device frame time, hands-on play.

**Done when:**
- The before/after measurement table exists.
- The captures show every layer (depth colour, translucency, reflection, ripples, sparkle, foam).
- The report separates measured, inferred and unchecked items.

For a worked example, see [observed-case.md](references/observed-case.md).
