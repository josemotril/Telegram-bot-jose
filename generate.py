import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from datetime import datetime

W, H = 1080, 1920

temas = [
    ("TIP", "Añade el aceite al final para un gazpacho más brillante", "Add the olive oil at the end for a brighter gazpacho"),
    ("RECETA", "Tomate rallado + AOVE + sal = desayuno andaluz perfecto", "Grated tomato + EVOO + salt = perfect Andalusian breakfast"),
    ("CURIOSIDAD", "El HPP conserva sabor sin usar calor", "HPP preserves flavor without heat"),
    ("FRASE", "Cocinar es un acto de amor diario", "Cooking is a daily act of love"),
    ("TIP", "Enfría rápido las cremas para mantener color intenso", "Cool soups quickly to keep bright color"),
]

categoria, texto_es, texto_en = random.choice(temas)

img = Image.new("RGB", (W, H), (245, 245, 240))
draw = ImageDraw.Draw(img)

try:
    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 95)
    font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
    font_sub = ImageFont.truetype("DejaVuSans.ttf", 50)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 40)
except:
    font_big = font_main = font_sub = font_small = ImageFont.load_default()

def multiline(text, font, y):
    lines = textwrap.fill(text, width=22)
    bbox = draw.multiline_textbbox((0, 0), lines, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.multiline_text(((W - w) / 2, y), lines, font=font, fill=(20,20,20), align="center")
    return y + h + 40


y = 250
y = multiline(categoria, font_big, y)
y = multiline(texto_es, font_main, y)
y = multiline(texto_en, font_sub, y)

draw.text((W/2, H-150), "@JoseMotril", font=font_small, anchor="mm", fill=(100,100,100))

os.makedirs("stories", exist_ok=True)
filename = f"stories/story_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
img.save(filename)

print("Creada:", filename)
