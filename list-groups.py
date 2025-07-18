import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import os

BOT_TOKEN = os.getenv("TOKEN") # type: ignore

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat is not None:
        print(f"Nome do chat: {chat.title}")
        print(f"chat_id: {chat.id}")
    else:
        print("Chat não disponível neste update")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build() # type: ignore

    app.add_handler(MessageHandler(filters.ALL, handle))
    app.run_polling()
