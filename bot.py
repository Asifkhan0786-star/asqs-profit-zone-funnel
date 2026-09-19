import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_URL = os.getenv("TELEGRAM_CHANNEL_URL", "https://t.me/your_channel")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Join Telegram Channel", url=CHANNEL_URL)]]
    await update.message.reply_text(
        "Welcome! Please join the channel using the button below. "
        "This bot does not send unsolicited messages.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CHANNEL_ID:
        await update.message.reply_text("CHANNEL_ID is not configured yet.")
        return

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=update.effective_user.id,
        )
        await update.message.reply_text(f"Your channel status: {member.status}")
    except Exception:
        await update.message.reply_text(
            "I couldn't verify membership yet. Make sure you joined the channel."
        )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is required.")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
