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
        r = int(c1[0] + (c2[0] - c1[0]) * y / H)
        g = int(c1[1] + (c2[1] - c1[1]) * y / H)
        b = int(c1[2] + (c2[2] - c1[2]
_{i}.png"
    img.save(filename)

print("3 historias creadas correctamente")
