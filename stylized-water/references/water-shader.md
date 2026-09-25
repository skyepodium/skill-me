# Stylized river shader (Unity URP reference, mobile)

A translucent water surface that flows along a configurable world direction (`_FlowDirection`, world xz) and needs **no depth texture and no opaque texture**. Depth comes from the known channel geometry: here, a straight river along world Z centred on x = 0, so `depth = f(|x|)`.

It combines:
- emerald shallows → clear blue body
- a sky-gradient Fresnel reflection with a bright highlight
- two flowing ripple normal maps
- a sun glint plus view-independent twinkles
- broken, flowing foam along the banks and around rectangles (docks, a moving boat) fed from script

Defaults are the values tuned against Mabinogi Mobile sea captures (see [tuning.md](tuning.md)).

For a curved river or a lake, keep the rest and replace the depth proxy:
- **Bake a distance-to-shore texture:** preferred on mobile.
- **Or use per-vertex shore distance:** store it in vertex colour on a river mesh.
- **Or use the camera depth texture:** only if the project already pays for it.

The shader includes a small noise/lighting file. Its relevant functions are listed after the shader.

```hlsl
Shader "Water/StylizedRiver"
{
    // Mobile river without depth or opaque textures. The river runs along world Z centred on x = 0, so
    // depth is derived from |x|: emerald shallows at the banks, clear blue in the middle. Two flowing normal
    // maps give ripples, a sky-gradient Fresnel reflection brightens grazing views, sun glints sparkle, and
    // foam lines trace the banks, the docks and the boat. The surface is translucent over the painted riverbed.
    Properties
    {
        _ShallowColor ("Shallow (banks)", Color) = (0.36, 0.72, 0.62, 1)
        _DeepColor ("Deep (centre)", Color) = (0.30, 0.62, 0.86, 1)
        _ShallowAlpha ("Shallow Alpha", Range(0, 1)) = 0.45
        _DeepAlpha ("Deep Alpha", Range(0, 1)) = 0.82
        _HorizonColor ("Sky Horizon", Color) = (0.58, 0.84, 0.89, 1)
        _ZenithColor ("Sky Zenith", Color) = (0.16, 0.54, 0.84, 1)
        _ReflectionTint ("Reflection Highlight", Color) = (0.68, 0.80, 1, 1)
        _ReflectionTintBlend ("Reflection Highlight Blend", Range(0, 1)) = 0.45
        _ReflectionStrength ("Reflection Strength", Range(0, 1)) = 0.9
        _FresnelPower ("Fresnel Power", Float) = 3
        [NoScaleOffset] _RippleNormal ("Ripple Normal", 2D) = "bump" {}
        _RippleScaleA ("Ripple Scale A (tiles per m)", Float) = 0.45
        _RippleScaleB ("Ripple Scale B (tiles per m)", Float) = 0.9
        _RippleStrength ("Ripple Strength", Range(0, 1)) = 0.45
        _FlowSpeed ("Flow Speed (m/s)", Float) = 0.35
        _FlowDirection ("Flow Direction (world xz)", Vector) = (0, -1, 0, 0)
        _GlintPower ("Glint Sharpness", Float) = 250
        _GlintIntensity ("Glint Intensity", Float) = 2.5
        _SparkleScale ("Sparkle Scale (per m)", Float) = 7
        _SparkleThreshold ("Sparkle Threshold", Range(0.5, 1)) = 0.8
        _SparkleIntensity ("Sparkle Intensity", Float) = 1.4
        _FoamColor ("Foam", Color) = (0.96, 0.99, 1, 1)
        _BankFoamWidth ("Bank Foam Width (m)", Float) = 0.11
        _ObjectFoamWidth ("Object Foam Width (m)", Float) = 0.14
        _FoamNoiseScale ("Foam Noise Scale (per m)", Float) = 2.2
        _RiverHalfWidth ("River Half Width (m)", Float) = 1.52
        _FoamBoxLeftDock ("Foam Box Left Dock (x,z,hx,hz)", Vector) = (0, 0, 0, 0)
        _FoamBoxRightDock ("Foam Box Right Dock (x,z,hx,hz)", Vector) = (0, 0, 0, 0)
        _FoamBoxBoat ("Foam Box Boat (x,z,hx,hz)", Vector) = (0, 0, 0, 0)
    }
    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" "RenderType" = "Transparent" "Queue" = "Transparent-100" "IgnoreProjector" = "True" }
        Blend SrcAlpha OneMinusSrcAlpha
        ZWrite Off
        Pass
        {
            Name "River"
            Tags { "LightMode" = "UniversalForward" }
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag
            #pragma multi_compile_fog
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
            #include "MeadowGround.hlsl"

            TEXTURE2D(_RippleNormal);
            SAMPLER(sampler_RippleNormal);

            CBUFFER_START(UnityPerMaterial)
            half4 _ShallowColor;
            half4 _DeepColor;
            half _ShallowAlpha;
            half _DeepAlpha;
            half4 _HorizonColor;
            half4 _ZenithColor;
            half4 _ReflectionTint;
            half _ReflectionTintBlend;
            half _ReflectionStrength;
            float _FresnelPower;
            float _RippleScaleA;
            float _RippleScaleB;
            half _RippleStrength;
            float _FlowSpeed;
            float4 _FlowDirection;
            float _GlintPower;
            half _GlintIntensity;
            float _SparkleScale;
            half _SparkleThreshold;
            half _SparkleIntensity;
            half4 _FoamColor;
            float _BankFoamWidth;
            float _ObjectFoamWidth;
            float _FoamNoiseScale;
            float _RiverHalfWidth;
            float4 _FoamBoxLeftDock;
            float4 _FoamBoxRightDock;
            float4 _FoamBoxBoat;
            CBUFFER_END

            struct Input { float4 vertex : POSITION; };
            struct Interpolators { float4 position : SV_POSITION; float3 world : TEXCOORD0; half fog : TEXCOORD1; };

            Interpolators Vert(Input input)
            {
                Interpolators output;
                output.world = TransformObjectToWorld(input.vertex.xyz);
                output.position = TransformWorldToHClip(output.world);
                output.fog = ComputeFogFactor(output.position.z);
                return output;
            }

            // Distance outside an axis-aligned box on the water plane (0 inside).
            float BoxDistance(float2 position, float4 box)
            {
                if (box.z <= 0.0) return 1e4;
                float2 outside = max(abs(position - box.xy) - box.zw, 0.0);
                return length(outside);
            }

            half4 Frag(Interpolators input) : SV_Target
            {
                float2 xz = input.world.xz;
                float time = _Time.y;

                // Two ripple layers flowing downstream at different speeds and scales, the second slightly cross-current.
                float2 downstream = normalize(_FlowDirection.xy);
                float2 across = float2(downstream.y, -downstream.x);
                float2 flowA = downstream * (time * _FlowSpeed);
                float2 flowB = (downstream * 0.6 + across * 0.15) * (time * _FlowSpeed);
                half3 rippleA = UnpackNormal(SAMPLE_TEXTURE2D(_RippleNormal, sampler_RippleNormal, (xz - flowA) * _RippleScaleA));
                half3 rippleB = UnpackNormal(SAMPLE_TEXTURE2D(_RippleNormal, sampler_RippleNormal, (xz - flowB) * _RippleScaleB + 0.37));
                half2 tilt = (rippleA.xy + rippleB.xy) * _RippleStrength;
                half3 normal = normalize(half3(tilt.x, 1.0, tilt.y));

                // Depth proxy from the channel profile: 0 at the bank, 1 in the middle.
                half depth = smoothstep(_RiverHalfWidth, _RiverHalfWidth * 0.3, abs(xz.x));
                half3 body = lerp(_ShallowColor.rgb, _DeepColor.rgb, depth);
                half alpha = lerp(_ShallowAlpha, _DeepAlpha, depth);

                float3 view = normalize(_WorldSpaceCameraPos - input.world);
                half fresnel = pow(1.0 - saturate(dot(normal, view)), _FresnelPower);
                float3 reflected = reflect(-view, normal);
                // Grazing reflections lean toward the zenith blue plus a bright highlight, so distant water reads
                // as clear sky blue rather than the cyan horizon haze.
                half3 sky = lerp(_HorizonColor.rgb, _ZenithColor.rgb, smoothstep(-0.05, 0.25, reflected.y));
                sky = lerp(sky, _ReflectionTint.rgb, _ReflectionTintBlend);
                half3 color = lerp(body, sky, fresnel * _ReflectionStrength);
                alpha = max(alpha, fresnel * _ReflectionStrength);

                Light sun = GetMainLight();
                half3 halfway = normalize(sun.direction + view);
                half glint = pow(saturate(dot(normal, halfway)), _GlintPower) * _GlintIntensity;
                // Stylized twinkles that do not depend on the sun angle: two drifting noise fields whose product
                // only peaks at rare points, so a few bright specks shimmer across the water from any view.
                half twinkle = MeadowValueNoise((xz - flowA) * _SparkleScale) * MeadowValueNoise((xz - flowB * 1.7) * _SparkleScale * 1.3 + 7.0);
                half sparkle = smoothstep(_SparkleThreshold, _SparkleThreshold + 0.06, twinkle) * _SparkleIntensity * depth;
                color += sun.color * (glint + sparkle);
                alpha = saturate(alpha + glint + sparkle);

                // Foam: a broken, flowing line along each bank and around docks and the boat.
                half foamNoise = MeadowFbm((xz - downstream * (time * _FlowSpeed * 0.8)) * _FoamNoiseScale);
                float bankDistance = _RiverHalfWidth - abs(xz.x);
                float objectDistance = min(BoxDistance(xz, _FoamBoxLeftDock), min(BoxDistance(xz, _FoamBoxRightDock), BoxDistance(xz, _FoamBoxBoat)));
                half bankFoam = 1.0 - smoothstep(_BankFoamWidth * 0.3, _BankFoamWidth, bankDistance + (foamNoise - 0.5) * _BankFoamWidth);
                half objectFoam = 1.0 - smoothstep(_ObjectFoamWidth * 0.3, _ObjectFoamWidth, objectDistance + (foamNoise - 0.5) * _ObjectFoamWidth);
                half foam = saturate(max(bankFoam, objectFoam)) * smoothstep(0.45, 0.7, foamNoise + 0.2);
                color = lerp(color, _FoamColor.rgb, foam);
                alpha = max(alpha, foam);

                return half4(MixFog(color, input.fog), alpha);
            }
            ENDHLSL
        }
    }
    Fallback Off
}
```

## Included helpers (`MeadowGround.hlsl` in the source project)

```hlsl
float MeadowHash(float2 p)
{
    return frac(sin(dot(p, float2(127.1, 311.7))) * 43758.5453);
}
float MeadowValueNoise(float2 p)
{
    float2 cell = floor(p);
    float2 f = frac(p);
    f = f * f * (3.0 - 2.0 * f);
    return lerp(lerp(MeadowHash(cell), MeadowHash(cell + float2(1, 0)), f.x),
                lerp(MeadowHash(cell + float2(0, 1)), MeadowHash(cell + 1), f.x), f.y);
}
float MeadowFbm(float2 p)
{
    return MeadowValueNoise(p) * 0.57 + MeadowValueNoise(p * 2.03 + 17.0) * 0.29 + MeadowValueNoise(p * 4.1 + 31.0) * 0.14;
}
```

## Script side: foam around moving objects

`RiverWater` sets three `float4` boxes (centre x, centre z, half x, half z) with a `MaterialPropertyBlock` in `LateUpdate`: two static docks and the boat. Pass the tracked transforms in explicitly (`TrackBoat(boat)`) instead of looking them up by name. For more objects, switch to a small array (`SetVectorArray`) with a fixed maximum.

## Flow direction

`_FlowDirection` is the downstream direction in world xz. Both ripple layers, the twinkles and the foam noise advect along it; the second ripple layer drifts slightly across the current. Choose it from the **player's default view**, not the world axes: find which world direction is screen-right for the default camera (`camera.transform.right`) and set downstream accordingly. In QB-001 the default camera looks +X, so screen-right is world −Z and `(0, -1)` makes the water run left to right.

## Porting notes

- **Built-in pipeline:**
  - Swap `Core.hlsl`/`Lighting.hlsl` for `UnityCG.cginc`/`Lighting.cginc`.
  - Read the sun from `_WorldSpaceLightPos0`.
  - Use `UnpackNormal` from UnityCG.
- **With a depth texture available:** replace the |x| proxy with the scene-depth difference `LinearEyeDepth(sceneDepth) - surfaceEyeDepth`. That also gives intersection foam around arbitrary objects, so the foam boxes are no longer needed.
- **HLSL reserved words:** `point`, `line`, `triangle` and `sample` cannot be used as identifiers.
