import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from core.config import settings
from core.database import get_session
from services.agent_service import run_research

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I am your autonomous Research Agent. 🤖\n\n"
        "Send me any question and I will search the web and write a report for you!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text

    await update.message.reply_text("🔍 Researching... this might take a minute. Please wait.")
    loop = asyncio.get_running_loop()
    session_generator = get_session()
    session = next(session_generator)

    try:
        result = await loop.run_in_executor(None, run_research, query, session)

        if result and result.report_markdown:
            report = result.report_markdown
            chunk_size = 4000
            for i in range(0, len(report), chunk_size):
                await update.message.reply_text(report[i:i+chunk_size])
        else:
            await update.message.reply_text("❌ Research failed or returned no results.")
    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred: {str(e)}")
    finally:
        session.close()

def start_telegram_bot():
    """Starts the telegram bot event loop"""
    if not settings.telegram_bot_token:
        print("Error: Please set TELEGRAM_BOT_TOKEN in your .env file.")
        return

    app = ApplicationBuilder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram Bot is running! Press Ctrl+C to stop.")
    app.run_polling()