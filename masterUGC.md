# masterUGC: AI UGC production workflow

> Source of truth for making AI UGC videos in this repo. Written for humans **and** agents (Claude Code, Codex).
> Proven on Tiff · Day 1 (2026-10-26): 2 talking vlog videos + 1 carousel, 60 Flow credits, 0 rerolls.
> Visual version: [masterUGC.html](masterUGC.html). Older notes: PIPELINE.md, TWEET_LEARNINGS.md, archive/MasterOmniPrompt.md (merged into §3b).

---

## 0. TL;DR pipeline

```
CHARACTER SHEET ──► OUTFIT SHEETS ──► START FRAME ──────► VIDEO CLIPS ──► QA ──► STITCH ──► FINISH
 (have it)          Codex CLI         Nano Banana Pro     Omni 1.1 Flash  local  ffmpeg    CapCut/TikTok
                    0 cr*             (Flow) 0 cr         15 cr / 10s     free   free      free
```
\* Codex image gen is billed against the ChatGPT/Codex plan (no per-image price seen; about 20k tokens per image).

**Per finished ~20s video: 2 × 10s clips = 30 Flow credits.** Images are free.

**Photo carousels:** slide 1 = persona start frame (NB Pro, Step 2); slides 2+ = moody b-roll with no person (**Codex**, Step 2b). 0 Flow credits.

---

## 1. Tools and where they live

| Role | Tool | How it's driven | Notes |
|---|---|---|---|
| Plan, scripts, prompts, QA | Claude Code (this repo) | chat | Writes files under `campaigns/<persona>/dayNN/` |
| Outfit / character sheets | **Codex CLI**, GPT Image | `campaigns/tiff/gen_image.sh` | Best **face consistency** |
| Start frame ("before image") | **Nano Banana Pro** in Google Flow | Chrome → flow.google.com, Image mode | Best **realism** (messy rooms, mirror smudges, grain). 0 credits |
| Carousel b-roll (no person) | **Codex CLI**, GPT Image | `campaigns/Tiff/tools/gen_image.sh`, no refs | Beat NB Pro 5/5 in the 2026-10-29 side-by-side |
| Video | **Omni 1.1 Flash** in Google Flow | Video → **Frames** mode, start frame only | Says scripts word for word, adds natural micro-actions |
| QA | ffmpeg + faster-whisper | `campaigns/tiff/transcribe.py` | Frame grid, transcript, silence detection |
| Stitch | ffmpeg | `campaigns/tiff/stitch.sh` | Trims dead air, jump-cuts, loudnorm −14 LUFS |
| Finish | CapCut / TikTok | by hand | Hook text, sound, captions, **AI label** |

Codex binary (Windows Store install):
`/c/Program Files/WindowsApps/OpenAI.Codex_26.1021.3705.0_x64__2p2nqsd0c76g0/app/resources/codex.exe`
(the version folder changes when the app updates; find it with `Get-AppxPackage *codex*`).

---

## 2. Folder layout

```
campaigns/<persona>/
  refs/                 original character sheets (never regenerate)
  outfits/              outfitN.png (Codex) + nanobanana/ + compare_*.jpg
  gen_image.sh          Codex image generation wrapper
  transcribe.py         Whisper transcript for QA
  stitch.sh             jump-cut + loudnorm
  dayNN/
    plan.md             slot, scripts, actions, on-screen text
    prompts.md          exact Omni prompts
    frames/             start frames (+ prompt .txt files)
    clips/              raw Omni clips (1A.mp4 …) + *_grid.jpg
    (no final/: postable mp4s go straight to campaigns/<persona>/videos/01_ready_to_post/,
     one copy only. Once a video is posted, the dayNN work folder moves to videos/_to_delete/;
     copy reusable sheets to sheet/ first)
    carousel/           carousel slides
    NOTES.md            what happened, what to change
```

---

## 3. Step by step

### Step 1 · Outfit sheets (Codex CLI)
Inputs: the persona's original sheets in `refs/`. Prompt template (`outfits/oN.txt`):
```
Character reference sheet of the SAME woman as the attached reference sheets: identical face, [eyes],
[hair], [skin], [signature accessories]. Same layout as the reference: wide 16:9 image, plain light grey
seamless studio background, four panels left to right: full body front view, full body three-quarter view,
full body back view, then a tight face close-up from the collarbone up. Soft even studio light, natural
skin texture with visible pores, realistic photo, no text, no labels.
Outfit N, "[name]": [every garment, colour, material, shoes, bag, jewellery].
```
Run (parallel is fine):
```bash
bash campaigns/tiff/gen_image.sh outfits/outfit1.png outfits/o1.txt refs/tiff_sheet_white.jpg refs/tiff_sheet_red.jpg
```
Check: face matches the original close-up; every garment present. Reroll if not (free).

### Step 2 · Start frame (Nano Banana Pro in Flow)
Flow → Image → **Nano Banana Pro**, 9:16, x2 (0 credits).
**References: both ORIGINAL sheets + the outfit sheet.** With only the outfit sheet, the face drifts.
```
Vertical 9:16 casual front-camera phone selfie video still (the phone itself is NOT visible). The SAME
woman as the attached images: identical face, [identity markers]. She wears [outfit]. [Location with
real clutter], framed from mid-chest up, slightly off-center, arm's-length, [light]. [Expression], about
to start talking. Natural skin texture with visible pores, slight shine, flyaway hairs. Amateur phone
photo, not studio, no ring light, no text.
```
For mirror OOTD / carousel: "full-length mirror selfie … holding her phone at chest height (exactly one phone, face fully visible above it) … slight mirror smudges".
Pick the more amateur-looking of the 2. Download 1K (2K is a free upscale).

### Step 2b · Carousel b-roll (Codex CLI)
Quote/vibe carousels: **only slide 1 shows the persona** (Step 2 frame + hook text). Slides 2–4 are vibe shots with nobody in them (coffee + flowers, pilates studio, city view, fruit stand, ocean view…), in low, moody light. Make them with **Codex**, not NB Pro: the user picked Codex for 5/5 slides in a side-by-side, because NB Pro added garbled sign text and odd reflections.
Prompt (`frames/bN_<subject>.txt`):
```
Vertical 9:16 photo. [Scene + 3–5 specific props and where they sit]. [Low light source: lamp, candles,
blue hour, golden hour side light]. No people anywhere in the frame, no hands. Shot on an iPhone,
amateur and candid, natural grain, soft shadows, slightly underexposed and moody, low warm light.
Not a stock photo, not studio, no text, no logos, no watermark.
```
Run every slide in parallel, with no refs. **Use absolute paths**: the script `cd`s into `tools/`, so relative paths fail with Codex saying "couldn't read".
```bash
bash /abs/campaigns/Tiff/tools/gen_image.sh /abs/.../frames/h20_b1_coffee_flowers_codex.png /abs/.../frames/b1_coffee_flowers.txt &
```
Output is 941×1672 PNG. Check for text, people or hands, and warped props. Reroll for free if needed.

### Step 3 · Video (Omni 1.1 Flash, Frames mode)
Flow → Video → **Frames** → Start = the frame, 9:16, 720p, **10s** → check "Generating will use **15 credits**".
**Use the same start frame for every clip of one video** so the jump cut looks like a real vlog cut.
```
authentic UGC vlog clip, handheld front-camera selfie, vertical. continue exactly from the start frame:
same woman, same [place], same outfit, [signature accessories]. she is already holding the phone at
arm's length and talks straight to camera. delivery: [ONE word]. she says exactly: "[script]".
around second [N] she [one small action], then [back to camera]. her voice: [FIXED voice line].
one continuous shot. no text, no captions, no music. slight handheld drift, [ambient sound],
built-in phone mic sound.
```
Rules:
- **Script ≤ 25 words per 10s clip** (28 words ran right up to 10.0s with no breathing room).
- One delivery word. One action per clip at a named second.
- Voice line identical across every clip of a persona. Always state the accent explicitly (Omni drifted British once). Tiff: *"warm, relaxed Mexican-American woman in her mid-20s from Southern California, natural SoCal Latina accent, American English (not British), slightly low, casual and a little dry, natural pace"*.
- "already holding", "exactly one phone", "no text/captions/music": each one prevents a known failure.
- **Mirror selfies: the phone IS the camera.** Keep it at face or chest height for the whole clip. Never prompt "lower/drop the phone": she flips it flat and then yanks it back up (intro clip C fidget). From a start frame with the phone covering her face, Omni also ignores "lowers it at second 1" (intro clip A). For a face reveal, start from a frame where the phone is already low and the face is visible.
- **Stutters/repeats:** Omni sometimes doubles a phrase ("let's chat let's chat", "exactly how … how"). It's worse when an opening action delays speech and the words get crammed. Start speaking by second 0.5, and use ≤ 18 words when the clip opens with an action.
- 360 turns / spins: use a separate clip with a static camera (no phone in hand) and timestamps (`5-8.5s: one slow complete 360`). Worked first try.

### Step 4 · QA (local, free)
```bash
ffmpeg -i clips/1A.mp4 -vf "fps=1,scale=240:-1,tile=5x2" -frames:v 1 clips/1A_grid.jpg   # face/artifacts
python transcribe.py clips/1A.mp4                                                         # script match
ffmpeg -i clips/1A.mp4 -af silencedetect=n=-35dB:d=0.4 -f null -                          # dead air / where speech ends
```
Reject on: face drift, extra fingers or a second phone, on-screen text, script mismatch, cut-off last word.
**Whisper hides stutters**: a repeated phrase shows up as one stretched word (e.g. "let's" lasting 0.96s). Flag any word longer than about 0.6s with `transcribe.py --words`, then check a 50ms loudness trace for double onsets, and *listen* to every clip's lines.
**Recut before reroll** (free): cut at a sentence boundary just before the flaw, drop a weak clip, or move the lost line to on-screen text. The intro v2 (16s recut) beat the 29s v1. Reroll (15 cr) only when no clean cut exists.

### Step 4b · Product b-roll (Remotion, free)
Listing photos → `remotion/public/dNN/`, add a composition in `remotion/src/Root.tsx` (reuse `ColorBroll`: ~1.3s per photo, spring slide/fade transitions, slow push-in, color-name pills). Render, then add a silent audio track so `stitch.sh` can concat it:
```bash
cd remotion && npx remotion render src/index.ts d01-color-broll ../campaigns/tiff/day01/clips/broll_remotion.mp4 --codec=h264 --crf=18
ffmpeg -i clips/broll_remotion.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -map 0:v -map 1:a -c:v copy -c:a aac -shortest out.mp4
```
Don't flash product photos faster than ~1s each: viewers can't read them.

### Step 5 · Stitch
```bash
bash stitch.sh final/dayNN_postX.mp4 clips/1A.mp4:9.0 clips/1B.mp4:full   # clip:end_sec trims dead air
```
Output: H.264 CRF 18, AAC 192k, loudnorm −14 LUFS (raw Omni audio is ≈ −29 dB).

### Step 6 · Finish (by hand)
On-screen hook text, trending sound, caption, **TikTok AI-generated label ON**, schedule per the calendar slot.

---

## 3b. Prompt playbook (merged from MasterOmniPrompt.md, Oct 16 learnings)

### Non-talking / scene clips (no selfie)
```
authentic vertical iPhone video, [CAMERA SETUP], one continuous shot, no cuts.
continue exactly from the start frame: same woman, [outfit, every piece], no sunglasses.
0-[X]s: [beat 1: one action + one expression].
[X]-[Y]s: [beat 2].
[Y]s-end: [look at camera + micro-expression].
[anti-AI checklist below]
```
- 3–4 beats max per 10s, one action per beat, use timestamps. List the outfit piece by piece every time.
- Camera setups that work: `static locked-off camera at chest height across the room` (tripod) · `static camera resting on the desk slightly to the side` (desk) · `handheld front-camera selfie at arm's length, her arm partly visible at the frame edge` (selfie).

### Recreating a trend / outfit-transition video (copy the ref 1:1)
When the user sends a reference video to "make Tiff in", **copy its movement and its transition move 1:1**. Don't invent a different (safer) transition.
- Watch the ref at 2 fps around the cut (`/watch --start --end`) and write down, beat by beat, what the body does, with timestamps. Example: the robe → glam ref (jessibuilds, 2026-11-03) uses a **punch toward the camera** as the transition. I swapped it for "covers her face with her hands", and the user rejected that.
- Clip A prompt = the ref's beats up to the cut, ending ON the transition move (e.g. `at 4s she throws a quick punch straight at the camera lens, fist filling the frame`). Clip B prompt = the ref's beats after the cut, starting from the matching end of that move (the fist pulling back out of frame to reveal the new outfit).
- Cut on the frame where the move covers the most of the frame (fist closest to the lens). That covers the outfit swap.
- Keep her on the same spot in clip A (`she stays on the same spot and does not walk toward the camera`). Otherwise her size jumps at the cut (robe clip A walked ~1.35x closer and needed a punch-in fix in ffmpeg).
- Make the glam start frame by feeding NB Pro the robe start frame + "recreate exactly, only change her look". This locked the hallway and camera perfectly.

### Known failures and their fixes
| Failure | Cause | Fix |
|---|---|---|
| A phone on a tripod appears in the scene | Prompt mentioned a "propped phone" | Describe the camera only by angle; end with `no phone, tripod, or camera anywhere in the scene`; check the start frame for phones |
| Warped pan + a second phone | One clip asked for a rear view and then a swing to selfie | Split into 2 clips and cut them together; never "camera swings around / turns 180" |
| Clothes float, room never gets clean | "Timelapse" + 6 tasks in one clip | No timelapses: one task per clip, a separate start frame for each state (messy → half → clean), speed it up in the edit; `objects only move when her hands touch them` |
| Props drift | Prop location not pinned | Name each prop's position the same way in the frame prompt and the video prompt |
| Phone fidget / stutter | See Step 3 rules | Phone stays still in mirror clips; speech starts by 0.5s |
| Extra cup appears, then two cups merge into one | Prompt brought in a new container ("ice cubes **from a glass**") | Every container must be in the start frame already. Never name a new vessel in the video prompt; say "ice is already in the shaker". One cup in the frame = one cup in the clip |
| Logo on the shaker/tub smears or vanishes when shaken | Omni can't hold AI-made label text in fast motion | Start frame: "plain clear shaker with no logo or text". Keep the branded tub still on the counter, never handled fast. Show the real label only as a listing-photo insert in the edit |
| Loud hiss in "silent" clips | Omni room tone (≈ −51 dB) boosted ~35 dB by loudnorm | Never loudnorm a no-speech clip. Strip the audio (`anullsrc`) for silent/vibe videos |
| Face is flat for a product/hype video | Prompt asked for "deadpan" | Product GRWMs: "big bright over-the-top influencer smile, wide eyes, exaggerated 'obsessed' reactions" in **both** the start frame and every beat |
| Clip 2+ opens by replaying the start-frame pose (e.g. picks up scoop AND cup again) | Every clip of one video starts from the same frame | In the stitch, trim each later clip's opening until its first new action (usually 0.5–1s). Check the frames around every cut |
| Wrong listing image used as a reference | Picked a listing photo by file number | Look at a contact sheet and rename the chosen photo (`<product>_<flavor>.jpg`) before upload. Never upload a claims/ingredient graphic |

### Cute-factor beats (pick 2–3 per video)
- **Micro-expressions (best hook in the first 1s):** pouty lips + big eyes, smirk then looks away, playful eye roll, scrunches nose and smiles, tucks hair behind ear while looking up.
- **Movement (shows the outfit):** slow spin with hair swinging, hair flip, small sway, hands in sweatpants pockets with weight on one hip.
- **Relatable:** dramatic sigh, sip of an iced latte, an "are you seeing this" glance, a shrug.
- End on eye contact + a micro-expression (loops and replays). Movement every 2–3s. Flirty-cute, never suggestive.

### Anti-AI checklist (add to every video prompt)
```
natural real-time speed, realistic body weight and physics, objects only move when touched,
props stay consistent and never morph, natural body proportions, normal hands with five fingers,
consistent background, no other people, no text, no captions, no music.
```
**Reject if:** a second phone appears · extra fingers · objects float · face or outfit changes · text appears · background warps · motion looks slow-mo.

---

## 4. Pricing (what we've actually seen)

### Google Flow (Google AI Pro plan, +50 Flow credits/day)
| Item | Credits |
|---|---|
| Omni 1.1 Flash · 720p · 10s | **15** |
| Omni 1.1 Flash · 720p · 8s | 12 |
| Omni 1.1 Flash · 360p · 8s | 6 |
| Nano Banana Pro / 2.1 / 2 Lite image (any count) | **0** |
| **One ~20s video (2 × 10s)** | **30** |
| Day 1 total (2 videos + carousel) | 60 |

Two videos a day = 60 credits/day, slightly over the daily +50.

### Codex CLI (GPT Image)
No per-image price shown; uses ChatGPT/Codex plan limits. ≈ 20k tokens and 1–2 min per image.

### Higgsfield (candidates to test; **prices TBD**, fill in)
Account checked 2026-10-26: free plan, 0 credits. Image-to-video models relevant to talking UGC:

| Model (id) | Start frame | Voice/audio ref | Lengths | Res | Why test it | Price / 10s 720p |
|---|---|---|---|---|---|---|
| Seedance 2.0 (`seedance_2_0`) | ✅ | ✅ audio_references | 4–15s | 480p–4k | Identity + **voice reference** (can lock one voice) | |
| Seedance 2.0 Mini (`seedance_2_0_mini`) | ✅ | ✅ | 4–15s | 480/720p | Budget version | |
| Seedance 2.5 (`seedance_2_5`) | ✅ | ✅ | 4–**30s** | to 1080p | One 20s take, no stitching; extension mode | |
| Seedance 1.5 Pro (`seedance1_5`) | ✅ | ❌ | 4/8/12s | to 1080p | Cheaper baseline | |
| Wan 2.6 (`wan2_6`) | refs only | ✅ | 5/10/15s | 720/1080p | Open-weight, stylized | |
| Kling 3.0 (`kling3_0`) | ✅ | ❌ | 3–15s | std/pro/4k | Strong motion, multi-shot | |
| Grok Video 1.5 (`grok_video_v15`) | ✅ | ✅ | 2–15s | to 1080p | Audio reference | |
| MiniMax H3 Max (`minimax_h3_max`) | ✅ | ✅ | 5–15s | 768p | Fast, audio ref | |

**Compare on:** cost per finished 20s video, script accuracy (Omni: 4/4 word for word), voice consistency across posts, face hold, reroll rate (Omni: 0/4).

---

## 5. Guardrails (keep the account alive)
- AI-generated label on every post; "AI creator" in the bio.
- No first-person product experience claims ("I've worn these all month"). Use listing features.
- No AI before/after results. Show real product images in shop posts.
- Only quote prices confirmed in the listing ("$12" in Day 1 is a category ballpark, not a price claim).
- "For the Boys" content: playful, not suggestive.

---

## 6. Agent notes (Claude Code / Codex)
- **Read this file first**, then `campaigns/<persona>/dayNN/plan.md` and the persona calendar (`tiff_november_calendar.html`).
- Flow automation (Chrome):
  - Uploads: patch `HTMLInputElement.prototype.click` so file inputs attach to the DOM instead of opening the native picker, then use file_upload.
  - Picker: type the file name in **Search assets**, then click **Add to prompt** (clicking the row only previews it).
  - References clear after each submit, so re-add them every time.
  - Always read "Generating will use N credits" before submitting; settings carry over between modes. Video: set **Frames** and **x1** (x2 doubles to 30 cr).
  - Frames-mode Start picker doesn't list generated images by name: upload the picked frame with a unique name (`dNN_skit_start.jpg`) and search for it.
  - Image downloads: the tile `<img>` is the full 1K file; `fetch(img.src)` → blob → `<a download="name">` saves every option with your own names in one call. (The row download button does nothing for images.)
  - Video downloads: the row download button works. Files land in `~/Downloads`; move them into `clips/` straight away.
- faster-whisper on this machine: PyAV is incompatible, so `transcribe.py` pipes PCM from ffmpeg.
- Never spend credits on rerolls without checking the frame grid and transcript first.

## 7. Changelog / learnings
- 2026-10-26 · Day 1: Codex sheets + Codex start frames + Omni. 4/4 clips first try.
- 2026-10-26 · Sheet bake-off: Codex = best face match; Nano Banana Pro nearly as good **when given the original sheets**; NB wins on realism → new split: **Codex sheets → NB start frames → Omni**.
- 2026-10-26 · Day 2: first full v2 run (NB Pro start frames → Omni). 2 videos + 3-slide carousel, 60 cr, 0 rerolls. Omni repeated one line once (4B); fixed with an in-clip jump cut instead of a reroll: find cut points with Whisper `word_timestamps=True` + `silencedetect=n=-38dB:d=0.15`.
- 2026-10-26 · Day 1 v2 (Shop Drop, [Every Color]): real TikTok Shop listing photos as b-roll + NB Pro color stills as a hook + 2 Omni clips. 30 cr, 0 rerolls. Rebuilt `gen_image.sh` (use `--image=FILE` per ref, prompt on stdin), `transcribe.py`, `stitch.sh`. Tiff: **no sunglasses** in generations (say it explicitly; the original sheets still show them). Flow uploads: hidden file input + synthetic `drop` event. Details: campaigns/Tiff/day01/NOTES.md.
- 2026-10-27 · Intro (5'6 wearing a S): Codex no-sunglasses sheet → NB frames → 3 Omni clips (45 cr). User QA caught a stutter (A) and a phone fidget (C, a prompt mistake). Fixed by a free recut to 16s. GRWM intro "let's chat" repeat also cut out. Details: the intro NOTES.md (now in videos/_to_delete/intro_workfolder).
- 2026-10-29 · Two quote carousels ("healing 20s", "be a good person"): Codex outfit sheets 06/07 → NB Pro hook frames → b-roll. The user wants the persona on slide 1 only. In a b-roll bake-off (Codex vs NB Pro ×2, 5 slides), **Codex won all 5** and is now the b-roll tool (Step 2b). 0 Flow credits.
- Next: test Higgsfield Seedance 2.0 with an audio reference to lock Tiff's voice.
- 2026-11-02 · Nov 3 RYSE GRWM v1 rejected: extra cup + merge, shaker logo vanished, hissy audio, deadpan face. Rules added to §3b Known failures. v2 = talking script + fake-bright energy + one container only.
- 2026-11-03 · Robe → glam transition (Codex sheets → NB Pro frames → 2 × 8s Omni, 24 cr). The user wanted the ref's movement and its **punch transition** copied 1:1, not the hands-over-face cover I used. Rules added in §3b "Recreating a trend". Kept as is, no regen.
