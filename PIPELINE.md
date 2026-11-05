# AI UGC Pipeline (v0, draft for a future skill)

Source: @sleepclip, "How I Make 100 AI UGC Videos for $0 with Opus 5.5" (X article, Oct 1 2026).
Their stack: Opus (plan + write) → GPT Image (characters) → Seedance/Krea (video) → post at volume, iterate winners.

## Our stack: Claude + Google Flow only

| Stage | Tool | Cost |
|---|---|---|
| Brief, cast, scripts, prompts | Claude (this repo) | free |
| Headshot + fullbody | Flow → Nano Banana 2, 9:16 | **0 credits** |
| Video | Flow → Omni 1.1 Flash, Ingredients mode, 9:16 | 8s: 6 cr @360p / 12 cr @720p |
| QA | Claude checks frames + transcript of each render (`watch` skill) | free |

Budget: 960 credits ≈ 80 clips at 720p, or 160 at 360p. Plan for about 40–60 finished clips per cycle, not 100.

## What we change from the article

1. **Files, not chat memory.** The article depends on "the same Opus chat still remembers everyone". We keep the state in `campaigns/<app>/`:
   `brief.md`, `cast.json`, `scripts.json`, `prompts.json`, `renders.csv`, `results.csv`. These survive between sessions and drive automation.
2. **One platform.** Flow does images and video, and it has a Characters panel, so there's no hopping between ChatGPT, Higgsfield and Krea.
3. **Free image rerolls.** Images cost nothing, so do 4–8 rerolls per character and keep the one that looks least like AI. Spend that effort here, where it's free.
4. **Word count follows clip length.** Spoken words ≈ 3.2 × (seconds − 1); the extra second covers the glance. That's 4s→10, 6s→16, 8s→22, 10s→29.
5. **Gate before you spend.** For each character: render 1 test clip at 360p (6 cr), check the face, voice and artifacts, then batch at 720p. A bad character costs 6 credits, not 120.
6. **Automated QA before a human looks.** Claude pulls frames and a transcript from every render and rejects it for: a second phone, extra fingers, on-screen text, a script mismatch, a face drifting from the headshot, or dead air.
7. **A real feedback loop.** `results.csv` records views and retention for each clip. Winners go back to Claude for 10–20 variations: same character and hook, different details.
8. **Fewer characters, deeper.** Start with 3–5 characters × 5 scripts, not 10 × 10. Find out which persona and hook type works, then scale.

## Pipeline

```
0 BRIEF     app, one-line value, user (age/where/pain), offer, banned claims
1 CAST      Claude → cast.json (N chars: age, look, job, moment-of-use, location, 1 flaw/marker)
2 LOOK      Claude → Nano Banana prompts → Flow (x4 rerolls) → pick headshot → fullbody from ref
3 SCRIPTS   Claude → scripts.json (per char: confession / callout / offer mix, no question openers,
            app named once, word count = clip length rule)
4 PROMPTS   Claude → prompts.json using the skeleton below
5 GATE      1 clip per char @360p → QA → fix char or prompt
6 BATCH     rest @720p with headshot + fullbody as Ingredients → QA → reroll fails only
7 POST/LOOP post 2–3/day/account → results.csv → winners → variations → step 6
```

## Prompt templates

**Cast (step 1)**
```
App: [name]. It does: [one sentence]. User: [age, gender, location, struggle].
Give me [N] UGC characters who'd realistically use this. For each: age, gender, ethnicity,
job, the exact moment in their day they open the app, where they film, one recognizable
physical detail (mole, scar, freckles, tooth gap). People I'd scroll past on TikTok, not models.
Return JSON matching cast.json schema.
```

**Headshot (step 2, Nano Banana 2, 9:16)**
```
casual front-camera phone selfie of a [age] year old [gender], [ethnicity], [hair w/ flyaways],
[eye color], [skin tone] with visible pores, slight shine, [marker], [makeup level],
wearing [one outfit], no jewellery. [location with some clutter], natural [time] light,
slightly off-center framing, [expression]. amateur phone photo, not studio.
```
Fullbody: `the SAME person as the reference image, identical face, hair and outfit, full body, standing in [location], natural posture, amateur phone photo realism`

Reject on sight: plastic skin, perfect hair, oversized eyes, a showroom background, ring-light catchlights.

**Video (step 4, Omni Ingredients: headshot + fullbody)**
```
authentic UGC clip, handheld front-camera selfie, vertical. keep the person identical to the
reference images. [location]. [she/he] is already holding the phone with [app] open.
delivery: [one word]. [she/he] says exactly: "[script]". around second [len-3] [she/he]
glances down at the screen, [small reaction], then back at camera. one continuous action.
exactly one phone in the scene. no text, no captions, no music. slight handheld drift,
built-in phone mic sound. 23mm front camera.
```
Why each piece is there (from the article): "already holding" avoids pickup artifacts and a second phone. One delivery word gets a performance; a pile of adjectives gets a flat face. The glance reads as realism. Camera specs go last so the model doesn't render the phone into the shot.

## Guardrails (also keep accounts alive)
- Turn on TikTok/IG **AI-generated content labels**. Unlabeled synthetic people get suppressed or banned.
- Use feelings and situations ("I kept forgetting X"). Never invent results or testimonials ("lost 20 lbs", "made $5k"); that's a deceptive-endorsement risk under FTC rules.
- Don't use real people's likenesses.

## Open questions to test
- [ ] Does Omni hold one voice across clips? Seedance takes a voice-reference audio and Omni may not. Check if Ingredients accepts audio. If not, test a fixed voice description in the prompt.
- [ ] Does Flow's **Characters** panel give better face consistency than raw Ingredients?
- [ ] Does Flow **Agent** mode let us queue prompts in bulk, or does Claude have to drive the UI per clip?
- [ ] Is 360p good enough to judge face/voice at the gate?

## Flow automation notes (learned in the first test)
- **Uploads:** Flow builds its `<input type=file>` on click, which opens the native picker. Patch `HTMLInputElement.prototype.click` so it attaches the input to the DOM instead, then use `file_upload` on it.
- **Click settings via `find` refs, not coordinates.** Coordinate clicks inside the settings popover often don't register.
- **Settings carry over between modes.** Image x2 turned into video x2 (24 cr). Always check the "Generating will use N credits" line before submitting.
- **Signed video URLs can't be read from JS.** QA in the page: seek `video.currentTime` and screenshot. `webkitAudioDecodedByteCount` > 0 confirms there's an audio track.
- **A studio character sheet makes a bad ingredient.** First turn it into a lifestyle selfie with Nano Banana (free), then use that selfie as the only Omni ingredient.

## Smoke test (done 2026-10-02, 6 credits; see campaigns/sunglasses-test/renders.md)
1 character → 4 headshot rerolls + 1 fullbody (0 cr) → 1 Omni 8s clip @360p (6 cr) → QA → if good, the same clip @720p (12 cr).
