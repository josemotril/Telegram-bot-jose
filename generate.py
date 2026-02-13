import random
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime

W, H = 1080, 1920

temas = [
    ("RECETA",
     "Gazpacho express: tomate maduro + AOVE + sal",
     "Quick gazpacho: ripe tomato + EVOO + salt",
     "tomato food kitchen cooking"),

    ("TIP",
     "Afila el cuchillo cada semana para cortes limpios",
     "Sharpen your knife weekly for clean cuts",
     "chef knife kitchen professional"),

    ("CURIOSIDAD",
     "El aceite temprano aporta más antioxidantes",
     "Early harvest olive oil has more antioxidants",
     "olive oil mediterranean food"),

    ("FRASE",
     "La cocina es pasión, técnica y constancia",
     "Cooking is passion, technique and consistency",
     "modern kitchen minimal background"),
]

def descargar_imagen(query):
    url = f"https://source.unsplash.com/1080x1920/?{query}"
    img_data = requests.get(url, timeout=20).content
    with open("temp.jpg", "wb") as f:
        f.write(img_data)
    return Image.open("temp.jpg").convert("RGB")

def multiline(draw, text, font, y):
    lines = textwrap.fill(text, width=24)
    bbox = draw.multiline_textbbox((0,0), lines, font=font)
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]
    draw.multiline_text(((W-w)/2, y), lines, font=font, fill="white", align="center")
    return y + h + 40

os.makedirs("stories", exist_ok=True)

for i in range(3):   # 🔥 genera 3 historias cada vez
    categoria, es, en, query = random.choice(temas)

    img = descargar_imagen(query)
    overlay = Image.new("RGBA", img.size, (0,0,0,120))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 90)
    font_main = ImageFont.truetype("DejaVuSans-Bold.ttf", 65)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 45)

    y = 300
    y = multiline(draw, categoria, font_big, y)
    y = multiline(draw, es, font_main, y)
    y = multiline(draw, en, font_small, y)_

