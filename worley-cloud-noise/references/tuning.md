# Tuning the cloud layer

Tune in the target game view at the default camera, not in a material preview sphere. Change one group at a time and capture before/after.

## Parameters

| Property | Controls | Raise it when | Lower it when |
|---|---|---|---|
| `_CloudCoverage` | Share of sky covered (density threshold = `1 - coverage`) | Sky reads empty | Sky reads overcast / clouds merge into sheets |
| `_CloudPlaneScale` | Noise tiles per plane unit; smaller = bigger clouds | Clouds look like few giant blobs | Clouds look like scattered confetti |
| `_CloudHorizonBias` | Stretch limit near the horizon | Horizon clouds smear into streaks | Horizon band looks too uniform / clouds don't shrink with distance |
| `_DetailErosion` | How deeply the Worley detail notches edges | Edges look like smooth airbrushed blobs | Clouds fragment into many specks |
| `_DetailTiling` | Size of the edge notches relative to the shape | Notches look like large bites | Notches read as noise/shimmer |
| `_CloudEdgeSoftness` | Width of the alpha ramp at the edge; small = crisp cel edge | Edges alias or look cut out | Edges look blurry (loses the stylized read) |
| `_ShadeThreshold` | How far inside the edge the shade tone starts | Shade covers most of the cloud / looks like holes | No shade band at all |
| `_ShadeOffset` | Width of the lit rim on the sun side | Lit rim too thin | Whole cloud reads lit or banding appears |
| `_CloudShadeColor` | Shade tone | — | Shade reads as a hole in the cloud → move it toward the lit colour |
| `_WindVelocity` | Drift in tiles/second | Motion invisible over ~10 s | Motion is distracting during puzzle play |
| `_HorizonFadeHeight`, `_HorizonHaze*` | Fade into the horizon colour | Hard cloud edge touches the terrain line | Horizon clouds look washed out |

Keep the shader `Properties` defaults equal to the tuned material values so a freshly created material looks identical.

## Observed tuning passes (QB-001, chase camera, FOV 58°)

| Pass | Values | What the Game view showed | Decision |
|---|---|---|---|
| 1 | coverage 0.48, scale 0.22, erosion 0.35, softness 0.03, shade (0.74,0.80,0.90) | Many tiny fragments; lavender shade patches read as holes | Bigger clouds, less erosion, lighter shade |
| 2 | coverage 0.45, scale 0.12, erosion 0.18, softness 0.045 | Large soft masses; edges blurry, lost the cel look | Crisper edge, some erosion back |
| 3 (kept) | coverage 0.44, scale 0.15, erosion 0.26, softness 0.02, shade (0.78,0.84,0.93), threshold 0.10, offset 0.025 | Crisp puffy stylized clouds, sun-side lit rim, soft blue core | Adopted; coverage 4–27% of visible sky at every pitch/yaw |

These values are a starting point for a similar chase camera; a camera that sees more zenith needs a larger plane scale check, and a different art direction (realistic, painterly) changes softness and shade first.
