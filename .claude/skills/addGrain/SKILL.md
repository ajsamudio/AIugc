---
name: addGrain
description: Add phone-camera film grain to one image, several images, or a folder of images with ffmpeg (no regeneration, face unchanged). Use when the user types /addGrain or asks to add grain/make AI images look less fake.
---

# /addGrain

Makes AI images (especially Codex/GPT Image) look less smooth and fake. It lowers saturation slightly, sharpens a little, adds film grain and a soft vignette, and saves a compressed JPEG.

## Steps
1. Take the image paths and/or folders from the user's message (args). If none were given, ask for them.
2. Strength: `light`, `medium` (default) or `heavy`. Use what the user says ("strong" = heavy, "subtle" = light).
3. Run (absolute paths, quoted):
   ```bash
   bash "C:/Users/Ajayy/OneDrive/Documents/WebCode/Claude/AIUGC/.claude/skills/addGrain/add_grain.sh" --strength medium "<path1>" "<path2-or-folder>"
   ```
   Folders: only top-level png/jpg/jpeg/webp files are processed.
4. Outputs go to a `grain/` subfolder next to each source as `<name>.jpg`. Originals are never touched.
5. Open one output with Read to check it, then list the output paths for the user.
