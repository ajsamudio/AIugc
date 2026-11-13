"""Score how much a video's face matches Tiff (and how much it still matches the source girl).

usage: python face_match.py OUT.mp4 --ref TIFF_IMG [TIFF_IMG ...] [--src SOURCE.mp4] [--n 10] [--grid OUT.jpg]
Prints the SFace cosine similarity per sampled frame and the mean.
  >= 0.45  same person (good)   0.30-0.45  borderline, eyeball it   < 0.30  drifted
With --src, also prints similarity to the source person; that should stay clearly below the Tiff score.
--grid writes a strip of the sampled face crops next to the Tiff ref crop for eyeballing.
"""
import argparse, os
import cv2, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("--ref", nargs="+", required=True)
ap.add_argument("--src"); ap.add_argument("--n", type=int, default=10); ap.add_argument("--grid")
a = ap.parse_args()

rec = cv2.FaceRecognizerSF.create(os.path.join(HERE, "models", "sface.onnx"), "")
def detector(w, h):
    return cv2.FaceDetectorYN.create(os.path.join(HERE, "models", "yunet.onnx"), "", (w, h), 0.6, 0.3, 50)

def faces_in(img):
    d = detector(img.shape[1], img.shape[0]); _, f = d.detect(img)
    return [] if f is None else list(f)

def embed(img, f):
    al = rec.alignCrop(img, f); return rec.feature(al), al

def ref_feats(paths):
    out, crop = [], None
    for p in paths:
        img = cv2.imread(p)
        for f in faces_in(img):
            if f[2] < 60: continue
            e, al = embed(img, f); out.append(e)
            if crop is None or f[2] > 200: crop = al
    return out, crop

def sample(video, n):
    cap = cv2.VideoCapture(video); tot = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); res = []
    for k in range(n):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int((k + 0.5) * tot / n)); ok, fr = cap.read()
        if not ok: continue
        fs = faces_in(fr)
        if not fs: res.append((k, None, None)); continue
        f = max(fs, key=lambda r: r[2] * r[3]); e, al = embed(fr, f); res.append((k, e, al))
    return res

def sim(e, refs): return max(float(rec.match(e, r, cv2.FaceRecognizerSF_FR_COSINE)) for r in refs)

refs, rcrop = ref_feats(a.ref)
if not refs: raise SystemExit("no face found in the Tiff refs")
src_refs = [e for _, e, _ in sample(a.src, 8) if e is not None] if a.src else []
rows, crops = [], [rcrop]
for k, e, al in sample(a.video, a.n):
    if e is None: print(f"frame {k}: no face"); continue
    t = sim(e, refs); s = sim(e, src_refs) if src_refs else None
    rows.append((t, s)); crops.append(al)
    print(f"frame {k}: tiff {t:.2f}" + (f"  source {s:.2f}" if s is not None else ""))
if rows:
    mt = np.mean([r[0] for r in rows]); ms = np.mean([r[1] for r in rows]) if src_refs else -1
    print(f"MEAN tiff {mt:.2f}" + (f"  source {ms:.2f}" if src_refs else ""))
    # calibrated on day_x4_swap: drifted clips scored tiff 0.36-0.37 vs source 0.67-0.76
    if src_refs and ms >= mt: print("verdict: DRIFTED toward the source face")
    else: print("verdict:", "OK" if mt >= 0.45 else "BORDERLINE - eyeball it" if mt >= 0.30 else "DRIFTED / face not readable")
if a.grid and len(crops) > 1:
    cv2.imwrite(a.grid, np.hstack([cv2.resize(c, (160, 160)) for c in crops]))
    print("grid:", a.grid, "(first crop = Tiff ref)")
