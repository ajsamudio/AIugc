"""Overlay TikTok-style text on a slide.
Usage: python add_text.py IN OUT "title" ["subtitle"]
Big, legible white text with a soft shadow, centered in the upper third (below TikTok's top tabs),
wrapped to ~78% width so the photo stays the main thing."""
import sys, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "C:/Windows/Fonts/segoeuib.ttf"

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def main(src, out, title, *subs):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(FONT, int(W * 0.062))
    f2 = ImageFont.truetype(FONT, int(W * (0.048 if len(subs) > 1 else 0.042)))
    blocks = [(l, f1) for l in wrap(d, title, f1, W * 0.78)]
    for s in subs:  # 2+ extra args = numbered list (e.g. all 5 items on one slide)
        if len(subs) > 1: s = f"{subs.index(s) + 1}. {s}"
        blocks += [(l, f2) for l in wrap(d, s, f2, W * 0.78)]
    y = int(H * 0.17)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dl, ds = ImageDraw.Draw(layer), ImageDraw.Draw(sh)
    for i, (line, f) in enumerate(blocks):
        if i and f is f2 and blocks[i - 1][1] is f1: y += int(W * 0.02)
        w = dl.textlength(line, font=f); x = (W - w) / 2
        ds.text((x, y + 3), line, font=f, fill=(0, 0, 0, 200))
        dl.text((x, y), line, font=f, fill=(255, 255, 255, 255),
                stroke_width=max(1, int(W * 0.002)), stroke_fill=(0, 0, 0, 90))
        y += int(f.size * 1.22)
    sh = sh.filter(ImageFilter.GaussianBlur(W * 0.006))
    im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), sh), layer).convert("RGB")
    im.save(out, quality=94)

if __name__ == "__main__":
    main(*sys.argv[1:])
