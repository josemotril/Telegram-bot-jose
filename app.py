import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def reenviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.forward_message(
        chat_id=CHAT_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, reenviar))

app.run_polling()
