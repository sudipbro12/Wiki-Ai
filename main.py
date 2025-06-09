import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Hardcoded bot token
BOT_TOKEN = "7699905568:AAFLHr44fH_OQo68cP2zTWch8UfitPR5OD4"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

user_languages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Wiki-Ai Bot!\n"
        "Send any topic to search Wikipedia.\n"
        "Change language with /lang en or /lang bn"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start bot\n"
        "/help - Help info\n"
        "/lang en or /lang bn - Set language\n"
        "Just send a topic to search."
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /lang en or /lang bn")
        return

    lang = args[0].lower()
    if lang in ["en", "bn"]:
        user_languages[user_id] = lang
        await update.message.reply_text(f"Language set to {'English' if lang=='en' else 'Bengali'}")
    else:
        await update.message.reply_text("Only 'en' and 'bn' supported.")

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
            await update.message.reply_text(f"*{title}*\n\n{summary}", parse_mode="Markdown")
        else:
            await update.message.reply_text("No summary found.")
    else:
        await update.message.reply_text("Article not found.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("lang", set_language))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_topic))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
