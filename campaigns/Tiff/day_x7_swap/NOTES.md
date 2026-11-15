# day_x7_swap — 8 reference clips → Tiff (2026-11-14)
Outfit sheets: characterSheet/codex/Tiff_outfit_28..35 (Codex, free). Start frames NB Pro x2 each (0 cr). Omni 1.1 Flash 720p, 8 x 20 cr = 160 cr.

| clip | outfit | face_match tiff/src | status |
|---|---|---|---|
| v1 mall walk (vibe, male VO) | 28 leopard maxi | 0.62/0.25 | shipped, title removed |
| v2 bedroom | 29 oversized jacket | 0.77/0.45 | shipped |
| v3 blonde night | 30 black tank | 0.53/0.42 | shipped (weakest pass) |
| v4 curly | 31 black tee | 0.82/0.37 | shipped |
| v5 grey room | 32 grey henley | 0.81/0.38 | shipped |
| v6 brown long-sleeve | 33 brown longsleeve | 0.35/0.51 | DRIFTED, not shipped |
| v7 | 34 rose top | 0.79/0.38 | shipped |
| v8 | 35 grey tee | 0.74/0.34 | shipped |

Learnings
- Flow ignores JS `.click()` on "Start generation": use a real click. Chips + prompt can be scripted (addIng / execCommand insertText).
- NB Pro copied the source's blonde hair (v3): add "She has dark brunette hair, NOT blonde" for blonde sources.
- One v6 start frame drifted to the source face before Omni even ran; v6 still drifted in Omni. Close-up selfie with long dark hair = high drift risk.
- Row download buttons work but are slow (~20s); files land as Woman_<desc>_<hash>.mp4, map by first frame.
