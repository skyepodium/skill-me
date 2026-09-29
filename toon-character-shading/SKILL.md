---
name: toon-character-shading
description: Move rigged game characters and the scenery around them to a flat anime/cel look (Fire Emblem, Genshin-like) in Unity URP, or fix one that looks glossy, blotchy, "realistic 3D" or mismatched. Use when characters "shine", when outfits or hair still read as realistic under a toon shader (light painted into textures), when adopting a vendor toon shader (Unity-Chan Toon Shader/UTS, lilToon) on existing materials, when a toon face shows a two-tone split or white blow-out, when face and body skin colours differ, when outlines turn meshes black, when purchased foliage/rocks clash with toon characters, or when adding skin tone / body shade options.
---

# Toon Character Shading

A flat anime look is mostly **material values, texture content and scene conditions**, not the choice of shader. The rule behind a good result: **light is drawn by the shader only.** A surface with no texture (one colour plus a shade colour) or a flat texture with line art reads as anime; a texture with painted light (shine bands, fold shading, gradients, photo detail) gets the toon steps on top and reads as realistic 3D. Before changing anything, prove whether the problem is "not applied", "applied with the wrong values", "light painted in the texture" or "light from the shader".

Case record (CombatGirls + Unity-Chan Toon Shader SDF, URP 17.6; P09 lilToon parts; a vendor jungle pack): [references/combatgirls-case.md](references/combatgirls-case.md). The numbers there are those assets', not defaults.

## 1. Inventory what is actually rendered

For every visible renderer and submesh of the character, list:
- the shader name, and whether the material is an asset that other things reference (scenes, baked meshes, derived materials);
- the effects that make a surface shine: smoothness/metallic (PBR), specular or high colour, rim light, matcap, environment reflection, angel ring;
- the shading rule: shade steps and feathers, shade colours, SDF face shadow.

Also record scene conditions: main light intensity and colour, ambient, each renderer's lossy scale, the head bone's axes in the rest pose, the render pipeline version.

**Done when:** a table shows each part's shader and effect values, so "still shiny" can be pinned to a value.

## 2. Remove gloss before going toon

A PBR material converted from another pipeline often keeps a default smoothness (URP Lit 0.5) and environment reflection: skin, cloth and even the ground mirror the sky. Set smoothness 0, turn off specular highlights and environment reflections (and their keywords) on character and ground materials. Compare the same view at the old and new values.

## 3. Adopt a vendor toon shader safely

- List the package's paths before importing; back up every existing file it will overwrite (vendor packages often rewrite the original materials and demo scripts).
- Resolve compile blockers without editing game code: missing dependencies (add the official package), test folders using removed APIs (delete), demo scripts with new dependencies (restore the backup). Expect editor scripts that add define symbols.
- If the shader was written for an older pipeline version and renders magenta, read the first shader error. A typical cause: the toon shader blocks the pipeline's Lit input file (its own CBUFFER) and a helper moved there. Patch the vendor include with a marker, idempotently, and keep the patch in a menu so a reinstall can reapply it.
- **Convert in place.** Overwrite the materials that the character already uses (keep the asset and its GUID) with the vendor's toon settings. Everything referencing them follows. Parallel "toon twin" materials force every reference to be rewired.
- Keep texture properties in step: toon shaders often read `_MainTex` while other code writes `_BaseMap`. Write both from code, bakers and colour pickers.

## 4. Fix the look against the scene

| Symptom | Check | Fix |
|---|---|---|
| Lit side blown to white | light intensity > 1 multiplied into the colour | the shader's light colour limiter (UTS `_Is_Filter_LightColor`), or light ≤ 1 |
| Mesh or hair fully black | lossy scale ≠ 1 with an object-space outline | outline width ÷ scale |
| Face shadow wrong or two-toned along the nose | SDF face shadow expects head vectors from a script; bone axes differ per rig | feed forward/right from the head bone each frame, or turn the face SDF off and light the face evenly |
| Still shiny after toon | specular/high colour, rim, matcap values | turn them off (keep only on purpose, per part) |
| Face and body skin differ | the two use different shading rules | one rule for all skin (face, body, derived skins) |
| Tint or recolour ignored in shade | shade colours are separate from the base colour | multiply the tint into the shade colours too |
| Tint wipes a material's own colour | a property block value replaces the material value | block value = material value × tint |

Painted light in textures cannot be removed by shader values: flatten the texture (section 6).

## 5. Find where the light comes from

Put a part that looks right next to one that does not (e.g. an untextured fitted hair against a pack hair) and dump both materials' values side by side: print only the properties that differ, plus each material's textures. If the toon values match and only the texture differs, open the texture: painted angel rings, highlight strokes, metal reflections, fold shading and gradients are the cause. For foliage and rocks from environment packs, also check whether their own shader adds light (translucency, soft wrap lighting, colour noise, reflections): then flattening the texture changes little.

## 6. Flatten painted light out of textures

[scripts/flatten_albedo.py](scripts/flatten_albedo.py) (numpy, OpenCV; Pillow for TGA) keeps colour regions and line art and removes painted light:
- Line art: pixels much darker than their neighbourhood median keep their colour.
- Regions: mean-shift smoothing, then a floating-range flood fill (small neighbour steps join, sharp steps stop), so a painted gradient stays one region. Clustering colours (k-means) cut gradients into bands and read as camouflage.
- Fill: each region takes the lit side of its pixels (lightness 65th percentile, median hue); the shader draws the shade.
- `--drop-highlights` (hair): small regions clearly brighter than their ring are painted shine and take the ring's colour; strand lines stay.
- `--bands N` (rocks, bark): one colour per region loses cracks and facets and reads as a lump; bands keep them as 2–4 flat darker steps. A normal map on the toon shader did not help: most faces sat on the lit side of the step.

Wire the results in through the owner that already swaps textures (colour choices, property blocks), keep them in a gitignored generated folder when derived from purchased assets, and reuse a result while it is newer than its source and the script. After flattening, give outfits a hard shade step (feather about 0.04) on their renderers only; leave faces and skin as they were. A part that keeps its own texture until a colour is chosen (a pack hair) must apply the flat colour at start.

## 7. Other packs' shaders on the same character

Parts from another pack (e.g. lilToon hair and armour with reflection, matcap and rim) get toon copies of their materials, not edits of the vendor files; convert every place a material is chosen from (colour options, per-style exceptions, preview renderers), and let a rerun find the source again from the copy's name. Metal that the vendor shader darkened through metallic × reflection turns pale on a toon shader: darken the base map where the metallic map says metal before converting.

## 8. Scenery that matches the characters

- Floors: a world-noise flat-colour terrain shader, no photo layers.
- Foliage: a small toon foliage shader of your own (two shade steps, cutout, two-sided) that keeps the vendor meshes' conventions: which vertex colour channels drive sway and flutter, UV-based grass wind, edge-on card fade, and the vendor's wind globals. Switch trunks and leaves together so they keep swaying as one tree.
- Vendor tints were chosen for the vendor's lighting; on two steps they turn dark and olive. Keep the hue, set a brightness, cap saturation (full brightness went neon).
- Many small plants: draw them with GPU instancing in cell batches; the SRP Batcher otherwise draws every copy.

## 9. Verify with numbers and matched views

- Same camera, pose and light before/after. Include the user's reported view.
- Sample pixels on face and body (cheek, thigh) with [scripts/sample_pixels.py](scripts/sample_pixels.py); compare RGB, saturation and value. Skin should match within a few points.
- Check every scene and UI that shows the character (gameplay, customizer thumbnails), and re-bake derived assets.
- Mobile cost: outlines add a pass per material; measure draw calls on the target device before calling it done. Mark device checks as unverified until run.

## 10. Make the look one module, then reuse it for new assets

Put the look in one function that takes the surface kind (skin, character, environment) and sets every toon value, and route everything through it: the character conversion, a converter for assets added later (textured sources → toon materials keeping texture and colour, saved next to each other and updated in place, outline width divided by the renderer's scale), and runtime creation from a toon template asset kept in `Resources` (so the shader ships in builds, with a lit fallback when the vendor shader is missing). Environment surfaces usually drop the outline. Skip sources whose colour lives in vertex colours if the toon shader ignores them, and say so. After refactoring, diff the character materials before and after: they must not change.

## 11. Options players or designers can choose

Skin tone and body shade are cheap on a toon material: tone multiplies base and shade colours on face and body together; a body shade slider moves the base step and blends the shade colour from white to a light shade. Keep the face out of shade if its split read as a stain.

Record each change, its measured effect and what stays unverified in the project; promote only verified rules here (source: `dev/skill-me/toon-character-shading`).
