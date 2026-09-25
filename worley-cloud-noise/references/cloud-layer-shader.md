# Stylized cloud-layer skybox shader (Unity URP reference)

Complete URP skybox shader (HLSL). It draws a horizon→zenith gradient and a cloud layer: the **cloud plane** projection, a low-frequency **cluster mask** that varies coverage by region, Perlin-Worley erosion, two-tone toon shading from a second sample toward the sun, wind, horizon fade and haze. Property defaults are the values tuned against the Arceus-style reference in the QB-001 Game view (see [tuning.md](tuning.md)).

Assign via `RenderSettings.skybox` (camera clear flags = Skybox). In URP the sun direction is `_MainLightPosition` (direction toward the main light), set per camera before the skybox draws. The shader falls back to a fixed direction when the sun is overhead.

```hlsl
Shader "Sky/StylizedCloudLayer"
{
    Properties
    {
        _HorizonColor ("Horizon", Color) = (0.58, 0.84, 0.89, 1)
        _ZenithColor ("Zenith", Color) = (0.16, 0.54, 0.84, 1)
        _GradientHeight ("Gradient Height (dir.y where zenith colour is reached)", Range(0.05, 1)) = 0.42
        _CloudLitColor ("Cloud Lit", Color) = (1, 1, 0.98, 1)
        _CloudShadeColor ("Cloud Shade", Color) = (0.87, 0.92, 0.99, 1)
        _CloudOpacity ("Cloud Opacity", Range(0, 1)) = 0.95
        [NoScaleOffset] _CloudNoise ("Cloud Noise (R shape, G detail)", 2D) = "black" {}
        _CloudCoverage ("Cloud Coverage", Range(0, 1)) = 0.49
        _ClusterScale ("Cluster Scale (relative to plane)", Float) = 0.18
        _CoverageVariation ("Coverage Variation", Range(0, 0.5)) = 0.25
        _CloudEdgeSoftness ("Cloud Edge Softness", Range(0.001, 0.2)) = 0.02
        _CloudPlaneScale ("Cloud Plane Scale (tiles per unit)", Float) = 0.36
        _CloudHorizonBias ("Cloud Horizon Bias", Range(0.01, 0.5)) = 0.3
        _DetailTiling ("Detail Tiling", Float) = 2.7
        _DetailErosion ("Detail Erosion", Range(0, 1)) = 0.3
        _WindVelocity ("Wind Velocity (tiles per second, xy)", Vector) = (0.004, 0.0015, 0, 0)
        _DetailWindMultiplier ("Detail Wind Multiplier", Float) = 1.6
        _ShadeOffset ("Shade Offset Toward Sun (tiles)", Float) = 0.025
        _ShadeThreshold ("Shade Density Above Edge", Range(0, 0.5)) = 0.22
        _HorizonFadeHeight ("Horizon Fade Height", Range(0.001, 0.2)) = 0.025
        _HorizonHaze ("Horizon Haze", Range(0, 1)) = 0.3
        _HorizonHazeHeight ("Horizon Haze Height", Range(0.01, 1)) = 0.22
    }
    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" "Queue" = "Background" "RenderType" = "Background" "PreviewType" = "Skybox" }
        Cull Off ZWrite Off
        Pass
        {
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            TEXTURE2D(_CloudNoise);
            SAMPLER(sampler_CloudNoise);

            CBUFFER_START(UnityPerMaterial)
            half4 _HorizonColor;
            half4 _ZenithColor;
            float _GradientHeight;
            half4 _CloudLitColor;
            half4 _CloudShadeColor;
            float _CloudOpacity;
            float _CloudCoverage;
            float _ClusterScale;
            float _CoverageVariation;
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
            CBUFFER_END

            static const float2 FallbackSunPlaneDirection = float2(0.7071, 0.7071);
            // Decorrelates the cluster mask from the shape sample that reads the same channel.
            static const float2 ClusterSampleOffset = float2(0.37, 0.61);

            struct Input { float4 vertex : POSITION; };
            struct Interpolators { float4 position : SV_POSITION; float3 direction : TEXCOORD0; };

            Interpolators Vert(Input input)
            {
                Interpolators output;
                output.position = TransformObjectToHClip(input.vertex.xyz);
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
                float shape = SAMPLE_TEXTURE2D(_CloudNoise, sampler_CloudNoise, planePoint + wind).r;
                float detail = SAMPLE_TEXTURE2D(_CloudNoise, sampler_CloudNoise, planePoint * _DetailTiling + wind * _DetailWindMultiplier).g;
                return shape - (1.0 - detail) * _DetailErosion;
            }

            float2 SunPlaneDirection()
            {
                // URP publishes the main directional light as a direction toward the light.
                float2 sunHorizontal = _MainLightPosition.xz;
                float lengthSquared = dot(sunHorizontal, sunHorizontal);
                if (lengthSquared < 1e-4) return FallbackSunPlaneDirection;
                return sunHorizontal * rsqrt(lengthSquared);
            }

            half4 Frag(Interpolators input) : SV_Target
            {
                float3 direction = normalize(input.direction);
                float horizonBlend = smoothstep(0.0, _GradientHeight, direction.y);
                half3 sky = lerp(_HorizonColor.rgb, _ZenithColor.rgb, horizonBlend);
                if (direction.y <= 0.0) return half4(sky, 1);

                float2 planePoint = CloudPlanePoint(direction);
                float2 wind = _WindVelocity.xy * _Time.y;
                // A low-frequency mask groups clouds into large masses separated by open blue sky.
                float cluster = SAMPLE_TEXTURE2D(_CloudNoise, sampler_CloudNoise,
                    planePoint * _ClusterScale + ClusterSampleOffset + wind * _ClusterScale).r;
                float localCoverage = _CloudCoverage + (cluster - 0.5) * 2.0 * _CoverageVariation;
                float edge = 1.0 - localCoverage;
                float density = CloudDensity(planePoint, wind);
                float body = smoothstep(edge, edge + _CloudEdgeSoftness, density);

                // Toon shading: sample toward the sun; the sun-facing rim stays lit, the dense core turns to shade.
                float densityTowardSun = CloudDensity(planePoint + SunPlaneDirection() * _ShadeOffset, wind);
                float coreThreshold = edge + _ShadeThreshold;
                float shade = smoothstep(coreThreshold, coreThreshold + _CloudEdgeSoftness, densityTowardSun);
                half3 cloud = lerp(_CloudLitColor.rgb, _CloudShadeColor.rgb, shade);
                cloud = lerp(cloud, _HorizonColor.rgb, (1.0 - smoothstep(0.0, _HorizonHazeHeight, direction.y)) * _HorizonHaze);

                float cloudAlpha = body * _CloudOpacity * smoothstep(0.0, _HorizonFadeHeight, direction.y);
                return half4(lerp(sky, cloud, cloudAlpha), 1);
            }
            ENDHLSL
        }
    }
    Fallback Off
}
```

## Porting notes

- **Built-in pipeline:** replace `HLSLPROGRAM`/`Core.hlsl` with `CGPROGRAM` and `#include "UnityCG.cginc"`. Use `UnityObjectToClipPos`, `sampler2D` with `tex2D`, and `_WorldSpaceLightPos0.xz` for the sun. Drop the `CBUFFER` block and the `RenderPipeline` tag.
- **HDRP:** HDRP uses its own sky system. Port the fragment logic into a custom sky renderer or a Shader Graph sky material.
- **Godot/Unreal/WebGL:** the fragment logic is engine-neutral:
  - normalize the view ray and compute `ray.xz / (ray.y + bias) * scale`;
  - read the texture three times (shape, detail, cluster mask);
  - evaluate density once more with an offset toward the sun.
- **Why the plane and not lat/long:** a lat/long mapping (`atan2` longitude) has three problems:
  - it seams at ±180°;
  - it pinches at the zenith;
  - it draws horizon clouds as large as overhead ones.

  Plane projection shrinks distant clouds and crowds them toward the horizon, so any view that shows sky shows clouds.
- **Horizon stretch:** `_CloudHorizonBias` bounds how far the plane coordinate stretches near the horizon. Low values (0.1) squash horizon clouds into flat streaks. Values around 0.3 keep them round, closer to a painted sky dome. Mipmaps on the noise texture hide the minification.
- **Gradient reach:** `_GradientHeight` is the `dir.y` at which the zenith colour takes over. It must fall inside the camera's visible sky band. A chase camera that sees only 0–20° shows nothing but the pale horizon colour when this value is 0.8 or more.
