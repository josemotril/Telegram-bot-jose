import os
import json
import base64
from datetime import datetime
from io import BytesIO

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont


# ======================================
# CONFIG GLOBAL
# ======================================

W, H = 1024, 1536
SAFE_MARGIN = 120

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

os.makedirs("stories", exist_ok=True)


# ======================================
# GPT → CONTENIDO PROFESIONAL
# ======================================

def generar_contenido():

    prompt = """
Devuelve SOLO JSON válido.

Genera 3 historias gastronómicas premium estilo Instagram profesional.

Formato EXACTO:

{
 "historias":[
   {
     "titulo":"máx 4 palabras",
     "frase":"frase corta inspiradora",
     "post":"texto profesional gastronómico 5-7 líneas útil y educativo",
     "prompt_imagen":"descripción fotográfica realista del plato relacionado con el texto"
   }
 ]
}

Tipos variados:
- receta
- técnica culinaria
- curiosidad gastronómica
- chef tip
- cultura foodie

Tono: elegante, moderno, profesional, revista gastronómica.
"""

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0
    )

    return json.loads(r.choices[0].message.content)["historias"]


# ======================================
# IA → IMAGEN REALISTA
# ======================================

def generar_imagen(prompt):

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt + ", fotografía gastronómica profesional, luz natural, fondo limpio, estilo editorial",
        size="1024x1536"
    )

    img_bytes = base64.b64decode(result.data[0].b64_json)

    return Image.open(BytesIO(img_bytes)).convert("RGBA")


# ======================================
# DISEÑO EDITORIAL PREMIUM
# ======================================

def story_layout(img, titulo, frase):

    img = img.resize((W, H))

    # overlay oscuro elegante inferior
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    draw_overlay = ImageDraw.Draw(overlay)

    box_h = 520
    y_box = H - box_h

    draw_overlay.rectangle(
        [(0, y_box), (W, H)],
        fill=(0, 0, 0, 200)
    )

    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
        sub_font = ImageFont.truetype("DejaVuSans.ttf", 46)
        brand_font = ImageFont.truetype("DejaVuSans.ttf", 30)
    except:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()


    # ---------- CENTRADO PERFECTO ----------
    def centered(text, font, y):

        bbox = draw.textbbox((0,0), text, font=font)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2

        draw.text((x, y), text, font=font, fill="white")


    y = y_box + 90

    centered(titulo.upper(), title_font, y)
    centered(frase, sub_font, y + 130)

    # línea fina decorativa
    draw.line(
        (W*0.2, y+200, W*0.8, y+200),
        fill="white",
        width=2
    )

    # marca
    draw.text(
        (SAFE_MARGIN, H-70),
        "@JoseMotril",
        font=brand_font,
        fill=(255,255,255,180)
    )

    return img.convert("RGB")


# ======================================
# MAIN
# ======================================

def main():

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

    print("✅ Historias PRO generadas correctamente")


if __name__ == "__main__":
    main()
