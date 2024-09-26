from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.constants import ChatAction, ParseMode
from bot.groq_api import generate_reply, transcribe_audio
from util.format import format_for_telegram
from util.settings import Settings
from util.translation import Translation
from util.user import User
import io, requests

def user_only(func):
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user = update.message.from_user.username if update.message else update.callback_query.from_user.username
        if user in Settings.USERS:
            return await func(update, context, *args, **kwargs)
        else:
            if update.message:
                await update.message.reply_text('You are not authorized to use this bot.')
            else:
                await update.callback_query.answer(text='You are not authorized to use this command.')
            return
    return wrapper

@user_only
async def start(update: Update, context: CallbackContext) -> None:
    User.set_username(update, context)
    Translation.set_user_language(update, context)
    User.initialize_message_history(context)
    await update.message.reply_text(Translation.get_text('start'))
    await User.welcome_user(update)

@user_only
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(Translation.get_text('help'))

@user_only
async def refresh_command(update: Update, context: CallbackContext) -> None:
    User.initialize_message_history(context)
    await update.message.reply_text(Translation.get_text('refresh'))

@user_only
async def language_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="language:en"),
            InlineKeyboardButton("Русский", callback_data="language:ru"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(Translation.get_text('language_command'), reply_markup=reply_markup)

@user_only
async def message_handler(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    message_history = context.user_data.get('message_history', [])
    if update.message.voice:
        file_id = update.message.voice.file_id
        new_file = await context.bot.get_file(file_id)
        file_url = new_file.file_path
        response = requests.get(file_url)
        audio_data = io.BytesIO(response.content)
        user_message = transcribe_audio(audio_data)
    else:
        user_message = update.message.text
    message_history.append({"role": "user", "content": user_message})
    new_text = generate_reply(message_history, User.model)
    message_history.append({"role": "assistant", "content": new_text})
    context.user_data['message_history'] = message_history
    formatted_text = format_for_telegram(new_text)
    await update.message.reply_text(formatted_text, parse_mode=ParseMode.MARKDOWN_V2)

@user_only
async def model_command(update: Update, context: CallbackContext) -> None:
    models = [
        'llama3-groq-8b-8192-tool-use-preview',
        'llama3-groq-70b-8192-tool-use-preview',
        'llama-3.1-8b-instant',
        'gemma-7b-it',
    ]
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=f"model:{models[0]}"),
            InlineKeyboardButton("2", callback_data=f"model:{models[1]}"),
        ],
        [
            InlineKeyboardButton("3", callback_data=f"model:{models[2]}"),
            InlineKeyboardButton("4", callback_data=f"model:{models[3]}"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        Translation.get_text('model_command'),
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

@user_only
async def callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    if data.startswith("model:"):
        User.model = data.split(":")[1]
        await query.answer()
        await query.edit_message_text(text=Translation.get_text('model_change'))
    elif data.startswith("language:"):
        language = data.split(":")[1]
        context.user_data['language'] = language
        Translation.set_language(language)
        await query.edit_message_text(text=Translation.get_text('language_change'))
        await query.answer()