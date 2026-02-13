import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_TO   = os.environ["EMAIL_TO"]

msg = EmailMessage()
msg["Subject"] = "📸 Historias Instagram listas"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO

msg.set_content("""
Tus contenidos están listos:

✅ Stories
✅ Carrusel
✅ Post
✅ Hashtags

Adjuntos abajo.
""")

# adjuntar todos los archivos de /output
for file in Path("output").glob("*"):
    with open(file, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=file.name
        )

with smtplib.SMTP_SSL("smtp.office365.com", 465) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)

print("Email enviado correctamente")
