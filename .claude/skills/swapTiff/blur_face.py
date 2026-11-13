"""Blur the source person's upper face (brows, eyes, nose) in every frame of a clip.

The mouth and jaw stay sharp so Omni can still copy lip/jaw motion, but there are no
eyes, nose or face shape to copy, so Tiff's face comes only from the identity sheets.

usage: python blur_face.py IN.mp4 OUT.mp4 [--start S] [--dur D] [--check]
  --start/--dur  trim window in seconds (default 0 / 10)
  --check        also write OUT_check.jpg (12-frame grid) to eyeball coverage
Output is muted (Omni rejects clips with music). Uses OpenCV YuNet (models/yunet.onnx).
"""
import argparse, os, subprocess, tempfile
import cv2, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--start", type=float, default=0.0)
ap.add_argument("--dur", type=float, default=10.0)
ap.add_argument("--check", action="store_true")
a = ap.parse_args()

cap = cv2.VideoCapture(a.inp)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
cap.set(cv2.CAP_PROP_POS_MSEC, a.start * 1000)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
det = cv2.FaceDetectorYN.create(os.path.join(HERE, "models", "yunet.onnx"), "", (W, H), 0.6, 0.3, 5)
n_max = int(round(a.dur * fps))

tmp = tempfile.mkdtemp(); raw = os.path.join(tmp, "raw.mp4")
vw = cv2.VideoWriter(raw, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))

last, miss, hits, i = None, 0, 0, 0
while i < n_max:
    ok, fr = cap.read()
    if not ok: break
    _, faces = det.detect(fr)
    if faces is not None and len(faces):
        f = max(faces, key=lambda r: r[2] * r[3])
        x, y, w, h = f[:4]
        nose_y = f[9]; mouth_y = (f[11] + f[13]) / 2
        box = np.array([x - 0.12 * w, y - 0.25 * h, x + 1.12 * w, nose_y + 0.45 * (mouth_y - nose_y)])
        last = box if last is None else 0.65 * box + 0.35 * last
        hits += 1; miss = 0
    else:
        miss += 1
    if last is not None and miss < int(fps * 1.5):
        g = min(miss, 12) * 0.05                       # widen while lost (fast motion/blur)
        bw, bh = last[2] - last[0], last[3] - last[1]
        x0, y0 = int(max(0, last[0] - g * bw)), int(max(0, last[1] - g * bh))
        x1, y1 = int(min(W, last[2] + g * bw)), int(min(H, last[3] + g * bh * 0.3))
        if x1 > x0 + 4 and y1 > y0 + 4:
            roi = fr[y0:y1, x0:x1]
            k = max(41, (min(roi.shape[:2]) // 2) | 1)
            fr[y0:y1, x0:x1] = cv2.GaussianBlur(cv2.resize(cv2.resize(roi, (12, 12)), roi.shape[1::-1]), (k, k), 0)
    vw.write(fr); i += 1
vw.release(); cap.release()

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-an", "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-crf", "18", a.out], check=True)
print(f"{a.out}: {i} frames, face found in {hits} ({100 * hits // max(i, 1)}%)")
if hits < i * 0.7:
    print("WARNING: face missed in many frames; check the grid or pick another window")
if a.check:
    chk = os.path.splitext(a.out)[0] + "_check.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.out, "-vf",
                    f"fps={12 / max(i / fps, 0.1)},scale=240:-2,tile=6x2", "-frames:v", "1", chk], check=True)
    print("grid:", chk)
