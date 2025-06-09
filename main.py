import logging
import requests
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# ✅ Get BOT_TOKEN from environment variable (Railway or local .env)
BOT_TOKEN = os.getenv("7699905568:AAHEhmdGFY9_w90fPgwD8BEEGLAKonJL6-o")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not found. Set it as an environment variable.")

# 🔧 Enable logging
logging.basicConfig(level=logging.INFO)

# 🌐 Track user language preferences
user_lang = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *Wiki-Ai Bot*!\n\n"
        "🔍 Just send me any topic name to search Wikipedia.\n"
        "🌐 Use /lang en or /lang bn to set your language.\nℹ️ Use /help for more commands.",
        parse_mode="Markdown"
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *Wiki-Ai Bot Commands:*\n\n"
        "• Send any topic to search Wikipedia\n"
        "• /lang en — Search in English\n"
        "• /lang bn — Search in Bengali\n"
        "• /about — Bot info\n",
        parse_mode="Markdown"
    )

# /about command
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Wiki-Ai Bot*\n\n"
        "Made with Python + Wikipedia REST API.\n"
        "Supports English and Bengali summaries.\n"
        "Hosted on Railway.\n\n"
        "Built by Sudip ❤️",
        parse_mode="Markdown"
    )

# /lang command
async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text("❗Usage: /lang en or /lang bn")
        return

    lang = args[0].lower()
    if lang in ["en", "bn"]:
        user_lang[user_id] = lang
        await update.message.reply_text(f"✅ Language set to {'English' if lang == 'en' else 'Bengali'}")
    else:
        await update.message.reply_text("❌ Only 'en' (English) and 'bn' (Bengali) are supported.")

# Wikipedia search handler
async def search_wikipedia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "en")  # Default language: English

    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        summary = data.get("extract")
        if summary:
            await update.message.reply_text(f"🔎 *{query}*:\n\n{summary}", parse_mode="Markdown")
        else:
            await update.message.reply_text("⚠️ No summary found.")
    elif response.status_code == 404:
        await update.message.reply_text("❌ Article not found on Wikipedia.")
    else:
        await update.message.reply_text("⚠️ Failed to connect to Wikipedia API.")

# Main app startup
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("lang", lang_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_wikipedia))

    print("🚀 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
