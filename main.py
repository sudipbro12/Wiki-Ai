import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# ⚠️ Your bot token directly here (DON'T share it with others!)
BOT_TOKEN = "7699905568:AAFLHr44fH_OQo68cP2zTWch8UfitPR5OD4"

# ✅ Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Store language preferences per user
user_languages = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Wiki-Ai Bot!\n\n"
        "📘 Send me any topic to search on Wikipedia.\n"
        "🌐 Use /lang en or /lang bn to change language."
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Commands:\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/lang en - English\n"
        "/lang bn - Bengali\n"
        "📚 Just type a topic to search on Wikipedia."
    )

# /lang command
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text("⚠️ Usage: /lang en or /lang bn")
        return

    lang = args[0].lower()
    if lang in ["en", "bn"]:
        user_languages[user_id] = lang
        await update.message.reply_text(f"✅ Language set to {'English' if lang == 'en' else 'Bengali'}")
    else:
        await update.message.reply_text("❌ Only 'en' and 'bn' are supported.")

# Wikipedia search function
async def search_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, "en")

    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        summary = data.get("extract")
        title = data.get("title", query)
        if summary:
            await update.message.reply_text(f"📖 *{title}*:\n\n{summary}", parse_mode="Markdown")
        else:
            await update.message.reply_text("⚠️ No summary found.")
    else:
        await update.message.reply_text("❌ Article not found or error occurred.")

# Main bot runner
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("lang", set_language))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_topic))

    print("🚀 Bot is running...")
    await app.run_polling()

# Run the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
