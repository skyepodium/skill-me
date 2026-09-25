# Observed case: QB-001 river ("clean, emerald, clear blue like Mabinogi's sea")

**Starting point:** the river was a 3 × 180 m opaque cube using the shared prop material, rendered neon cyan (110,235,220). There was no depth colour, reflection, transparency, ripples or foam.

**Constraints:**
- Mobile, minimum Galaxy S10.
- URP with the depth texture and opaque texture both off for cost.
- Stylized, low-poly valley with a baked terrain, straight river along world Z.

**Why not an off-the-shelf stylized water shader:** common open-source URP water shaders expect the depth and opaque textures to be enabled (checked from repository summaries; code and licences not reviewed). Their techniques are standard: depth colour, Fresnel, flowing normals, glints, intersection foam. We rebuilt only the parts we needed, with depth derived analytically from the channel shape.

**What worked:**
1. Depth from |x| (distance to the river centre): emerald banks, clear blue centre.
2. A translucent surface over a riverbed painted by the terrain shader below the water line.
3. A sky-gradient Fresnel copied from the sky material, biased to zenith and tinted brighter so grazing water is not horizon-cyan.
4. Two flowing ripple normal maps baked by the editor builder.
5. Twinkles independent of view direction. A physically correct sun glint alone gave 0 % sparkle because the chase camera faces away from the sun.
6. Bank foam plus foam boxes around the docks and the moving boat, fed per frame through a `MaterialPropertyBlock`.

**Flow direction:** the first version hard-coded downstream as +Z. From the default camera (looking +X) that is screen-left, and the user saw the water run right to left. Making it `_FlowDirection = (0, -1)` fixed it. The fix was measured: +26 px to the right over one second of game time, against −34 px before.

**Pitfall:** `point` is a reserved word in HLSL, so a function parameter named `point` failed to compile.

**Result:**
- Bank 180° (reference 183°) and centre 203° (reference 203°).
- Visible ripples, foam and sparkle.
- One translucent quad, no new render textures.
