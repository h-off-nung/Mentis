import logging
from util.settings import Settings

from telegram import Update
from telegram.ext import Application as TelegramApplication, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.handlers import start, help_command, model_command, refresh_command, language_command, message_handler, callback

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def run():
    logging.info("Mentis is starting...")
    application = TelegramApplication.builder().token(Settings.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("model", model_command))
    application.add_handler(CommandHandler("refresh", refresh_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(MessageHandler(filters.VOICE, message_handler))
    application.add_handler(CallbackQueryHandler(callback))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
