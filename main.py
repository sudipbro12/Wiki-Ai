import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = "7699905568:AAE2qfZEZfKRiw_jbpnB5zkthH9c93ovmNM"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Welcome to the Wikipedia Search Bot!\n"
        "Send me any word or phrase, and I'll fetch the summary from Wikipedia."
    )

async def search_wikipedia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        await update.message.reply_text("Please send a valid search term.")
        return

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        summary = data.get("extract")
        if summary:
            await update.message.reply_text(f"🔎 About *{query}*:\n\n{summary}", parse_mode="Markdown")
        else:
            await update.message.reply_text("No summary available for this topic.")
    elif response.status_code == 404:
        await update.message.reply_text("❌ No Wikipedia article found for that query.")
    else:
        await update.message.reply_text("❌ Something went wrong while fetching data.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_wikipedia))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
