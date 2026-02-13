import random
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime

W, H = 1080, 1920
os.makedirs("stories", exist_ok=True)

recetas = [
    ("Gazpacho andaluz cremoso con AOVE", "Creamy Andalusian gazpacho with EVOO"),
    ("Salmorejo tradicional en 5 minutos", "Traditional salmorejo in 5 minutes"),
]

tips = [
    ("Afila el cuchillo cada semana", "Sharpen your knife weekly"),
    ("Añade el aceite al final para más aroma", "Add oil at the end for more aroma"),
]

frases = [
    ("La cocina es pasión diaria", "Cooking is daily passion"),
    ("Menos ingredientes, más calidad", "Less ingredients, more quality"),
]


def center(draw, text, font, y, color="white"):
    text = textwrap.fill(text, width=22)
    bbox = draw.multiline_textbbox((0,0), text, font=font)
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]
    draw.multiline_text(((W-w)/2, y), text, font=font, fill=color, align="center")
    return y + h


font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 95)
font_mid = ImageFont.truetype("DejaVuSans-Bold.ttf", 65)
font_small = ImageFont.truetype("DejaVuSans.ttf", 45)


# =========================
# ESTILO 1 → RECETA EDITORIAL
# =========================
img = Image.new("RGB", (W,H), (245,242,235))
draw = ImageDraw.Draw(img)

draw.rectangle((80, 300, W-80, 1200), fill=(255,255,255))

es, en = random.choice(recetas)

y = 350
y = center(draw, "RECETA", font_small, y, "black") + 40
y = center(draw, es, font_mid, y, "black") + 40
center(draw, en, font_small, y, "gray")

draw.text((W/2, H-140), "@JoseMotril", font=font_small, anchor="mm", fill="gray")
img.save(f"stories/story_{datetime.now().strftime('%H%M%S')}_0.png")


# =========================
# ESTILO 2 → TIP MINIMAL
# =========================
img = Image.new("RGB", (W,H), (30,30,30))
draw = ImageDraw.Draw(img)

es, en = random.choice(tips)

draw.rectangle((0, 900, W, 1200), fill=(255,255,255))

center(draw, "TIP PRO", font_small, 200, "white")
center(draw, es, font_big, 450, "white")
center(draw, en, font_small, 950, "black")

draw.text((W/2, H-140), "@JoseMotril", font=font_small, anchor="mm", fill="white")
img.save(f"stories/story_{datetime.now().strftime('%H%M%S')}_1.png")


# =========================
# ESTILO 3 → FRASE IMPACTO
# =========================
c1 = (255,126,95)
c2 = (254,180,123)

img = Image.new("RGB", (W,H))
draw = ImageDraw.Draw(img)

for y in range(H):
    r = int(c1[0] + (c2[0]-c1[0]) * y/H)
    g = int(c1[1] + (c2[1]-c1[1]) * y/H)
    b = int(c1[2] + (c2[2]-c1[2]) * y/H)
    draw.line((0,y,W,y), fill=(r,g,b))

es, en = random.choice(frases)

center(draw, es.upper(), font_big, 700)
center(draw, en, font_small, 1000)

draw.text((W/2, H-140), "@JoseMotril", font=font_small, anchor="mm", fill="white")
img.save(f"stories/story_{datetime.now().strftime('%H%M%S')}_2.png")

print("3 historias PRO creadas")
