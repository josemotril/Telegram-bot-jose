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

# 🔥 Contenido más elaborado
contenidos = [
    (
        "Gazpacho andaluz tradicional\n\nTomate pera maduro, AOVE temprano y vinagre suave.\nTextura sedosa y frescura natural.",
        "Traditional Andalusian gazpacho\nRipe tomatoes, early harvest olive oil and smooth vinegar."
    ),
    (
        "Técnica profesional en cocina\n\nAfila tus cuchillos cada semana.\nCortes limpios mejoran textura y precisión.",
        "Professional kitchen tip\nSharpen knives weekly for cleaner and more precise cuts."
    ),
    (
        "Curiosidad gastronómica\n\nEl tratamiento HPP conserva nutrientes sin aplicar calor.\nMayor vida útil, mismo sabor.",
        "Gastronomy fact\nHPP preserves nutrients without heat."
    ),
    (
        "Cocinar es equilibrio\n\nProducto, técnica y respeto.\nMenos ingredientes, más intención.",
        "Cooking is balance\nIngredients, technique and respect."
    )
]

# 🔥 Generar imagen IA
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


# 🔥 Overlay profesional estilo editorial
def overlay_text(img, es, en):
    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Degradado elegante inferior
    gradient = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(gradient)

    for y in range(H):
        alpha = int(220 * (y / H))
        grad_draw.line((0, y, W, y), fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, gradient)
    draw = ImageDraw.Draw(img)

    # Tipografías
    font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 74)
    font_body = ImageFont.truetype("DejaVuSans.ttf", 44)
    font_brand = ImageFont.truetype("DejaVuSans.ttf", 38)

    margin = 90
    y_start = int(H * 0.60)

    # Texto español (principal)
    draw.multiline_text(
        (margin, y_start),
        es,
        font=font_title,
        fill="white",
        spacing=10
    )

    # Texto inglés (subtítulo)
    draw.multiline_text(
        (margin, y_start + 280),
        en,
        font=font_body,
        fill=(230, 230, 230),
        spacing=6
    )

    # Firma
    draw.text(
        (margin, H - 110),
        "@JoseMotril",
        font=font_brand,
        fill=(220, 220, 220)
    )

    return img.convert("RGB")


# 🔥 Generar 3 historias diferentes
for i in range(3):
    es, en = random.choice(contenidos)

    prompt = """
    professional food photography,
    mediterranean cuisine,
    natural window light,
    cinematic composition,
    editorial magazine style,
    realistic textures,
    instagram story format,
    elegant, modern, premium
    """

    img = generar_imagen(prompt)
    img = overlay_text(img, es, en)

    filename = f"stories/story_{datetime.now().strftime('%H%M%S')}_{i}.png"
    img.save(filename)

print("Historias generadas correctamente")

