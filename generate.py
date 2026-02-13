import random
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime

W, H = 1080, 1920

temas = [
    ("RECETA", "Gazpacho express: tomate maduro + AOVE + sal", "Quick gazpacho: ripe tomato + EVOO + salt"),
    ("TIP", "Afila el cuchillo cada semana para cortes limpios", "Sharpen your knife weekly for clean cuts"),
    ("CURIOSIDAD", "El aceite temprano aporta más antioxidantes", "Early harvest olive oil has more antioxidants"),
    ("FRASE", "La cocina es pasión, técnica y constancia", "Cooking is passion, technique and consistency"),
]

fondos = [
    ((245, 87, 87), (255, 195, 113)),
    ((67, 206, 162), (24, 90, 157)),
    ((255, 154, 158), (250, 208, 196)),
    ((141, 153, 174), (237, 242, 244)),
]

def degradado(c1, c2):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(c1[0] + (c2[0]-c1[0]) * y/H)
        g = int(c1[1] + (c2[1]-c1[1]) * y/H)
        b = int(c1[2] + (c2[2]-c1[2]) * y/H)
        draw.line((0,y,W,y), fill=(r,g,b))
    return img

def multiline(draw, text, font, y):
    lines = textwrap.fill(text, width=24)
    bbox = draw.multiline_textbbox((0,0), lines, font=font)
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]
    draw.multiline_text(((W-w)/2, y), lines, font=font, fill="white", align="center")
    return y + h + 40

os.makedirs("stories", exist_ok=True)

for i in range(3):  # 🔥 3 historias por ejecución
    categoria, es, en = random.choice(temas)

    c1, c2 = random.choice(fondos)
    img = degradado(c1, c2)
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 95)
    font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 50)

    y = 300
    y = multiline(draw, categoria, font_big, y)
    y = multiline(draw, es, font_main, y)
    y = multiline(draw, en, font_small, y)

    draw.text((W/2, H-120), "@JoseMotril", font=font_small, anchor="mm", fill="white")

    filename = f"stories/story_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
    img.save(filename)

print("3 historias creadas correctamente")
