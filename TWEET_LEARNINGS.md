# What we took from @sleepclip's AI UGC article

Source: x.com/sleepclip/status/2105574125745922166 (Oct 1 2026). Their claim is 100 UGC videos for $0, made with Opus → GPT Image → Seedance/Krea.
Note: it ends in a pitch for their creator-distribution agency, so the "$0" framing is marketing. The craft notes are the useful part.

## Rules worth keeping (all confirmed or adopted in our test)

**Casting**
- Ask the LLM to pick the characters, giving it the user profile plus the moment of day they'd use the product and where they'd film.
- Give each character one recognizable flaw (mole, freckles, tooth gap). Add "people I'd scroll past, not models" or you get perfect skin, which gets called out as AI.

**Images**
- Ask for amateur phone-photo cues: visible pores, slight shine, flyaway hair, a cluttered room, off-center framing, natural light.
- Reroll and keep the one that looks least like AI. Reject: plastic skin, perfect hair, oversized eyes, showroom backgrounds, ring-light catchlights.
- Lock each character as a headshot plus a full-body image and never regenerate them. *(Ours: Nano Banana rerolls are free, so do 4–8.)*

**Scripts**
- Fit the words to the clip: about 3.5 words/sec for talking, fewer if there's an action. *(Ours: 3.2 × (sec − 1); 8s ≈ 20–22 words.)* Too many words come out rushed; too few leave dead air.
- Mix the openers: confessions, callouts, offers. No questions as openers. Name the product once, naturally.

**Video prompt skeleton**: each piece fixes a known failure
| Piece | Why |
|---|---|
| "already holding / already wearing X" | Picking things up causes extra fingers and duplicate objects |
| one delivery word ("excited") | A pile of adjectives gives a flat face |
| a small action around second 5 (glance, push glasses up) | Nobody stares into their own camera for 7s straight |
| "exactly one [phone/pair of sunglasses] in the scene" | Models add duplicate props in the background |
| camera specs last | Mention "iPhone" in the scene and it renders an iPhone in the shot |
| "no text, no captions, no music" | Add captions yourself later in CapCut/TikTok |

**Rendering & posting**
- Render one clip per character first, check the face and voice, then batch. A bad character found on clip 40 means 39 wasted renders.
- Keep the voice consistent by reusing the first good clip's audio as a voice reference (Seedance). *(Omni: not known yet.)*
- Post 2–3 a day per account. About 90% will flop; you're hunting for the 3–4 outliers.
- When one hits, have Claude write 20 variations: same character, same hook, new details.

## What the article skips (our additions; see PIPELINE.md)
- Saved files instead of "the same chat remembers": cast.json, scripts.json, prompts.json and renders log.
- Cheap test clips at 360p before spending on 720p.
- Automated checks on every render (frames + audio) before a human looks.
- A results spreadsheet that feeds the variation loop.
- AI-content labels, and no invented results or testimonials. This keeps accounts alive and avoids FTC trouble.
- Only the opener styles are cited, not why the hooks work. Track hook type against retention ourselves.
