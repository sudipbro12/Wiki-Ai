import logging
import requests
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

BOT_TOKEN = os.getenv("7699905568:AAE2qfZEZfKRiw_jbpnB5zkthH9c93ovmNM")
logging.basicConfig(level=logging.INFO)

user_lang = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *Wiki-Ai*! Just send me any topic to search Wikipedia.\n\n"
        "🌐 Use /lang en or /lang bn to change language.\nℹ️ Use /help for more.",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *Wiki-Ai Help Menu:*\n\n"
        "• Send any topic to search Wikipedia\n"
        "• /lang en — Set language to English\n"
        "• /lang bn — Set language to Bengali\n"
        "• /about — Bot info\n",
        parse_mode="Markdown"
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Wiki-Ai Bot*\nBuilt using Python & Telegram Bot API.\n"
        "Powered by Wikipedia REST API.\n\n"
        "Made with ❤️ by Sudip.",
        parse_mode="Markdown"
    )

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
        await update.message.reply_text("❌ Only 'en' and 'bn' are supported.")

async def search_wikipedia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    user_id = update.effective_user.id
    lang = user_lang.get(user_id, "en")

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
        await update.message.reply_text("❌ No Wikipedia article found.")
    else:
        await update.message.reply_text("⚠️ Failed to fetch data from Wikipedia.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

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
