import os
import json
import base64
from io import BytesIO
from datetime import datetime

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont


# =========================================
# CONFIG
# =========================================

W_STORY, H_STORY = 1024, 1536
W_POST, H_POST = 1080, 1350   # carrusel 4:5 Instagram

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

os.makedirs("output", exist_ok=True)


# =========================================
# GPT CONTENIDO COMPLETO
# =========================================

def generar_contenido():

    prompt = """
Devuelve SOLO JSON válido.

Genera 1 tema gastronómico profesional.

Formato:

{
 "titulo":"",
 "frase":"",
 "slides":[
   "texto slide 1 portada corto",
   "texto slide 2 desarrollo",
   "texto slide 3 tip práctico",
   "texto slide 4 cierre o CTA"
 ],
 "caption":"texto largo profesional 6-8 líneas",
 "hashtags":"#gastronomia #chef ...",
 "prompts_imagen":[
   "prompt imagen 1",
   "prompt imagen 2",
   "prompt imagen 3",
   "prompt imagen 4",
   "prompt imagen story"
 ]
}

Estilo Michelin, editorial, profesional.
"""

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=1
    )

    return json.loads(r.choices[0].message.content)


# =========================================
# IMAGEN IA
# =========================================

def generar_imagen(prompt, size):

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt + ", fotografía gastronómica profesional, luz natural, estilo editorial",
        size=size
    )

    img_bytes = base64.b64decode(result.data[0].b64_json)
    return Image.open(BytesIO(img_bytes)).convert("RGBA")


# =========================================
# FONTS
# =========================================

def fonts():
    try:
        return (
            ImageFont.truetype("DejaVuSans-Bold.ttf", 90),
            ImageFont.truetype("DejaVuSans.ttf", 50),
            ImageFont.truetype("DejaVuSans.ttf", 42)
        )
    except:
        f = ImageFont.load_default()
        return f, f, f


# =========================================
# STORY LAYOUT
# =========================================

def layout_story(img, titulo, frase):

    img = img.resize((W_STORY, H_STORY)).convert("RGBA")

    # ===== degradado suave inferior =====
    gradient = Image.new("L", (1, H_STORY))
    for y in range(H_STORY):
        value = int(255 * (y / H_STORY) ** 2)
        gradient.putpixel((0, y), value)

    alpha = gradient.resize(img.size)

    black = Image.new("RGBA", img.size, (0, 0, 0, 190))

    img = Image.composite(black, img, alpha)

    draw = ImageDraw.Draw(img)

    f_title, f_sub, _ = fonts()

    # ===== tamaños más elegantes =====
    f_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
    f_sub = ImageFont.truetype("DejaVuSans.ttf", 44)

    SAFE = 140

    def wrap(text, font, max_width):
        words = text.split()
        lines = []
        line = ""
        for w in words:
            test = line + w + " "
            if draw.textlength(test, font=font) < max_width:
                line = test
            else:
                lines.append(line)
                line = w + " "
        lines.append(line)
        return lines


    max_w = W_STORY - SAFE*2

    title_lines = wrap(titulo.upper(), f_title, max_w)
    sub_lines = wrap(frase, f_sub, max_w)

    total_h = len(title_lines)*90 + len(sub_lines)*60

    y = int(H_STORY*0.65 - total_h/2)

    # ===== centrado perfecto =====
    for l in title_lines:
        w = draw.textlength(l, font=f_title)
        draw.text(((W_STORY-w)//2, y), l, font=f_title, fill="white")
        y += 90

    y += 20

    for l in sub_lines:
        w = draw.textlength(l, font=f_sub)
        draw.text(((W_STORY-w)//2, y), l, font=f_sub, fill=(235,235,235))
        y += 60

    # branding pequeño
    draw.text((60, H_STORY-70), "@JoseMotril", fill=(255,255,255,170), font=f_sub)

    return img.convert("RGB")



# =========================================
# CARRUSEL LAYOUT
# =========================================

def layout_slide(img, texto):

    img = img.resize((W_POST, H_POST))

    overlay = Image.new("RGBA", img.size, (0,0,0,160))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)
    _, _, f_body = fonts()

    margin = 120

    words = texto.split()
    lines = []
    line = ""

    for w in words:
        test = line + w + " "
        if draw.textlength(test, font=f_body) < W_POST - margin*2:
            line = test
        else:
            lines.append(line)
            line = w + " "
    lines.append(line)

    y = H_POST//2 - len(lines)*30

    for l in lines:
        w = draw.textlength(l, font=f_body)
        draw.text(((W_POST-w)//2, y), l, font=f_body, fill="white")
        y += 60

    return img.convert("RGB")


# =========================================
# MAIN
# =========================================

def main():

    c = generar_contenido()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ---------- STORY ----------
    story_img = generar_imagen(c["prompts_imagen"][4], "1024x1536")
    story_img = layout_story(story_img, c["titulo"], c["frase"])
    story_img.save(f"output/story.png")


    # ---------- CARRUSEL ----------
    for i in range(4):

        img = generar_imagen(c["prompts_imagen"][i], "1024x1024")
        slide = layout_slide(img, c["slides"][i])
        slide.save(f"output/carrusel_{i+1}.png")


    # ---------- TEXTO ----------
    with open("output/caption.txt","w",encoding="utf-8") as f:
        f.write(c["caption"])

    with open("output/hashtags.txt","w",encoding="utf-8") as f:
        f.write(c["hashtags"])

    print("✅ Story + Carrusel + Post generados correctamente")


if __name__ == "__main__":
    main()
