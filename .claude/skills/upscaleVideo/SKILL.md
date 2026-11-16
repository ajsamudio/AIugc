---
name: upscaleVideo
description: AI-upscale a generated video (Omni / Flow / Nano Banana / any mp4) to sharp 1080p or 4K locally with Real-ESRGAN on the user's RTX 3060, keeping the audio. Use when the user types /upscaleVideo or asks to upscale, sharpen, or "Topaz" a video.
---

# /upscaleVideo

Script: `C:/Users/Ajayy/OneDrive/Documents/WebCode/Claude/AIUGC/campaigns/Tiff/tools/upscale.sh`
(Real-ESRGAN binary lives in `tools/realesrgan/`, official xinntao v0.2.5.0 release, verified 2026-11-06.)

Args: `<video path> [1080|4k|both]` (default 1080 — TikTok caps at 1080p; 4K only as a master copy).

1. Run in the background (several minutes per 10s clip; ~2 min even for a 1s test):
   `bash ".../tools/upscale.sh" "<video>" <mode>`
   Output lands next to the input as `<name>_upscaled_1080p.mp4` / `_4k.mp4`, original audio kept.
2. Make a before/after face crop to check it:
   `ffmpeg -ss 4 -i <orig> -ss 4 -i <upscaled_1080p> -filter_complex "[0:v]scale=1080:1920,crop=540:540:270:300[a];[1:v]crop=540:540:270:300[b];[a][b]hstack" -frames:v 1 <dir>/compare_face.jpg`
   Read it; report sharper brows/lashes/hair vs any plastic skin.
3. If the user wants a final, move it to `campaigns/Tiff/videos/` per the folder rules.

What it does: downscale to true 720p → Real-ESRGAN x4plus per frame → lanczos down to 1080/2160 → light grain (noise=3) so skin isn't plastic → x264 crf16.
