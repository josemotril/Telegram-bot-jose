import os
import base64
from io import BytesIO
from datetime import datetime
import random

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

W, H = 1080, 1920
os.makedirs("stories", exist_ok=True)


contenidos = [
    ("Gazpacho andaluz tradicional con AOVE temprano y tomate maduro. Sabor fresco y natural.",
     "Traditional Andalusian gazpacho with early harvest olive oil."),

    ("Tip profesional: afila cuchillos cada semana. Cortes limpios mejoran textura y sabor.",
     "Pro tip: sharpen knives weekly for cleaner cuts."),

    ("Curiosidad: el tratamiento HPP conserva nutrientes sin usar calor ni conservantes.",
     "Fun fact: HPP preserves nutrients without heat."),

    ("Cocinar es pasión, técnica y respeto por el producto. Menos es más.",
     "Cooking is passion, technique and respect for ingredients.")
]


# 🔥 GENERAR IMAGEN IA (BASE64 NUEVO FORMATO)
def generar_imagen(prompt):
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1536"
    )

    img_base64 = result.data[0].b64_json
    img_bytes = base64.b64decode(img_base64)

    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    return img.resize((W, H))


def overlay_text(img, es, en):
    img = img.convert("RGBA")

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 120))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 65)
    font_small = ImageFont.truetype("DejaVuSans.ttf", 45)

    y = 1200

    draw.multiline_text((80, y), es, font=font_big, fill="white")
    draw.multiline_text((80, y + 200), en, font=font_small, fill="white")
    draw.text((W - 250, H - 120), "@JoseMotril", font=font_small, fill="white")

    return img.convert("RGB")


for i in range(3):
    es, en = random.choice(contenidos)

    prompt = """
    professional food photography,
    mediterranean cuisine,
    natural light,
    editorial magazine style,
    realistic textures,
    instagram story composition,
    high quality,
    elegant
    """

    img = generar_imagen(prompt)
    img = overlay_text(img, es, en)

    filename = f"stories/story_{datetime.now().strftime('%H%M%S')}_{i}.png"
    img.save(filename)


print("Historias generadas correctamente")
