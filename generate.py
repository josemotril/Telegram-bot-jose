import os
import base64
from io import BytesIO
from datetime import datetime

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

W, H = 1080, 1920
os.makedirs("stories", exist_ok=True)


# 🔥 GPT genera contenido completo (story + post)
def generar_contenido():

    prompt = """
    Crea contenido profesional para Instagram gastronómico.

    Devuelve EXACTAMENTE:

    TITULO: frase corta potente (máx 4 palabras)
    FRASE: frase corta inspiradora (máx 12 palabras)
    POST: texto largo explicativo de 4-6 líneas
    PROMPT_IMAGEN: descripción visual muy concreta de la foto
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    data = {}
    for l in r.choices[0].message.content.split("\n"):
        if ":" in l:
            k, v = l.split(":", 1)
            data[k.strip()] = v.strip()

    return data


def generar_imagen(prompt):
    r = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1536"
    )

    img_bytes = base64.b64decode(r.data[0].b64_json)
    return Image.open(BytesIO(img_bytes)).convert("RGB").resize((W, H))


# 🔥 Story minimalista centrada
def overlay_text(img, titulo, frase):

    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)

    # degradado suave
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 120))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 110)
    font_sub = ImageFont.truetype("DejaVuSans.ttf", 55)
    font_brand = ImageFont.truetype("DejaVuSans.ttf", 36)

    # 🔥 centrado REAL
    def center(text, font, y):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        draw.text((x, y), text, font=font, fill="white")

    center(titulo, font_title, H//2 - 150)
    center(frase, font_sub, H//2 + 10)

    draw.text((50, H-80), "@JoseMotril", font=font_brand, fill="white")

    return img.convert("RGB")


# 🔥 Generar 3 stories
for i in range(3):

    c = generar_contenido()

    titulo = c["TITULO"]
    frase = c["FRASE"]
    post = c["POST"]
    prompt_img = c["PROMPT_IMAGEN"]

    img = generar_imagen(prompt_img)
    img = overlay_text(img, titulo, frase)

    ts = datetime.now().strftime("%H%M%S")

    img.save(f"stories/story_{ts}_{i}.png")

    # 🔥 guardar texto largo para post
    with open(f"stories/post_{ts}_{i}.txt", "w", encoding="utf-8") as f:
        f.write(post)

print("Stories + captions generados")
