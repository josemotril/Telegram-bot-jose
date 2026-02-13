import random
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime

W, H = 1080, 1920

recetas = [
    ("Gazpacho express con tomate pera y AOVE", "Quick gazpacho with plum tomato and EVOO"),
    ("Salmorejo cremoso con pan del día anterior", "Creamy salmorejo with day-old bread"),
    ("Guacamole casero con lima y cilantro", "Homemade guacamole with lime and cilantro"),
    ("Tomate rallado con aceite temprano y sal marina", "Grated tomato with early olive oil and sea salt"),
]

tips = [
    ("Afila el cuchillo cada semana", "Sharpen your knife weekly"),
    ("Enfría rápido las cremas para mantener color", "Cool soups quickly to keep color"),
    ("Añade el aceite al final para más aroma", "Add oil at the end for more aroma"),
    ("Sala siempre al final para controlar sabor", "Salt at the end to control flavor"),
]

curiosidades = [
    ("El HPP conserva sabor sin calor", "HPP preserves flavor without heat"),
    ("El tomate maduro tiene más umami", "Ripe tomatoes contain more umami"),
    ("El AOVE protege antioxidantes naturales", "EVOO protects natural antioxidants"),
]

frases = [
    ("Cocinar es cuidar a los demás", "Cooking is caring for others"),
    ("La cocina es pasión diaria", "Cooking is daily passion"),
    ("Menos ingredientes, más calidad", "Less ingredients, more quality"),
]

fondos = [
    ((245, 87, 87), (255, 195, 113)),
    ((67, 206, 162), (24, 90, 157)),
    ((255, 154, 158), (250, 208, 196)),
    ((141, 153, 174), (237, 242, 244)),
    ((255, 126, 95), (254, 180, 123)),
]


def degradado(c1, c2):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        r = int(c1[0] + (c2[0]-c1[0]) * y/H)
        g = int(c1[1] + (c2[1]-c1[1]) * y/H)
        b = int(c1[2] + (c2[2]-c1[2]) * y/H)
        draw.line((0, y, W, y), fill=(r, g, b))

    return img


def escribir(draw, texto, font, y):
    texto = textwrap.fill(texto, width=24)
    bbox = draw.multiline_textbbox((0,0), texto, font=font)
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]
    draw.multiline_text(((W-w)/2, y), texto, font=font, fill="white", align="center")
    return y + h + 50


def generar_contenido():
    tipo = random.choice(["RECETA", "TIP", "CURIOSIDAD", "FRASE"])

    if tipo == "RECETA":
        es, en = random.choice(recetas)
    elif tipo == "TIP":
        es, en = random.choice(tips)
    elif tipo == "CURIOSIDAD":
        es, en = random.choice(curiosidades)
    else:
        es, en = random.choice(frases)

    return tipo, es, en


os.makedirs("stories", exist_ok=True)

for i in range(3):

    categoria, es, en = generar_contenido()
    c1, c2 = random.choice(fondos)

    img = degradado(c1, c2)
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 95)
    font_mid = ImageFont.truetype("DejaVuSans-Bold.ttf", 65)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 45)

    y = 300
    y = escribir(draw, categoria, font_big, y)
    y = escribir(draw, es, font_mid, y)
    y = escribir(draw, en, font_small, y)

    draw.text((W/2, H-130), "@JoseMotril", font=font_small, anchor="mm", fill="white")

    nombre = f"stories/story_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
    img.save(nombre)

print("Historias creadas")

    img.save(nombre)

print("OK")
