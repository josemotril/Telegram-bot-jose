import random
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime

W, H = 1080, 1920

temas = [
    ("RECETA", "Gazpacho express: tomate maduro + AOVE + sal", "Quick gazpacho: ripe tomato + EVOO + salt"),
    ("TIP", "Afila el cuchillo cada semana", "Sharpen your knife weekly"),
    ("FRASE", "Cocinar es pasión diaria", "Cooking is daily passion"),
]

fondos = [
    ((245, 87, 87), (255, 195, 113)),
    ((67, 206, 162), (24, 90, 157)),
    ((255, 154, 158), (250, 208, 196)),
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


def escribir(draw, texto, font, y):
    texto = textwrap.fill(texto, width=22)
    bbox = draw.multiline_textbbox((0,0), texto, font=font)
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]
    draw.multiline_text(((W-w)/2, y), texto, font=font, fill="white", align="center")
    return y + h + 40


os.makedirs("stories", exist_ok=True)

for i in range(3):

    categoria, es, en = random.choice(temas)
    c1, c2 = random.choice(fondos)

    img = degradado(c1, c2)
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 90)
    font_mid = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 45)

    y = 350
    y = escribir(draw, categoria, font_big, y)
    y = escribir(draw, es, font_mid, y)
    y = escribir(draw, en, font_small, y)

    draw.text((W/2, H-120), "@JoseMotril", font=font_small, anchor="mm", fill="white")

    nombre = "stories/story_" + datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(i) + ".png"
    img.save(nombre)

print("OK")
