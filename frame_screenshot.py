#!/usr/bin/env python3
"""Frame a screenshot so it matches the rest of the report.

Usage:
    python3 tools/frame_screenshot.py INPUT.png screenshots/06-dnsrecon.png "kali@kali: ~  ·  dnsrecon -d networkwalks.com"

Needs Pillow:  sudo apt install python3-pil
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def load_font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()

def frame(src, dst, title, width=1500):
    im = Image.open(src).convert("RGB")
    h = round(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS)
    bar, pad, r = 50, 46, 18
    ww, wh = width, h + bar
    W, H = ww + pad * 2, wh + pad * 2 + 8
    lg = Image.linear_gradient("L")
    mask = Image.blend(lg.resize((W, H)), lg.rotate(90).resize((W, H)), 0.5)
    bg = Image.composite(Image.new("RGB", (W, H), (22, 14, 62)), Image.new("RGB", (W, H), (7, 34, 40)), mask)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((pad, pad + 14, pad + ww, pad + wh + 14), r, fill=(0, 0, 0, 170))
    bg = Image.alpha_composite(bg.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(24)))
    win = Image.new("RGB", (ww, wh), (10, 16, 32))
    d = ImageDraw.Draw(win)
    d.rectangle((0, 0, ww, bar), fill=(24, 34, 58))
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 30 + i * 28
        d.ellipse((cx - 8, bar // 2 - 8, cx + 8, bar // 2 + 8), fill=col)
    font = load_font(19)
    tw = d.textlength(title, font=font)
    d.text(((ww - tw) / 2, bar / 2 - 12), title, font=font, fill=(148, 163, 184))
    win.paste(im, (0, bar))
    m = Image.new("L", (ww, wh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, ww - 1, wh - 1), r, fill=255)
    bg.paste(win.convert("RGBA"), (pad, pad), m)
    bg.convert("RGB").save(dst, optimize=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    frame(*sys.argv[1:4])
    print("saved", sys.argv[2])
