# day_x5_swap (2026-11-11) — Tiff swapped into 4 X clips with the new /swapTiff method

Sources: danclipping car talk (r1, 7.8s), sixugc kitchen fridge (r2, 0–10s), danclipping car dance (r3, 5–15s), maxxmalist suit + cash (r4, 5–15s).

Method (now `.claude/skills/swapTiff`):
- Motion clips: upper face (brows/eyes/nose) blurred with `blur_face.py` (YuNet), mouth left sharp, muted.
- New reusable face-angle sheet: `characterSheet/codex/Tiff_face_angles.png`.
- Outfit sheets (Codex): 24 black cami car, 25 navy scoop tank, 26 black lace cami, 27 navy power suit. Tiff's own hair/makeup kept.
- Start frames (NB Pro, 0 cr): refs id1, id2, face-angles, outfit sheet, blurred source first frame.
- Omni 1.1 Flash Ingredients: id1, id2, face-angles, start frame, blurred clip. 20 cr each.

Results (face_match.py, Tiff vs source):
- v1 car talk ✅ 0.70 / 0.36
- v2 kitchen ✅ 0.63 / 0.44
- v4 suit cash ✅ 0.60 / 0.12 (hands in the fan close-ups look a bit large)
- v3 lace cami car dance ❌ Omni policy block twice (refunded). Codex also blocked the sheet once until the source frame was dropped.
Compare day_x4 drifted clips: Tiff 0.37 / source 0.67–0.76.

Credits: 60 spent (3 × 20). Two v3 attempts refunded.
Exports in ../videos: tiff_swap_{car-talk_black-cami 8s, kitchen_navy-scoop-tank 10s, bedroom-cash_navy-suit 10s}, each _audio and _muted.
