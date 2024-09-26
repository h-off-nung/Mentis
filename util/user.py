from util.settings import Settings

class User:
    username = None
    language = 'en'
    model = "llama3-groq-70b-8192-tool-use-preview"

    @staticmethod
    def set_username(update, context):
        user = update.message.from_user.username
        if user in Settings.USERS:
            User.username = Settings.USERNAMES[Settings.USERS.index(user)]
        else:
            context.user_data['username'] = update.message.from_user.first_name
            User.username = context.user_data['username']

    @staticmethod
    async def welcome_user(update):
        user = update.message.from_user.username

        if user in Settings.USERS:
            user_index = Settings.USERS.index(user)
            user_messages = Settings.MESSAGES[user_index].split(';')
            for message in user_messages:
                await update.message.reply_text(message)
        else:
            if User.language == 'ru':
                await update.message.reply_text(f'Здравствуй, {User.username}!')
            else:
                await update.message.reply_text(f'Hi, {User.username}!')

    @staticmethod
    def initialize_message_history(context):
        language_mode = 'Russian' if User.language.startswith('ru') else 'English'
        context.user_data['message_history'] = [
            {"role": "system",
             "content": f"You should answer only in {language_mode}. User is called {User.username}. Call it each time you ask something. Use bold formatting in Markdown only when necessary to highlight important information."}
        ]