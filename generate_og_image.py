"""
Generate static/img/og-image.png — the 1200x630 social-share preview card.
Run once: python generate_og_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (0, 22, 33)            # #001621 Noturno
ACCENT = (255, 65, 3)       # #FF4103 Vulcanico
ACCENT2 = (255, 138, 92)    # #ff8a5c
TEXT = (234, 242, 245)
MUTED = (138, 164, 176)

OUT = os.path.join("static", "img", "og-image.png")


def load_font(size, bold=True):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Soft accent glow (top-right)
    glow = Image.new("RGB", (W, H), BG)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 520, -260, W + 160, 300], fill=(40, 20, 10))
    img = Image.blend(img, glow, 0.6)
    d = ImageDraw.Draw(img)

    # Accent side bar
    d.rectangle([0, 0, 16, H], fill=ACCENT)

    # AK monogram chip
    d.rounded_rectangle([80, 70, 190, 180], radius=24, fill=ACCENT)
    mono = load_font(60)
    d.text((135, 125), "AK", font=mono, fill=(255, 255, 255), anchor="mm")

    # Name
    name_font = load_font(76)
    d.text((80, 250), "Ashish Kumar Rajpoot", font=name_font, fill=TEXT)

    # Title line in accent
    role_font = load_font(40, bold=True)
    d.text((82, 345), "Data Engineer", font=role_font, fill=ACCENT2)

    # Subtitle
    sub_font = load_font(30, bold=False)
    d.text((82, 405), "Python · SQL · ETL · Apache Airflow · Spark · AWS · Agentic AI",
           font=sub_font, fill=MUTED)

    # Bottom tagline
    tag_font = load_font(26, bold=False)
    d.text((82, 520), "Turning data into reliable pipelines and clear insights.",
           font=tag_font, fill=MUTED)

    # URL
    url_font = load_font(26)
    d.text((82, 560), "ashishkumarrajpoot89.github.io", font=url_font, fill=ACCENT)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG")
    print("Wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
