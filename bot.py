import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("asqs-bot")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_URL = os.getenv("TELEGRAM_CHANNEL_URL", "https://t.me/your_channel")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join ASQS Profit Zone", url=CHANNEL_URL)],
        [InlineKeyboardButton("✅ Check Membership", callback_data="check_membership")]
    ]
    await update.message.reply_text(
        "🚀 Welcome to ASQS PROFIT ZONE!\n\n"
        "Join the community using the button below. "
        "After joining, tap “Check Membership”.\n\n"
        "Educational content only — no guaranteed profits.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CHANNEL_ID:
        await update.message.reply_text("CHANNEL_ID is not configured.")
        return
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=update.effective_user.id,
        )
        await update.message.reply_text(f"Your channel status: {member.status}")
    except Exception as exc:
        log.warning("Membership check failed: %s", exc)
        await update.message.reply_text(
            "I couldn't verify membership. Make sure you joined the channel."
        )

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not CHANNEL_ID:
        await query.message.reply_text("CHANNEL_ID is not configured.")
        return
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=query.from_user.id,
        )
        if member.status in ("creator", "administrator", "member"):
            await query.message.reply_text(
                "✅ Membership verified!\n\n"
                "Welcome to ASQS PROFIT ZONE. 🎉"
            )
        else:
            await query.message.reply_text(
                "❌ Membership not verified yet. Please join the channel first."
            )
    except Exception as exc:
        log.warning("Membership callback failed: %s", exc)
        await query.message.reply_text(
            "❌ I couldn't verify membership right now. Please try again."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — Join and start\n"
        "/status — Check your membership\n"
        "/help — Show help"
    )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is required.")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(__import__("telegram").ext.CallbackQueryHandler(
        check_membership, pattern="^check_membership$"
    ))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
