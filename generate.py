import os
import base64
import random
from io import BytesIO
from datetime import datetime

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

W, H = 1080, 1920
os.makedirs("stories", exist_ok=True)


# 🔥 1. GPT genera el contenido del día
def generar_contenido():
    prompt = """
    Crea contenido para una historia de Instagram gastronómica profesional.

    Devuelve en este formato exacto:

    TITULO: ...
    TEXTO_ES: ...
    TEXTO_EN: ...
    PROMPT_IMAGEN: ...

    El contenido debe ser profesional, elegante, útil y realista.
    Puede ser receta, técnica, curiosidad gastronómica o reflexión de chef.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    texto = response.choices[0].message.content

    partes = {}
    for linea in texto.split("\n"):
        if ":" in linea:
            clave, valor = linea.split(":", 1)
            partes[clave.strip()] = valor.strip()

    return partes


# 🔥 2. Generar imagen coherente con prompt IA
def generar_imagen(prompt_imagen):
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt_imagen,
        size="1024x1536"
    )

    img_bytes = base64.b64decode(result.data[0].b64_json)
    img = Image.open(BytesIO(img_bytes)).convert("RGB")

    return img.resize((W, H))


# 🔥 3. Overlay profesional
def overlay_text(img, titulo, es, en):
    img = img.convert("RGBA")

    box = Image.new("RGBA", (W, 600), (0, 0, 0, 190))
    img.paste(box, (0, H - 600), box)

    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
    font_body = ImageFont.truetype("DejaVuSans.ttf", 48)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 38)

    margin = 90
    y = H - 520

    draw.text((margin, y), titulo, font=font_title, fill="white")
    draw.multiline_text((margin, y + 120), es, font=font_body, fill="white", spacing=8)
    draw.multiline_text((margin, y + 280), en, font=font_small, fill=(210, 210, 210), spacing=6)

    draw.text((margin, H - 80), "@JoseMotril", font=font_small, fill=(200, 200, 200))

    return img.convert("RGB")


# 🔥 Generar 3 historias diferentes cada vez
for i in range(3):

    contenido = generar_contenido()

    titulo = contenido.get("TITULO", "Gastronomía")
    texto_es = contenido.get("TEXTO_ES", "")
    texto_en = contenido.get("TEXTO_EN", "")
    prompt_imagen = contenido.get("PROMPT_IMAGEN", "professional food photography")

    img = generar_imagen(prompt_imagen)
    img = overlay_text(img, titulo, texto_es, texto_en)

    filename = f"stories/story_{datetime.now().strftime('%H%M%S')}_{i}.png"
    img.save(filename)

print("Historias dinámicas generadas correctamente")
