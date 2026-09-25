# Tileable Perlin-Worley noise baker (Unity editor reference)

Bakes an RGBA PNG: **R = Perlin-Worley shape**, **G = inverted Worley fBm detail**. Every octave doubles the cell count and wraps its lattice, so the texture tiles seamlessly. Values are histogram-normalized to 0..1 so `coverage` behaves predictably.

Adapt the paths, menu name, material property and namespace. Keep generation in an editor-only folder; the PNG is a generated artifact — rebake instead of hand-editing it. Import it **linear (sRGB off), Repeat, mipmapped, uncompressed**; sRGB or compression shifts the density threshold and bands the edges.

```csharp
using System;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace CloudSky.Editor
{
    // Bakes the tileable noise that the cloud sky shader projects onto its cloud plane.
    // R: Perlin-Worley shape (large puffs). G: inverted Worley fBm (cauliflower edge detail).
    public static class CloudNoiseBaker
    {
        public const string TexturePath = "Assets/Sky/CloudNoise.png";
        private const string SkyMaterialPath = "Assets/Sky/CloudSky.mat";
        private const string CloudNoiseProperty = "_CloudNoise";

        private const int TextureSizePixels = 256;
        private const int ShapeBaseCellCount = 4;
        private const int DetailBaseCellCount = 8;
        private const int OctaveCount = 3;
        private const float OctaveGain = 0.5f;
        private const uint ShapeSeed = 17u;
        private const uint DetailSeed = 71u;
        private const uint PerlinSeed = 131u;

        [MenuItem("Tools/Sky/Bake Cloud Noise")]
        public static void BakeAndAssign()
        {
            WriteNoiseTexture();
            ConfigureImporter();
            AssignToSkyMaterial();
            Debug.Log("Cloud noise baked to " + TexturePath + " and assigned to the sky material.");
        }

        private static void WriteNoiseTexture()
        {
            float[] shape = new float[TextureSizePixels * TextureSizePixels];
            float[] detail = new float[shape.Length];
            for (int y = 0; y < TextureSizePixels; y++)
            {
                for (int x = 0; x < TextureSizePixels; x++)
                {
                    var position = new Vector2((x + 0.5f) / TextureSizePixels, (y + 0.5f) / TextureSizePixels);
                    int index = y * TextureSizePixels + x;
                    float perlin = PerlinFbm(position, ShapeBaseCellCount, PerlinSeed);
                    float worley = InvertedWorleyFbm(position, ShapeBaseCellCount, ShapeSeed);
                    shape[index] = Remap(perlin, worley - 1f, 1f, 0f, 1f);
                    detail[index] = InvertedWorleyFbm(position, DetailBaseCellCount, DetailSeed);
                }
            }
            Normalize(shape);
            Normalize(detail);

            var texture = new Texture2D(TextureSizePixels, TextureSizePixels, TextureFormat.RGBA32, false, true);
            var pixels = new Color32[shape.Length];
            for (int index = 0; index < pixels.Length; index++)
                pixels[index] = new Color32(ToByte(shape[index]), ToByte(detail[index]), 0, byte.MaxValue);
            texture.SetPixels32(pixels);
            texture.Apply();
            try
            {
                File.WriteAllBytes(TexturePath, texture.EncodeToPNG());
            }
            finally
            {
                UnityEngine.Object.DestroyImmediate(texture);
            }
            AssetDatabase.ImportAsset(TexturePath, ImportAssetOptions.ForceUpdate);
        }

        private static void ConfigureImporter()
        {
            var importer = (TextureImporter)AssetImporter.GetAtPath(TexturePath);
            if (!importer) throw new Exception("Missing importer for " + TexturePath);
            importer.textureType = TextureImporterType.Default;
            importer.sRGBTexture = false;
            importer.alphaSource = TextureImporterAlphaSource.None;
            importer.wrapMode = TextureWrapMode.Repeat;
            importer.filterMode = FilterMode.Trilinear;
            importer.mipmapEnabled = true;
            importer.textureCompression = TextureImporterCompression.Uncompressed;
            importer.SaveAndReimport();
        }

        private static void AssignToSkyMaterial()
        {
            var material = AssetDatabase.LoadAssetAtPath<Material>(SkyMaterialPath);
            var noise = AssetDatabase.LoadAssetAtPath<Texture2D>(TexturePath);
            if (!material) throw new Exception("Missing sky material at " + SkyMaterialPath);
            if (!noise) throw new Exception("Missing baked cloud noise at " + TexturePath);
            material.SetTexture(CloudNoiseProperty, noise);
            EditorUtility.SetDirty(material);
            AssetDatabase.SaveAssets();
        }

        // Every octave doubles the cell count, so each octave still tiles over the unit square.
        private static float InvertedWorleyFbm(Vector2 position, int baseCellCount, uint seed)
        {
            float sum = 0f;
            float amplitude = 1f;
            float amplitudeTotal = 0f;
            for (int octave = 0; octave < OctaveCount; octave++)
            {
                sum += (1f - WorleyDistance(position, baseCellCount << octave, seed + (uint)octave)) * amplitude;
                amplitudeTotal += amplitude;
                amplitude *= OctaveGain;
            }
            return sum / amplitudeTotal;
        }

        private static float PerlinFbm(Vector2 position, int baseCellCount, uint seed)
        {
            float sum = 0f;
            float amplitude = 1f;
            float amplitudeTotal = 0f;
            for (int octave = 0; octave < OctaveCount; octave++)
            {
                sum += Perlin(position, baseCellCount << octave, seed + (uint)octave) * amplitude;
                amplitudeTotal += amplitude;
                amplitude *= OctaveGain;
            }
            return sum / amplitudeTotal * 0.5f + 0.5f;
        }

        // Distance to the nearest feature point, in cell units, clamped to [0, 1].
        private static float WorleyDistance(Vector2 position, int cellCount, uint seed)
        {
            Vector2 scaled = position * cellCount;
            int cellX = Mathf.FloorToInt(scaled.x);
            int cellY = Mathf.FloorToInt(scaled.y);
            float nearest = float.MaxValue;
            for (int offsetY = -1; offsetY <= 1; offsetY++)
            {
                for (int offsetX = -1; offsetX <= 1; offsetX++)
                {
                    int neighborX = cellX + offsetX;
                    int neighborY = cellY + offsetY;
                    uint hash = Hash(Wrap(neighborX, cellCount), Wrap(neighborY, cellCount), seed);
                    var featurePoint = new Vector2(neighborX + ToUnit(hash), neighborY + ToUnit(Hash(hash)));
                    nearest = Mathf.Min(nearest, (featurePoint - scaled).sqrMagnitude);
                }
            }
            return Mathf.Clamp01(Mathf.Sqrt(nearest));
        }

        // Gradient noise in [-1, 1] with a lattice that wraps at cellCount.
        private static float Perlin(Vector2 position, int cellCount, uint seed)
        {
            Vector2 scaled = position * cellCount;
            int cellX = Mathf.FloorToInt(scaled.x);
            int cellY = Mathf.FloorToInt(scaled.y);
            float localX = scaled.x - cellX;
            float localY = scaled.y - cellY;
            float bottom = Mathf.Lerp(
                Gradient(cellX, cellY, cellCount, seed, localX, localY),
                Gradient(cellX + 1, cellY, cellCount, seed, localX - 1f, localY), Fade(localX));
            float top = Mathf.Lerp(
                Gradient(cellX, cellY + 1, cellCount, seed, localX, localY - 1f),
                Gradient(cellX + 1, cellY + 1, cellCount, seed, localX - 1f, localY - 1f), Fade(localX));
            return Mathf.Lerp(bottom, top, Fade(localY)) * Mathf.Sqrt(2f);
        }

        private static float Gradient(int cornerX, int cornerY, int cellCount, uint seed, float offsetX, float offsetY)
        {
            float angle = ToUnit(Hash(Wrap(cornerX, cellCount), Wrap(cornerY, cellCount), seed)) * 2f * Mathf.PI;
            return Mathf.Cos(angle) * offsetX + Mathf.Sin(angle) * offsetY;
        }

        private static float Fade(float value) => value * value * value * (value * (value * 6f - 15f) + 10f);

        private static float Remap(float value, float fromMin, float fromMax, float toMin, float toMax) =>
            toMin + (value - fromMin) / (fromMax - fromMin) * (toMax - toMin);

        private static void Normalize(float[] values)
        {
            float minimum = float.MaxValue;
            float maximum = float.MinValue;
            foreach (float value in values)
            {
                minimum = Mathf.Min(minimum, value);
                maximum = Mathf.Max(maximum, value);
            }
            float range = Mathf.Max(maximum - minimum, Mathf.Epsilon);
            for (int index = 0; index < values.Length; index++)
                values[index] = (values[index] - minimum) / range;
        }

        private static int Wrap(int cell, int cellCount) => ((cell % cellCount) + cellCount) % cellCount;

        private static uint Hash(int x, int y, uint seed) => Hash((uint)x * 73856093u ^ (uint)y * 19349663u ^ seed * 83492791u);

        private static uint Hash(uint value)
        {
            value ^= value >> 16;
            value *= 0x7feb352dU;
            value ^= value >> 15;
            value *= 0x846ca68bU;
            value ^= value >> 16;
            return value;
        }

        private static float ToUnit(uint hash) => (hash & 0xFFFFFF) / (float)0x1000000;

        private static byte ToByte(float unit) => (byte)Mathf.RoundToInt(Mathf.Clamp01(unit) * byte.MaxValue);
    }
}
```

## Why these channels

- **Shape (R):** `remap(perlinFbm, worleyFbm - 1, 1, 0, 1)` — Perlin gives connected cloud masses, the inverted Worley term pushes billowy round lobes into the edge. Base 4 cells, 3 octaves, gain 0.5.
- **Detail (G):** inverted Worley fBm at base 8 cells. The shader subtracts `(1 - detail) * erosion`, which bites cauliflower notches into edges only (dense cores survive).
- 256² is enough: the shader tiles the shape at a low plane scale and the detail at ~2.7×; mips remove shimmer near the horizon.

Porting to another engine: the algorithm is self-contained (integer hash, wrapped lattice, F1 Worley distance, quintic-fade Perlin). Only `Texture2D`/importer/material calls are Unity-specific.
