from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

import os
import logging

token = os.environ.get('BOT_TOKEN')
if not token:
    raise Exception('Token is not provided')
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Voice to text bot')


async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file_id = update.message.voice.file_id
    logging.info(f"Downloading {file_id} audio")
    audio = await context.bot.get_file(file_id)
    await audio.download_to_drive()


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.ALL, download_audio))

    application.run_polling()