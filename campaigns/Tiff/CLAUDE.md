# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this folder is

Content production for **Tiff**, an AI UGC TikTok persona (try-on girly: going-out fits, gym sets, cozy fits, trinkets; TikTok Shop affiliate). Goal one is followers, goal two is shop sales. There is no app to build or test here: the work is prompts, generated images/videos, ffmpeg scripts and two self-contained HTML planning pages.

**Read `../../masterUGC.md` first** (repo root). It is the source of truth for the pipeline, Flow automation tricks, credit costs and guardrails. `.claude/skills/MakeSlideshow/SKILL.md` (repo root) is the source of truth for slideshows.

## Pipeline (summary of masterUGC)

Character sheet → outfit sheet (Codex CLI) → start frame (Nano Banana Pro in Google Flow, 0 credits) → video (Omni 1.1 Flash in Flow, ~15–20 credits per 10 s) → local QA → stitch → finish in CapCut/TikTok by hand (hook text, sound, AI label).

- Flow is driven in the user's Chrome. Always read "Generating will use N credits" before submitting; never reroll before checking the frame grid and transcript. Prefer free ffmpeg recuts over rerolls.
- Photo slideshows/carousels cost 0 Flow credits: slide 1 = Tiff, other slides = moody low-light b-roll with no person.

## Tools (`tools/`, run with Git Bash; paths relative to `campaigns/Tiff`)

```bash
bash tools/gen_image.sh OUT.png PROMPT.txt REF1 [REF2 ...]   # Codex CLI image gen; copies newest PNG from this run's ~/.codex session folder
bash tools/stitch.sh OUT.mp4 a.mp4:7.5 b.mp4:2-9 c.mp4:full   # 720x1280 jump-cut concat + loudnorm -14 LUFS
bash tools/upscale.sh clip.mp4 [1080|4k|both]                 # Real-ESRGAN (tools/realesrgan, local GPU), keeps audio
python tools/transcribe.py clip.mp4 [--words]                 # faster-whisper QA; pipes PCM from ffmpeg (PyAV is broken here)
python ../../.claude/skills/MakeSlideshow/add_text.py IN OUT "title" ["item1" ...]  # slideshow text overlay
```

`gen_image.sh` finds the Codex binary through `Get-AppxPackage OpenAI.Codex`, so it survives app updates. Codex runs can go in parallel (`&`); each run only reads its own session folder.

## Identity refs

Use `characterSheet/codex/outfit_sophie_black.png` + `characterSheet/codex/Tiff_comfy_sheet_nosunglasses.png` for her face. Always write "No sunglasses" (old sheets show them). Codex blocks sports-bra/bikini outfits; use NB Pro in Flow for those, or a long-sleeve top + leggings in Codex.

## Folder layout

- `images/slideshow_<slug>/` — one per slideshow: `prompts/sN_*.txt`, `codex/`, `nbpro/` (each with `text/` overlays), `text.tsv`, `caption.md`, contact sheets, and `final/`. **`final/` is the user's: they copy their picks in. Never fill it.**
- `images/carousel/`, `images/pfp/` — older carousel and profile pics.
- `videos/` — finished mp4s. **Every new finalized video goes directly into `videos/` (flat, no subfolder) as soon as it passes QA**, named `tiff_<topic>_<outfit>_<audio|muted>_<len>s.mp4`; no second copy left in a work folder; finished work folders and dupes move to `videos/_to_delete/`.
- `_archive/day_*` — past day work folders (plan, prompts, frames, clips, NOTES.md). Look here for prompts that already worked.
- `characterSheet/` — **every new character/outfit sheet goes here directly, never in a day/work folder.** `codex/Tiff_outfit_NN_<slug>.png` (Codex), `nano_banana/Tiff_outfit_NN_<slug>_nb.jpg` (NB Pro), prompt in `outfit_prompts/oNN.txt`. NN = next free number (continue after the highest existing). Same NN for both tools' versions of one outfit.
- `comparison/` — Codex vs grain bake-off page.

## HTML planning pages

- `tiff_november_calendar.html` — the month plan. Single file, vanilla JS in an IIFE. Data arrays near the top of the script: `SLOTS` (6 daily slots; `ORDER` sorts by time, Slideshow stays last so saved checkbox ids are stable), `DAYS` (each day's 6 slot strings: leading `$` = shop-linked, `+` = b-roll, `[Series]` tag), `B` (full briefs per day/slot), `PRODUCTS`, `ACCOUNTS`. Tabs are `.tab[data-tab]` buttons toggling `<section id>`s. Checkbox state lives in `localStorage` key `tiff-nov`. Colors are CSS tokens on `:root` with a dark-mode override; keep new UI on those tokens.
- `tiff_november_board.html` — production status board.

## Content rules (keep the account alive)

AI label on every post; no first-person wear/experience claims; no AI before/after results; real product images in shop posts; only prices confirmed in the listing; fitted is fine but no lingering body crops or suggestive captions; supplements: label facts only. TikTok Shop posts should use Commercial Music Library sounds.
