# Master Omni Prompt Guide

Reference for every Flow → Omni 1.1 Flash video. Built from the first 4 Tiff videos (Oct 16 2026).

---

## 1. Workflow (do it in this order)

1. **Character sheet** (Codex CLI or Flow Nano Banana, 16:9, 4 panels). Codex held the face best. Save to `campaigns/<char>/sheet/`.
2. **Scene still** (Nano Banana, 9:16, 0 credits, x2). Generate the woman *already in the scene, in the first pose of the video*. Never use the studio sheet as the only ingredient: it makes the video stiff.
3. **Pick the still that looks least AI.** Look for a real-looking room with clutter, imperfect framing and skin texture.
4. **Omni video:** Video → **Ingredients** → 9:16 → 720p → 8s or 10s → **x1**. Ingredients = **scene still + character sheet**. Check that the line says "12 credits" (8s) or "15 credits" (10s) before submitting.
5. **QA before posting:** download, then `ffmpeg -i v.mp4 -vf "fps=1.5,scale=220:-1,tile=7x2" -frames:v 1 grid.jpg` and check every frame for the failures in section 3.

---

## 2. Master prompt template

```
authentic vertical iPhone video, [CAMERA SETUP], one continuous shot, no cuts.
keep the woman identical to the reference images: same face, [HAIR], [OUTFIT, every piece].
[LOCATION + LIGHT, 1 sentence, real place details].
0-[X]s: [BEAT 1: one action + one expression].
[X]-[Y]s: [BEAT 2].
[Y]-[Z]s: [BEAT 3].
[Z]-end: [ENDING: look at camera + cute micro-expression].
natural real-time speed, realistic body weight, [PROPS] stay in the same place and never morph,
normal hands with five fingers, no other people.
the woman's hands are empty except for [PROP]. no phone anywhere in the scene.
no text, no captions, no music, [AMBIENT SOUND] only.
```

Rules for filling it in:
- **3–4 beats max for 10s.** More beats means rushed, glitchy motion.
- **One action per beat.** "She spins, grabs coffee, waves" in one beat produces morphing.
- **Use timestamps** (`0-3s:`). Omni follows them well.
- **List the outfit piece by piece** every time, even with the sheet attached.
- **Camera line goes first, the "no phone" line goes last.**

### Camera setups that worked
| Want | Write |
|---|---|
| Tripod / propped | `static locked-off camera at chest height across the room` |
| Desk cam | `static camera resting on the desk slightly to the side` |
| Selfie | `handheld front-camera selfie at arm's length, her arm partly visible at the frame edge` |
| POV view then reveal | Avoid in one clip (see balcony failure). Make 2 clips and cut them together. |

---

## 3. Failures we hit and how to prevent them

### ❌ Phone visible in the scene (restaurant video)
**Cause:** the prompt said `phone propped still on a table`, so Omni drew a phone on a tripod in the corner.
**Fix:**
- Never write "phone", "iPhone on a tripod" or "propped phone" as an *object*. Describe the camera only by angle: `static locked-off camera at chest height`.
- "authentic vertical iPhone video" at the start is fine: it sets the look and doesn't draw a phone.
- Always end with: `no phone, tripod, or camera anywhere in the scene.`
- Also check the **scene still** before using it. If a phone is in the still, it will be in the video.

### ❌ Weird pan + second phone appearing (balcony video)
**Cause:** one clip asked for a rear-camera view **and then** a 180° swing to selfie. Omni can't keep that consistent: the pan warps, and in the selfie half she holds a phone while the camera is also "the phone".
**Fix:**
- **Split it into 2 clips:** Clip A = view only (4–5s, no person). Clip B = selfie OOTD starting already in selfie mode. Cut them together in CapCut with a quick whip-pan transition.
- For any selfie clip: `her arm extends out of frame holding the camera; her other hand is empty or in her pocket. she never holds a second phone.`
- Avoid "camera swings around" or "turns 180 degrees" in one prompt.

### ❌ Clothes levitating to her + room never gets clean (cleaning video)
**Cause:** "timelapse at 8x" plus 6 tasks in one prompt. Omni fakes speed by making objects drift and float, and it won't remove clutter across a single clip.
**Fix:**
- **Don't ask Omni for a timelapse.** Shoot 3 short clips and speed them up in CapCut:
  1. Messy room still → `she picks up clothes one armful at a time and drops them in the basket` (normal speed).
  2. **Half-clean room still** (make a new Nano Banana still with less mess) → `she makes the bed and fluffs pillows`.
  3. **Spotless room still** → `she does a slow spin, hair swinging, smiles at camera`.
- The "after" state has to be in a **separate still**. Omni won't transform the room on its own.
- Add: `objects only move when her hands are touching them; nothing floats or slides on its own.`

### ⚠️ Props drifting (corporate video)
The coffee was set down front-center instead of back where it started.
**Fix:** `she puts the coffee back in the exact same spot to the right of the laptop.` Name each prop's location in the scene still prompt and the video prompt the same way.

---

## 4. Making her cutesy (retention for guys AND girls)

Pick **2–3 per video** (not all of them):

**Micro-expressions (best for retention, hook in the first 1s)**
- pouty lips + big eyes at camera
- little smirk then looks away
- playful eye roll
- bites lip while thinking
- soft laugh, covers mouth with her hand
- scrunches nose and smiles
- tucks hair behind her ear while looking up at camera

**Body movement (shows the outfit, guys watch the loop)**
- slow graceful spin, hair swinging
- hair flip over one shoulder
- small shimmy / sway to imaginary music
- leans toward camera on the desk, chin in hands
- cross-legged in a chair, swivels side to side
- hands in back pockets / pocket of sweats, weight on one hip

**Relatable "girly" beats (girls share and comment)**
- dramatic sigh, shoulders drop
- head tilts back, eyes closed, "I'm so done"
- long sip of an iced latte through a straw
- glances at the camera like "are you seeing this"
- little shrug with palms up

**Rules:**
- **End on eye contact + a micro-expression.** It makes the clip loop and lifts replays.
- **Movement every 2–3 seconds.** A still pose for 4s+ = scroll.
- Keep it **flirty-cute, not explicit**: fitted outfits, spins and smiles. Explicit or suggestive framing gets suppressed or the account banned, and kills reach with girls.
- Outfit + setting should look **aspirational but real**: a nice apartment with some clutter, golden hour, an iced coffee, light-up vanity, photo wall.

---

## 5. Anti-AI checklist (add these lines every time)

```
natural real-time speed, realistic body weight and physics, objects only move when touched,
props stay consistent and never morph or teleport, natural body proportions,
normal hands with five fingers, consistent background, no other people unless stated,
no phone, tripod, or camera anywhere in the scene, no text, no captions, no music.
```

**Reject a render if:** a second phone shows up · extra or merged fingers · objects float or slide · the face changes mid-clip · the outfit changes · text appears · the background warps during camera moves · the motion is too smooth or slow-mo.

---

## 6. Captions & text
- Generate **without text**. Add captions in CapCut/TikTok (they look better and you can A/B them).
- Hook text = the caption idea. Video = the reaction or visual punchline.
- Turn on the TikTok/IG **AI-generated content label**.

---

## 7. Log of what we made

| Video | File | Result | Fix next time |
|---|---|---|---|
| Skyscraper sunset OOTD | `Tiff_skyscraper_sunset_OOTD_v1.mp4` | View is great; the pan is warped and a second phone shows at 8–9.5s | Split into a view clip + a selfie clip |
| Server runaway | `Tiff_server_runaway_v1.mp4` | Good expressions; a phone on a tripod sits in the corner | Remove "phone propped" from the prompt; add the no-phone line |
| Cleaning room | `Tiff_cleaning_room_v1.mp4` | Cute spins; clothes float and the room never gets clean | 3 clips from 3 stills (messy → half → clean); no timelapse |
| Corporate job | `Tiff_corporate_job_v1.mp4` | Best of the 4: sigh, lean back, sip, smirk | Lock prop positions |

**Credits:** 10s 720p = 15 cr · 8s 720p = 12 cr · Nano Banana images = 0 cr.
