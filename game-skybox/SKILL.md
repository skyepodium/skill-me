---
name: game-skybox
description: Design, fix, or review a game's sky starting from the visible sky band, meaning the elevations the game camera can actually see. Use for skybox/스카이박스 work, empty or wrong-looking skies ("각도에 따라 구름이 없다"), choosing cubemap vs procedural vs volumetric skies, or matching sky, fog and horizon. For generating cloud texture itself, use worley-cloud-noise.
---

# Game Skybox

A sky is judged from the player's camera, not from the shader source or a preview sphere. Every decision here starts from the **visible sky band**: the elevation range, per camera state, that actually reaches the screen.

## 1. Measure the visible sky band

- Read the camera rig: FOV, aspect, pitch limits, orbit distance and height offset, what it `LookAt`s, and any cutscene cameras. Record the default state the player starts in.
- Run [scripts/visible_sky_band.py](scripts/visible_sky_band.py) over the full pitch range. For existing sky content, pass its elevation band with `--band` so views that show sky but miss the content are flagged.
- If existing content is procedural, replicate its fragment math on the CPU under the same camera (see [observed-case.md](references/observed-case.md)). For clouds, [worley-cloud-noise/scripts/cloud_coverage.py](../worley-cloud-noise/scripts/cloud_coverage.py) does this.

**Done when:** you have a table of pitch → screen-top elevation and sky share. Every view that shows sky either shows sky content or is flagged as a hole. If the user sent a screenshot, it is reproduced by the numbers.

## 2. Choose the sky technique

Use [skybox-options.md](references/skybox-options.md). Choose with the visible band, the need for runtime change (wind, time of day), the art direction and the GPU budget. A chase or ground camera that sees 0–30° almost always wants a gradient plus a cloud layer projected on a plane. Choose volumetric only when the camera looks up or flies through clouds.

**Done when:** the choice and the rejected alternatives are each stated with the reason from the band, motion, art or cost.

## 3. Build and integrate

- Keep the sky base (gradient, horizon colour) in one shader or material. The horizon colour, fog colour and camera background must match.
- Put the dense sky content where the visible band is. For chase cameras that means the 0–15° elevations near the horizon.
- Keep generated assets (baked noise, cubemaps) separate from their generators, and validate required sky assets where the sky is applied.
- Keep shader property defaults equal to the tuned material values.

**Done when:** the project compiles, the shader has no errors, and a fresh setup path produces the same sky.

## 4. Verify in the target view

For Unity, follow [unity-verification.md](references/unity-verification.md). Everywhere else, use the engine's equivalent.

- Capture the default view, both pitch limits and opposite yaws. Include cutscene cameras that show sky.
- Re-run the numeric sweep from step 1 on the final values.
- For motion, capture a fixed sky camera at two times and measure the difference.
- If the user supplied a screenshot, reproduce it before and after the change.

**Done when:** the sweep shows no sky-without-content views, captures of every listed view exist, and the report separates numeric checks, captures and hands-on play. Name any of them that did not run.
