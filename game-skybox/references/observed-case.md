# Observed case: QB-001 meadow (clouds invisible from the default view)

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
