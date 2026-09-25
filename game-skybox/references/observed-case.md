# Observed cases: QB-001 meadow

## Case 1: clouds invisible from the default view

**Symptom:** the user reported that clouds disappear at some angles and look textureless.

**What the code did:** a procedural skybox drew 12 clouds as max-blended Gaussian ellipses, placed by longitude with centre heights `dir.y` 0.23–0.58 (elevation about 14–35°, visible from about 7° up). It used one flat colour and no `_Time`.

**What the camera saw:** the chase rig (orbit distance 3, height offset 0.65, pitch −15..55, FOV 58°) looks down about 20° at the default pitch of 8°, so the screen top sits at 9.1° elevation. A CPU replica of the shader under that camera showed 0% cloud cover at all 12 yaws for pitches 8–17°. Sky still filled 2–17% of the screen at those pitches. The replica matched the user's screenshot.

**The first analysis failed.** It reported that a skybox "is implemented" by reading the code. It never computed what the player sees, so it missed the placement mismatch completely.

**Fix:**
- Project the clouds onto a plane.
- Use baked Perlin-Worley noise for the shape and edges.
- Shade in two toon tones from a second sample toward the sun.
- Add wind.

Afterwards the coverage sweep measured 4–27% of visible sky at every pitch and yaw, and Game-view captures at 6 angles plus a wind probe confirmed the result.

**Lessons:**
1. A cloud band can exist in the shader and still never be on screen. Always compute the visible sky band before placing sky content.
2. A chase camera that frames the character sees mostly 0–30° of elevation. Horizon-near sky is where the content must be dense.
3. A band edge (where alpha barely starts) overstates visibility. Test actual coverage, not the band's geometric extent.

## Case 2: "the sky is boring and looks like rain" next to a reference

**Symptom:** the user compared the game with a bright Arceus-style tutorial frame. Their words: "our sky is dull, like it is about to rain."

**Measured** with `sky_palette_compare.py`:

| | Reference | Game before |
|---|---|---|
| Sky share of frame | 37% | 19% |
| Sky saturation | 0.44 | 0.24 |
| Cloud cover | 20% | 15% |
| Cloud brightness | 0.99 | 0.93 |

**Cause:**
- The camera looked down about 20°, so the screen showed only 0–9° of elevation.
- The gradient `smoothstep(-0.08, 0.85, dir.y)` mixes in at most 15% of the zenith colour over that range, so almost all the visible sky was the pale horizon colour.
- The grey-blue cloud shade, covering most of each cloud, added the rainy tone.

The cloud shapes were not the main problem.

**Fix:**
- Lower the camera pitch from 8° to −5° (about 7° look-down).
- Set `_GradientHeight` to 0.42 and use a more saturated horizon/zenith palette.
- Add a cluster mask so big, small and open areas mix.
- Raise the horizon bias to 0.3 so horizon clouds stay round.
- Shrink the shade and make it lighter.

Result: sky share 40%, saturation 0.51, cloud cover about 18–20%, cloud brightness 0.97. No cloudless view appeared in six Game-view angles or in the numeric sweep.

**Lessons:**
1. Turn "dull" into numbers against the reference before touching the clouds.
2. Sky share is a camera property. Fix the framing first and re-measure the visible band.
3. The gradient has to finish inside the visible band.
4. After the sky matched, the remaining gap to the reference was composition: flat ground, a horizontal river, no framing and a ruler-straight horizon. That belongs to terrain, not the sky.
