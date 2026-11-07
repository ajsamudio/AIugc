from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import textwrap
F="frames/"
slides=[("sc_s1_car_B.jpeg","how i stay calm when life gets loud",True),
("sc_b1_matcha_codex.png","1. i stop replying right away.",False),
("sc_b4_train_window_codex.png","2. not everything deserves a reaction.",False),
("sc_b2_candle_journal_codex.png","3. i write it down instead of spiraling.",False),
("sc_b3_beach_codex.png","4. i go outside, even for 10 minutes.",False),
("sc_s3_bed_A.jpeg","5. i remind myself feelings pass.",False)]
W,H=1080,1920
for n,(src,txt,title) in enumerate(slides,1):
    im=ImageOps.fit(Image.open(F+src).convert("RGB"),(W,H),Image.LANCZOS)
    font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf",50 if title else 40)
    lines=textwrap.wrap(txt,26 if title else 30)
    lh=font.size*1.3; y0=H*(0.70 if src.startswith("sc_s") else 0.52)-len(lines)*lh/2
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(sh)
    for i,l in enumerate(lines):
        w=d.textlength(l,font=font); d.text(((W-w)/2,y0+i*lh),l,font=font,fill=(0,0,0,200))
    sh=sh.filter(ImageFilter.GaussianBlur(4))
    im=Image.alpha_composite(im.convert("RGBA"),sh); d=ImageDraw.Draw(im)
    for i,l in enumerate(lines):
        w=d.textlength(l,font=font); d.text(((W-w)/2,y0+i*lh),l,font=font,fill=(255,255,255,255))
    im.convert("RGB").save(f"carousel/staycalm_{n}.jpg",quality=93)
print("ok")
