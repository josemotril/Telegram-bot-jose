import os
import requests
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from datetime import datetime

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

W, H = 1080, 1920
os.makedirs("stories", exist_ok=True)

contenidos = [
    ("Receta rápida de gazpacho andaluz con AOVE temprano y vinagre suave",
     "Quick Andalusian gazpacho with early harvest EVOO"),

    ("Tip profesional: enfría las cremas en abatidor para mantener color y sabor",
     "Pro tip: chill soups fast to keep color and flavor"),

    ("Curiosidad: el HPP alarga la vida útil sin afectar nutrientes",
     "Fun fact: HPP extends shelf life without heat"),

    ("Frase chef: menos ingredientes, más técnica y producto",
     "Chef quote: fewer ingredients, more technique"),
]


def generar_imagen(prompt):
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1536"
    )

    img_url = result.data[0].url
    img = Image.open(BytesIO(requests.get(img_url).content)).convert("RGB")
    return img.resize((W, H))


def overlay_text(img, es, en):
    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 120))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 45)

    y = 1200

    draw = ImageDraw.Draw(img)

    draw.multiline_text((80, y), es, font=font_big, fill="white")
    draw.multiline_text((80, y+200), en, font=font_small, fill="white")

    draw.text((W-200, H-120), "@JoseMotril", font=font_small, fill="white")

    return img.convert("RGB")


for i in range(3):

    es, en = random.choice(contenidos)

    prompt = f"""
    professional food photography, mediterranean kitchen, natural light,
    gastronomic editorial style, high quality, instagram story composition,
    realistic textures, modern, clean, elegant
    """

    img = generar_imagen(prompt)
    img = overlay_text(img, es, en)

    filename = f"stories/story_{datetime.now().strftime('%H%M%S')}_{i}.png"
    img.save(filename)


print("imagenes generadas")
