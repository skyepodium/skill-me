# Tuning the stylized river

Tune in the game view at the views players actually use: the default chase view, a high view down at the water, and a view along the water. Measure zones with `scripts/water_palette_compare.py` against the reference before and after each pass.

## Parameters

| Property | Controls | Raise it when | Lower it when |
|---|---|---|---|
| `_ShallowColor` / `_DeepColor` | Bank vs centre colour | — | — (match measured hues: emerald ~180°, clear blue ~203°) |
| `_ShallowAlpha` / `_DeepAlpha` | How much riverbed shows through | Water looks like tinted glass | Water looks like painted plastic |
| `_ReflectionStrength`, `_FresnelPower` | Sky reflection at grazing angles | Distant water looks as dark as nearby water | Near water turns milky |
| `_ReflectionTint`, `_ReflectionTintBlend` | Brightness/blueness of the reflection | Far water reads cyan-grey (horizon haze) | Far water glows white |
| `_RippleScaleA/B`, `_RippleStrength` | Ripple size and bumpiness | Surface looks flat | Surface looks noisy or boiling |
| `_FlowSpeed` | Downstream speed (m/s) | Water looks still | Flow distracts |
| `_GlintPower`, `_GlintIntensity` | Sun highlight (only when facing the sun) | No sparkle toward the sun | Harsh white patches |
| `_SparkleScale`, `_SparkleThreshold`, `_SparkleIntensity` | View-independent twinkles | Water looks dull from views away from the sun | More than ~2 % of water pixels twinkle |
| `_BankFoamWidth`, `_ObjectFoamWidth`, `_FoamNoiseScale` | Foam lines | Banks or objects float without contact | Foam reads as a continuous painted white line |

## Symptom → first thing to check

| Symptom | Check first |
|---|---|
| "Neon / plastic water" | It is probably an opaque single-colour surface. Add the depth colour and translucency, and paint the riverbed |
| No sparkle at all | The camera faces away from the sun, so only view-independent twinkles can show |
| Far water too cyan | Reflection samples the horizon colour; bias toward zenith and blend a highlight tint |
| Foam looks like a drawn line | Narrow the width and raise the noise threshold so it breaks up |
| Shallows invisible | Riverbed not painted, or `_ShallowAlpha` too high |

## Observed passes (QB-001 river, 3 m wide, chase camera)

References are Mabinogi Mobile sea captures: shallows (104,143,145) hue 183°, near water (116,178,216) hue 203° V 0.85, far horizon reflection (162,196,249) hue 217°, glints 0.9–1.9 %.

| Pass | Change | Measured | Decision |
|---|---|---|---|
| Before | Opaque cube, one material colour | (110,235,220) hue 173°, no variation, 0 % glints | Replace with the translucent shader |
| 1 | Shader defaults above (reflection 0.75, power 4, glint 600, foam 0.16 m) | Centre 202° V 0.79, bank 180° V 0.64, far/grazing 193° V 0.75, glints 0 % | Far too cyan, no sparkle, foam too solid |
| 2 | Reflection biased to zenith + highlight tint 0.45, strength 0.9, power 3; glint 250; foam 0.11 m, higher threshold | Centre 203°, bank 180°, grazing 197°, still 0 % glints | The camera faces away from the sun, so add twinkles |
| 3 (kept) | View-independent twinkles (scale 7, threshold 0.8, intensity 1.4) | Top view ~2.8 % bright pixels (incl. foam) | Adopted |

The sea's far-horizon value (217°) is not reachable or meaningful on a 3 m river 8–10 m from the camera. Compare like with like: river body against the sea's near water.
