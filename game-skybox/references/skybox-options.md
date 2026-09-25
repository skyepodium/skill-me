# Skybox options

Pick by what the camera sees and what must change at runtime, not by what looks best in a reference video.

| Option | What it is | Strengths | Costs / failure modes | Pick when |
|---|---|---|---|---|
| **Cubemap / 6-sided image** | Six images folded into a cube around the world | Art-directed, any style, zero shader math | Static unless layered; resolution thins near the horizon; must match the scene's art style; licensing for bought skies | Fixed time of day, painted look, background never changes |
| **Procedural gradient** | Horizon→zenith colour from view-ray height | Tiny, tweakable, matches fog colour exactly | No clouds on its own | Base layer for everything else |
| **2D cloud layer on a plane** | View ray projected to a virtual cloud plane, noise density, fake lighting | Clouds at every angle, perspective toward the horizon, wind, cheap (a few texture reads) | Flat: no fly-through or parallax between layers | Ground or chase cameras that mostly see 0–40° elevation — see the `worley-cloud-noise` skill |
| **Lat/long mapped clouds** | Cloud texture or blobs placed by longitude/latitude | Easy to place individual clouds | Seam at ±180°, zenith pinch, no horizon perspective, easy to put clouds where the camera never looks | Rarely; prefer the plane |
| **Volumetric raymarch** | 3D Perlin-Worley textures marched through a cloud slab with light scattering | Real depth, fly-through, dramatic lighting | GPU cost, temporal reprojection, much more tuning | Flight/open-world cameras that look up or move through clouds |
| **Mesh / billboard clouds** | Modelled or sprite clouds in the scene | Strong stylization, exact placement | Visible from limited distances; sorting; scale versus far clip | Diorama or toy-box art where clouds are props |

## Integration checklist

- The horizon colour, fog colour and camera background agree, so terrain fades into the sky with no seam.
- The far clip and fog end hide the ground edge; the sky is the only thing behind them.
- The sun direction used for cloud shading is the same light that casts the scene's shadows.
- Required sky assets (material, textures) are validated where the sky is applied, with an actionable error when missing.
