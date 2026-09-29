# Case: CombatGirls on Unity-Chan Toon Shader SDF (Unity 6.6, URP 17.6), 2026-09-28/29

Goal: flat Fire Emblem: Three Houses look for CombatGirls characters in a Unity URP mobile project.

## Timeline

1. **Glossy under URP Lit.** The pack's Standard materials had been converted to URP Lit with smoothness 0.5 left in. Skin, armour and the ground reflected the sky. Smoothness 0, highlights and reflections off: the ground's mint sheen vanished, skin calmer, still "3D".
2. **Vendor toon package.** The pack shipped `Unity Chan Toon Shader - SDF - Unity6_URP_SwordShield.unitypackage`.
   - Overwrote 31 pack files (materials, a demo camera script); backed up first.
   - Needed `com.unity.timeline` (its bundled film utilities).
   - Test folders failed to compile on Unity 6.6 (`GetInstanceID` obsolete): deleted.
   - Demo camera script now required the Input System: restored.
   - Editor script adds `UNITY_PIPELINE_URP` to the scripting defines on every load.
3. **Magenta.** `LitForwardPass.hlsl` calls parameterless `IsSurfaceTypeTransparent()`; URP 17.6 moved it into `Shaders/Utils/SurfaceType.hlsl`, included by `LitInput.hlsl`, which the toon shader blocks (`URPIncludeGuards.hlsl` defines `UNIVERSAL_LIT_INPUT_INCLUDED`). Patch in that guard file:
   ```hlsl
   #define UNIVERSAL_SURFACE_TYPE_TRANSPARENT_INCLUDED
   inline bool IsSurfaceTypeTransparent() { return _Surface > 0.5; }
   inline bool IsSurfaceTypeOpaque() { return !IsSurfaceTypeTransparent(); }
   ```
4. **First trial used toon "twins"** in a separate folder and swapped them per unit. Replaced by converting the existing Lit copies in place (named after the vendor materials' GUIDs), so scenes, masked bodies and derived skins all followed.
5. **Fitted Tripo hair black:** imported at scale 100; outline width 1.2 → 0.012.
6. **Half the face white:** sun 1.25–1.3; `_Is_Filter_LightColor` = 1 on every toon material.
7. **Face shadow direction:** the vendor's `SDFFaceShadowController` feeds `_FaceForward/_FaceRight`. CombatGirls' head bone in rest pose: +Y = face forward, −Z = face right (bone forward pointed to the character's left). Our own component feeds them after the Animator.
8. **"Still shiny" (user):** every part was already `Toon/Toon`. The vendor values: cloth high colour 0.5 + matcap 0.85; hair high colour 0.5 + rim; weapons rim + matcap. All off.
9. **Face two-toned along the nose (user):** SDF face shadow. Off, face lit evenly (base step 0, feather 0.0001).
10. **Face vs thigh colour (user):** face even, body still on the vendor's two pink shade steps. Same view: face (238, 217, 208) sat 0.12 val 0.93; thigh lit (208, 164, 153) 0.26 / 0.82, shade (182, 132, 123) 0.33 / 0.71. Body lit evenly too: thigh (244, 219, 204) 0.16 / 0.96.
11. **Options (user):** skin tone swatches (1; 0.94/0.87/0.84; 0.85/0.75/0.75 = the old thigh colour; 0.74/0.60/0.55) and a body shade slider (shade colour up to lit × (0.9, 0.8, 0.8), step 0.4, feather 0.12). Face kept even.

12. **Shared for backgrounds (user):** `ToonStyle.Apply(material, Skin | Character | Environment)` became the one source; `ToonMaterialConverter` converts selected objects or builder output (URP Lit/Standard/Unlit with texture), `ToonStyle.Create` makes runtime materials from `Resources/Toon/ToonTemplate.mat`. Our vertex-colour shaders are skipped. Character materials were byte-identical before and after the refactor.

## What would have saved time

- Listing shader + effect values per renderer before the first change (step 8 was a value question, not an application question).
- Applying one skin rule to face and body at once (steps 9–10).
- Checking lossy scale, light intensity and bone axes against the vendor's assumptions right after the import (steps 5–7).
