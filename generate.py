import os
import json
import base64
from datetime import datetime
from io import BytesIO

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont


# =========================
# CONFIG
# =========================

W, H = 1024, 1536  # tamaño vertical compatible con OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

os.makedirs("stories", exist_ok=True)


# =========================
# GPT → CONTENIDO
# =========================

def generar_contenido():
    prompt = """
Devuelve SOLO JSON válido.

Genera 3 historias diferentes sobre gastronomía española moderna.

Formato:

{
 "historias": [
   {
     "titulo": "...",
     "frase": "...",
     "post": "... texto profesional 4-6 líneas ...",
     "prompt_imagen": "... descripción fotográfica realista ..."
   }
 ]
}

Requisitos:
- profesional
- educativo
- atractivo
- estilo chef / restaurante / foodie
- español + tono premium
"""

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.95
    )

    return json.loads(r.choices[0].message.content)


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

    return Image.open(BytesIO(img_bytes)).convert("RGB")


# =========================
# DISEÑO PROFESIONAL
# =========================

def story_layout(img, titulo, frase):

    draw = ImageDraw.Draw(img)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 120))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

    text = f"{titulo}\n\n{frase}\n\n@JoseMotril"

    bbox = draw.multiline_textbbox((0, 0), text, font=font_title, align="center")

    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    x = (W - tw) / 2
    y = (H - th) / 2

    draw = ImageDraw.Draw(img)

    draw.multiline_text(
        (x, y),
        text,
        font=font_title,
        fill="white",
        align="center"
    )

    return img.convert("RGB")


# =========================
# GENERAR TODO
# =========================

data = generar_contenido()["historias"]

for i, h in enumerate(data):

    titulo = h["titulo"]
    frase = h["frase"]
    post = h["post"]
    prompt_img = h["prompt_imagen"]

    img = generar_imagen(prompt_img)

    img = story_layout(img, titulo, frase)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename_img = f"stories/story_{timestamp}_{i}.png"
    filename_txt = f"stories/story_{timestamp}_{i}.txt"

    img.save(filename_img)

    with open(filename_txt, "w", encoding="utf-8") as f:
        f.write(post)

print("Historias generadas correctamente")

