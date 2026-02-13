import os
import json
import base64
from datetime import datetime
from io import BytesIO

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont


# =========================
# CONFIG PRO
# =========================

W, H = 1024, 1536
SAFE_MARGIN = 120

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

os.makedirs("stories", exist_ok=True)


# =========================
# GPT CONTENIDO PREMIUM
# =========================

def generar_contenido():

    prompt = """
Devuelve SOLO JSON válido.

Genera 3 historias gastronómicas estilo profesional Instagram.

Formato:

{
 "historias": [
   {
     "titulo": "4 palabras máximo",
     "frase": "frase inspiradora breve",
     "post": "texto profesional educativo 5-7 líneas",
     "prompt_imagen": "fotografía gastronómica realista, luz natural, estilo editorial, plato descrito"
   }
 ]
}

Tipos:
- técnica culinaria
- receta premium
- curiosidad gastronómica
- chef tip

Tono:
moderno, elegante, foodie, profesional.
"""

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0
    )

    return json.loads(r.choices[0].message.content)["historias"]


# =========================
# IMAGEN IA
# =========================

def generar_imagen(prompt):

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1536"
    )

    img_b64 = result.data[0].b64_json
    img_bytes = base64.b64decode(img_b64)

    return Image.open(BytesIO(img_bytes)).convert("RGBA")


# =========================
# DISEÑO PREMIUM
# =========================

def add_gradient(img):

    gradient = Image.new("L", (1, H), 0)

    for y in range(H):
        value = int(255 * (y / H))
        gradient.putpixel((0, y), value)

    alpha = gradient.resize(img.size)
    black = Image.new("RGBA", img.size, (0, 0, 0, 190))

    img = Image.composite(black, img, alpha)

    return img


def draw_centered(draw, text, font, y):

    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")

    w = bbox[2] - bbox[0]

    x = (W - w) // 2

    draw.multiline_text((x, y), text, font=font, fill="white", align="center")


def story_layout(img, titulo, frase):

    img = add_gradient(img)

    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
        sub_font = ImageFont.truetype("DejaVuSans.ttf", 48)
        brand_font = ImageFont.truetype("DejaVuSans.ttf", 32)
    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()

    y_start = H * 0.60

    draw_centered(draw, titulo.upper(), title_font, y_start)
    draw_centered(draw, frase, sub_font, y_start + 120)

    draw.text(
        (SAFE_MARGIN, H - 80),
        "@JoseMotril",
        font=brand_font,
        fill=(255, 255, 255, 180)
    )

    return img.convert("RGB")


# =========================
# MAIN
# =========================

historias = generar_contenido()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

for i, h in enumerate(historias):

    titulo = h["titulo"]
    frase = h["frase"]
    post = h["post"]
    prompt_img = h["prompt_imagen"]

    img = generar_imagen(prompt_img)

    img = story_layout(img, titulo, frase)

    img.save(f"stories/story_{timestamp}_{i}.png")

    with open(f"stories/story_{timestamp}_{i}.txt", "w", encoding="utf-8") as f:
        f.write(post)

print("Historias PRO generadas correctamente")
