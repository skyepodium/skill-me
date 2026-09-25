# Stylized cloud-layer skybox shader (Unity built-in pipeline reference)

Complete skybox shader: horizon→zenith gradient, **cloud plane** projection, Perlin-Worley erosion, two-tone toon shading from a second sample toward the sun, wind, horizon fade and haze. Property defaults are the values tuned in the QB-001 Game view (see [tuning.md](tuning.md)).

Assign via `RenderSettings.skybox` (camera clear flags = Skybox). `_WorldSpaceLightPos0` in a skybox pass is the sun direction (the `RenderSettings.sun` or brightest directional light); the shader falls back to a fixed direction when the sun is overhead.

```hlsl
Shader "Sky/StylizedCloudLayer"
{
    Properties
    {
        _HorizonColor ("Horizon", Color) = (0.72, 0.85, 0.90, 1)
        _ZenithColor ("Zenith", Color) = (0.20, 0.56, 0.83, 1)
        _CloudLitColor ("Cloud Lit", Color) = (1, 0.99, 0.94, 1)
        _CloudShadeColor ("Cloud Shade", Color) = (0.78, 0.84, 0.93, 1)
        _CloudOpacity ("Cloud Opacity", Range(0, 1)) = 0.95
        [NoScaleOffset] _CloudNoise ("Cloud Noise (R shape, G detail)", 2D) = "black" {}
        _CloudCoverage ("Cloud Coverage", Range(0, 1)) = 0.44
        _CloudEdgeSoftness ("Cloud Edge Softness", Range(0.001, 0.2)) = 0.02
        _CloudPlaneScale ("Cloud Plane Scale (tiles per unit)", Float) = 0.15
        _CloudHorizonBias ("Cloud Horizon Bias", Range(0.01, 0.5)) = 0.1
        _DetailTiling ("Detail Tiling", Float) = 2.7
        _DetailErosion ("Detail Erosion", Range(0, 1)) = 0.26
        _WindVelocity ("Wind Velocity (tiles per second, xy)", Vector) = (0.004, 0.0015, 0, 0)
        _DetailWindMultiplier ("Detail Wind Multiplier", Float) = 1.6
        _ShadeOffset ("Shade Offset Toward Sun (tiles)", Float) = 0.025
        _ShadeThreshold ("Shade Density Above Edge", Range(0, 0.5)) = 0.1
        _HorizonFadeHeight ("Horizon Fade Height", Range(0.001, 0.2)) = 0.025
        _HorizonHaze ("Horizon Haze", Range(0, 1)) = 0.45
        _HorizonHazeHeight ("Horizon Haze Height", Range(0.01, 1)) = 0.22
    }
    SubShader
    {
        Tags { "Queue" = "Background" "RenderType" = "Background" "PreviewType" = "Skybox" }
        Cull Off ZWrite Off
        Pass
        {
            CGPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #include "UnityCG.cginc"

            fixed4 _HorizonColor;
            fixed4 _ZenithColor;
            fixed4 _CloudLitColor;
            fixed4 _CloudShadeColor;
            float _CloudOpacity;
            sampler2D _CloudNoise;
            float _CloudCoverage;
            float _CloudEdgeSoftness;
            float _CloudPlaneScale;
            float _CloudHorizonBias;
            float _DetailTiling;
            float _DetailErosion;
            float4 _WindVelocity;
            float _DetailWindMultiplier;
            float _ShadeOffset;
            float _ShadeThreshold;
            float _HorizonFadeHeight;
            float _HorizonHaze;
            float _HorizonHazeHeight;

            static const float2 FallbackSunPlaneDirection = float2(0.7071, 0.7071);

            struct Input { float4 vertex : POSITION; };
            struct Interpolators { float4 position : SV_POSITION; float3 direction : TEXCOORD0; };

            Interpolators Vert(Input input)
            {
                Interpolators output;
                output.position = UnityObjectToClipPos(input.vertex);
                output.direction = input.vertex.xyz;
                return output;
            }

            // Projects a view ray onto a flat cloud layer: distant clouds shrink and crowd toward the horizon,
            // so every view that shows any sky also shows clouds, without longitude seams or a zenith pinch.
            float2 CloudPlanePoint(float3 direction)
            {
                return direction.xz / (direction.y + _CloudHorizonBias) * _CloudPlaneScale;
            }

            float CloudDensity(float2 planePoint, float2 wind)
            {
                float shape = tex2D(_CloudNoise, planePoint + wind).r;
                float detail = tex2D(_CloudNoise, planePoint * _DetailTiling + wind * _DetailWindMultiplier).g;
                return shape - (1.0 - detail) * _DetailErosion;
            }

            float2 SunPlaneDirection()
            {
                float2 sunHorizontal = _WorldSpaceLightPos0.xz;
                float lengthSquared = dot(sunHorizontal, sunHorizontal);
                if (lengthSquared < 1e-4) return FallbackSunPlaneDirection;
                return sunHorizontal * rsqrt(lengthSquared);
            }

            fixed4 Frag(Interpolators input) : SV_Target
            {
                float3 direction = normalize(input.direction);
                float horizonBlend = smoothstep(-0.08, 0.85, direction.y);
                fixed3 sky = lerp(_HorizonColor.rgb, _ZenithColor.rgb, horizonBlend);
                if (direction.y <= 0.0) return fixed4(sky, 1);

                float2 planePoint = CloudPlanePoint(direction);
                float2 wind = _WindVelocity.xy * _Time.y;
                float edge = 1.0 - _CloudCoverage;
                float density = CloudDensity(planePoint, wind);
                float body = smoothstep(edge, edge + _CloudEdgeSoftness, density);

                // Toon shading: sample toward the sun; the sun-facing rim stays lit, the dense core turns to shade.
                float densityTowardSun = CloudDensity(planePoint + SunPlaneDirection() * _ShadeOffset, wind);
                float coreThreshold = edge + _ShadeThreshold;
                float shade = smoothstep(coreThreshold, coreThreshold + _CloudEdgeSoftness, densityTowardSun);
                fixed3 cloud = lerp(_CloudLitColor.rgb, _CloudShadeColor.rgb, shade);
                cloud = lerp(cloud, _HorizonColor.rgb, (1.0 - smoothstep(0.0, _HorizonHazeHeight, direction.y)) * _HorizonHaze);

                float cloudAlpha = body * _CloudOpacity * smoothstep(0.0, _HorizonFadeHeight, direction.y);
                return fixed4(lerp(sky, cloud, cloudAlpha), 1);
            }
            ENDCG
        }
    }
    Fallback Off
}
```

## Porting notes

- **URP/HDRP:** keep `CloudPlanePoint`, `CloudDensity` and the shading block; replace `UnityCG.cginc`/`CGPROGRAM` with the pipeline's HLSL includes and read the main light direction from the pipeline's light API. HDRP normally uses its own sky system; implement it as a custom sky renderer or a Shader Graph fullscreen/sky material.
- **Godot/Unreal/WebGL:** the fragment logic is engine-neutral: normalize the view ray, `ray.xz / (ray.y + bias) * scale`, two texture reads for density, one extra density evaluation offset toward the sun.
- **Why the plane, not lat/long:** a lat/long mapping (`atan2` longitude) seams at ±180°, pinches at the zenith and draws horizon clouds as large as overhead ones. Plane projection shrinks and crowds distant clouds toward the horizon, so any view that shows sky shows clouds.
- `_CloudHorizonBias` bounds the stretch at the horizon (the plane coordinate → ∞ as `dir.y → 0`); mipmapping on the noise hides the resulting minification.
