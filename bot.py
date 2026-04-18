from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler, filters
from voice import text_to_file
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
#TOKEN = "8533960104:AAGD3pV3vNZf-VfMEYMTOXOrpcfgNczC2vA"
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def help_hendler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(""" Цей бот може перетворити звичайне текстове повідомлення на аудіо повідомлення. Очікую на будь-який текст.""")

async def reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text("Озвучимо текст: " + update.message.text)

async def reply_message_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    file_name = text_to_file(update.message.text)
    await update.message.reply_voice(voice= open(file_name,"rb"))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("help", help_hendler))
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,reply_message_voice))

app.run_polling()
