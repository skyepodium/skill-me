# Tuning the cloud layer

Tune in the target game view at the default camera, not in a material preview sphere. Change one group at a time, capture each pass, and when a reference image exists, measure both with `game-skybox/scripts/sky_palette_compare.py`.

## Parameters

| Property | Controls | Raise it when | Lower it when |
|---|---|---|---|
| `_GradientHeight` | `dir.y` where the zenith colour takes over | The upper visible sky is too dark or too uniform | Visible sky is pale/grey. Most common cause of a "rainy" sky with a low camera |
| `_HorizonColor`, `_ZenithColor` | Sky palette | — | — (match the reference's measured saturation, e.g. ~0.45–0.5 for a bright day) |
| `_CloudCoverage` | Base share of sky covered (threshold = `1 - coverage`) | Sky reads empty | Sky reads overcast or clouds merge into sheets |
| `_ClusterScale` | Size of the regions that get more or fewer clouds (relative to the plane) | Regions of dense or clear sky are too large | The mask reads as noise |
| `_CoverageVariation` | How much coverage swings between regions. 0 turns the mask off | All clouds look the same size and evenly spread | Some views end up cloudless |
| `_CloudPlaneScale` | Noise tiles per plane unit. Smaller values make bigger clouds | A few giant blobs dominate | Clouds look like scattered confetti |
| `_CloudHorizonBias` | Stretch limit near the horizon | Horizon clouds are squashed into flat streaks | Horizon clouds don't shrink with distance |
| `_DetailErosion` | How deeply the Worley detail notches the edges | Edges look like smooth airbrushed blobs | Clouds fragment into specks |
| `_DetailTiling` | Size of the notches relative to the shape | Notches look like big bites | Notches read as noise or shimmer |
| `_CloudEdgeSoftness` | Width of the alpha ramp at the edge. Small values give a crisp cel edge | Edges alias | Edges look blurry |
| `_ShadeThreshold` | How far inside the edge the shade tone starts | Shade covers most of the cloud (reads grey/rainy or like holes) | There is no shade band at all |
| `_ShadeOffset` | Width of the lit rim on the sun side | The lit rim is too thin | The whole cloud reads lit, or banding appears |
| `_CloudLitColor`, `_CloudShadeColor` | Cloud tones | — | The shade colour reads as a hole or rain cloud: move it toward the lit colour |
| `_WindVelocity` | Drift in tiles per second | Motion is invisible over ~10 s | Motion distracts during play |
| `_HorizonFadeHeight`, `_HorizonHaze*` | Fade into the horizon colour | A hard cloud edge touches the terrain line | Horizon clouds look washed out |

Keep the shader `Properties` defaults equal to the tuned material values so that a freshly created material looks identical.

## Symptom → first thing to check

| Symptom | Check first |
|---|---|
| "Dull, rainy sky" | The camera's visible sky band against `_GradientHeight`. Then shade area (`_ShadeThreshold`) and the shade colour |
| Clouds missing at some angles | The visible band (game-skybox step 1), then `_CoverageVariation` |
| Flat streaky clouds near the horizon | `_CloudHorizonBias` |
| Every cloud looks alike | `_CoverageVariation`, `_ClusterScale`, `_CloudPlaneScale` |
| Tiny fragments everywhere | `_DetailErosion` too high, or `_CloudPlaneScale` too high |

## Observed tuning passes (QB-001, chase camera, FOV 58°)

**First look (before any reference image).** Camera pitch 8°, which looked down about 20°.

| Pass | Values | What the Game view showed | Decision |
|---|---|---|---|
| 1 | coverage 0.48, scale 0.22, erosion 0.35, softness 0.03, shade (0.74,0.80,0.90) | Many tiny fragments. Lavender shade patches read as holes | Bigger clouds, less erosion, lighter shade |
| 2 | coverage 0.45, scale 0.12, erosion 0.18, softness 0.045 | Large soft masses, blurry edges, lost the cel look | Crisper edges, some erosion back |
| 3 | coverage 0.44, scale 0.15, erosion 0.26, softness 0.02, shade (0.78,0.84,0.93) | Crisp stylized clouds | Kept, until the user compared against the reference |

**Against the reference (Arceus-style tutorial frame).** Camera pitch lowered to −5°, which looks down about 7°.

| Pass | Values | Measured (reference: sky 37%, skyS 0.44, cloud 20%, cloudV 0.99) | Decision |
|---|---|---|---|
| Before | pass 3 values, gradient `smoothstep(-0.08, 0.85, y)`, pitch 8° | sky 19%, skyS 0.24, cloud 15%, cloudV 0.93: dull and rainy | The root cause was camera + gradient, not the clouds |
| 4 | pitch −5°, `_GradientHeight` 0.42, horizon (0.58,0.84,0.89), zenith (0.16,0.54,0.84), cluster mask 0.23/0.22, bias 0.1 | sky 40%, saturated, but clouds squashed flat with wide grey shade | Raise the horizon bias, shrink the shade |
| 5 | bias 0.3, scale 0.26, erosion 0.3, shade threshold 0.22, shade (0.87,0.92,0.99) | Round white cumulus, but few and very large | More and smaller clouds |
| 6 (kept) | scale 0.36, cluster 0.18, variation 0.25, coverage 0.49 | sky 40%, skyS 0.51, cloud ~18–20%, cloudV 0.97. Mixed sizes with open blue gaps | Adopted. No cloudless view in the six Game-view angles or the numeric sweep |

These values are a starting point for a similar low chase camera. A different art direction (realistic, painterly) changes the softness, the shade, and the palette first.
