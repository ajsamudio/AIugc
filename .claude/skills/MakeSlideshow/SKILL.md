---
name: MakeSlideshow
description: Make a 6-slide TikTok photo slideshow for a persona (default Tiff) - 1 persona selfie/hook slide + 5 topic images (e.g. "my favorite high protein meals", "my favorite books", "my favorite ab exercises"). Use when the user types /MakeSlideshow or asks for a "my favorite X" slideshow/carousel.
---

# /MakeSlideshow <topic> [slides] [lighting] [engine]

**Slide count is up to the user (usually 6 or 2; default 6).** N slides = 1 persona slide + (N-1) topic images.
- **2-slide mode:** slide 1 = persona, slide 2 = ONE topic image with all items as a numbered list on it
  (e.g. "my go-to high protein meals" + 1-5). Prompt that image with "the subject sits in the lower half of the frame,
  calm dark empty space in the upper half" so the list has room. Text: `add_text.py IN OUT "<title>" "item1" "item2" ...`
  (2+ extra args = numbered list).

Format copied from the "pov: nobody understands the way you eat" accounts: slide 1 = the persona in a moody
mirror selfie or candid shot (black gym set, warm LED-strip kitchen/studio, hook text added later in TikTok),
slides 2-6 = five images of the topic itself, all in the SAME lighting/palette so the post looks like one set.

Read `masterUGC.md` (Step 2 + 2b) first. Persona refs (Tiff): `campaigns/Tiff/characterSheet/codex/outfit_sophie_black.png`
+ `campaigns/Tiff/characterSheet/codex/Tiff_comfy_sheet_nosunglasses.png`. Always say "No sunglasses".

## Steps
1. **Topic -> 5 items.** Pick 5 specific, visually distinct items (e.g. salmon rice bowl, steak & eggs...). Show the list to the user only if the topic is vague.
2. **Lighting.** Default: low, moody, warm (LED cabinet strips, lamp, candle). Use the user's choice if given. Use the same light words in all 6 prompts.
3. **Folder:** `campaigns/<Persona>/images/slideshow_<topic_slug>/` with `prompts/`, `codex/`, `nbpro/`, and an EMPTY `final/`. The user copies the picks into `final/` themselves. Never fill it or choose for them.
4. **Prompts** (`prompts/sN_<subject>.txt`):
   - s1 (persona): "Vertical 9:16 photo ... The SAME woman as the attached reference images: identical face, hair and body. No sunglasses. [outfit] [setting tied to the topic: cooking at stove / reading on couch / on a mat] [light]. Natural skin texture, flyaway hairs, amateur phone photo, natural grain, not studio, no ring light, no text, no logos." For a mirror selfie, add: "holding exactly one phone at chest height, face fully visible above it, slight mirror smudges".
   - s2..sN (topic): "Vertical 9:16 photo. [item + 3-5 specific props and where they sit] [light]. No people anywhere in the frame, no hands. Shot on an iPhone, amateur and candid, natural grain, soft shadows, slightly underexposed and moody, low warm light. Not a stock photo, not studio, no text, no logos, no watermark." (Books/exercises: covers must have no readable titles; exercise slides may show the persona only if the user asks - then attach refs.)
5. **Generate** (engine: `both` by DEFAULT, so the user can pick per slide when uploading; `codex` or `nbpro` only if asked):
   - Codex: all 6 in parallel, absolute paths, refs only on s1:
     `bash <abs>/campaigns/Tiff/tools/gen_image.sh <abs>/codex/s1_x.png <abs>/prompts/s1_x.txt <ref1> <ref2> &`
   - NB Pro: Google Flow in Chrome, Image mode, Nano Banana Pro, 9:16 (0 credits). s1 with both refs uploaded; s2-s6 with no refs. Save to `nbpro/`. Never press Enter in a prompt box you don't know.
   - Codex blocks a sports bra + shorts outfit on s1 (moderation "sexual", 2026-11-06). Use NB Pro for revealing gym outfits, or have Codex use a long-sleeve top + leggings.
   - Flow tips: clicks can miss if the window resizes, so screenshot before each send. Upload refs by patching `HTMLInputElement.prototype.click` and then calling file_upload. "Add to prompt" adds only one asset at a time. Download with `fetch(tile.src)` → `<a download>`, then move the file from ~/Downloads.
6. **QA:** open each image. Reroll (free) for text/logos, extra hands/people, warped food/props, wrong face, sunglasses.
7. **Text overlay (always, every slide):** match campaigns/Tiff/images/carousel - one short lowercase line per slide.
   Write `text.tsv` (`name<TAB>text`): s1 = the slideshow TITLE (e.g. "my go-to high protein meals"); each topic slide = ONLY its own
   item, numbered: "1. salmon rice bowl", "2. steak & eggs"... No subtitles, no other items. Then for each engine (codex=png, nbpro=jpeg):
   `python <abs>/.claude/skills/MakeSlideshow/add_text.py <engine>/<name>.<ext> <engine>/text/<name>.jpg "<text>"`
   This draws white Segoe UI Bold text with a soft shadow at 17% from the top, sized at about 6% of the width and wrapped to 78% of it. That keeps it big and readable but not covering the photo, and it stays under TikTok's top tabs.
8. **Caption (always):** write `caption.md` in the folder, thinking like a senior social designer:
   - **Title:** 3 options under 40 characters, lowercase, the first one recommended. It repeats the slide 1 text, with 1-2 emojis at most.
   - **Description:** a one-line hook, then the numbered list with one emoji per item, then a two-part call to action: an easy comment ("which number are you making first? comment 1-5 👇🫶", reworded for the topic) and a save ("save this for your next ___ 🛒✨").
   - **Then** 6-8 hashtags, mixing broad and specific ones.
   - **Emojis:** soft Gen Z and cozy (🤍🫶✨🧸🍓 plus one per topic item) to fit the dim, warm look. No 🔥💯 or other loud ones.
   - **Also** give the full caption in chat so the user can paste it straight in.
9. **Deliver:** make a contact sheet (codex row on top, nbpro row below) from the `text/` images with ffmpeg hstack/vstack, and send it. Say which slides look best from each engine. Offer `/addGrain` (run it on the images before adding text) and a short caption.
