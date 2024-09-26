from telegram import Update
from telegram.ext import CallbackContext

from util.user import User


class Translation:
    COMMANDS = {
        'en': {
            'start': 'Welcome! My name is Mentis, I am an intelligent assistant. \nType /help to see available commands.\nIf my responses seem odd, please do a /refresh.',
            'help': '/help - Display all available commands\n/model - Change the language model\n/refresh - Start a new chat session (forget the previous context)\n/language - Change the assistant\'s language',
            'refresh': 'Chat history cleared. Starting a new session 🫡',
            'language_command': 'Choose your preferred language:',
            'language_change': 'Language changed to English.',
            'model_command': r'''Choose your preferred model:
    1\. Quick and compact version\.
    2\. The default, advanced and talkative variant\.
    3\. Lightning\-fast response\.
    4\. Google\-trained, offering good text formatting\.''',
            'model_change': 'Model has been successfully changed, beep boop 🤖',
            'context_length_exceeded': 'The conversation is too long. Please use /refresh to start a new session.'
        },
        'ru': {
            'start': 'Добро пожаловать! Меня зовут Ментис, я - интеллектуальный помощник. \nВведите /help, чтобы увидеть доступные команды.\nЕсли мои ответы кажутся странными, пожалуйста, выполните /refresh.',
            'help': '/help - Показать все доступные команды\n/model - Изменить языковую модель\n/refresh - Начать новый сеанс чата (забыть предыдущий контекст)\n/language - Изменить язык помощника',
            'refresh': 'История чата очищена. Начинаем новый сеанс 🫡',
            'language_command': 'Выберите предпочитаемый язык:',
            'language_change': 'Язык изменен на Русский.',
            'model_command': r'''Выберите предпочитаемую модель:
    1\. Быстрая и компактная\.
    2\. Дефолтная, продвинутая и разговорчивая\.
    3\. С молниеносным откликом\.
    4\. Обученная Google, с красивым форматированием текста\.''',
            'model_change': 'Модель успешно изменена, бип-буп 🤖',
            'context_length_exceeded': 'Разговор слишком длинный. Пожалуйста, используйте /refresh для начала новой сессии.'
        }
    }
    LANGUAGES = list(COMMANDS.keys())

    @staticmethod
    def set_user_language(update: Update, context: CallbackContext):
        user_language = update.message.from_user.language_code
        if user_language.startswith('ru'):
            context.user_data['language'] = 'ru'
            User.language = 'ru'
        else:
            context.user_data['language'] = 'en'
            User.language = 'en'

    @staticmethod
    def set_language(language: str) -> None:
        User.language = language

    @classmethod
    def get_text(cls, key: str) -> str:
        return cls.COMMANDS.get(User.language, {}).get(key, '')